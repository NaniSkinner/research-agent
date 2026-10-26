import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name) / 'cedar'
        self.workspace.mkdir()
        spec = importlib.util.spec_from_file_location('manage', ROOT / 'scripts/manage.py')
        self.manage = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.manage)

    def test_stage_and_check_preserve_contract(self):
        receipt = self.manage.stage(ROOT, self.workspace)
        checked = self.manage.check(self.workspace)
        self.assertEqual(checked['contract_sha256'], receipt['contract_sha256'])
        import tomllib
        data = tomllib.loads((self.workspace / '.codex/agents/project-researcher.toml').read_text())
        self.assertEqual(data['name'], 'project-researcher')
        self.assertIn((ROOT / 'project-research/references/contract.md').read_text(), data['developer_instructions'])
        self.assertNotIn('model', data)

    def test_stage_refuses_existing_registration_without_changes(self):
        path = self.workspace / '.codex/agents/project-researcher.toml'
        path.parent.mkdir(parents=True)
        path.write_text('unrelated owner')
        with self.assertRaises(ValueError):
            self.manage.stage(ROOT, self.workspace)
        self.assertEqual(path.read_text(), 'unrelated owner')
        self.assertFalse((self.workspace / '.agents/skills/project-research').exists())

    def test_changed_profile_blocks_check_and_removal(self):
        self.manage.stage(ROOT, self.workspace)
        path = self.workspace / '.codex/agents/project-researcher.toml'
        path.write_text(path.read_text() + '\n# local edit\n')
        with self.assertRaises(ValueError):
            self.manage.check(self.workspace)
        with self.assertRaises(ValueError):
            self.manage.remove(self.workspace)
        self.assertTrue(path.exists())

    def test_rollback_only_removes_owned_files(self):
        self.manage.stage(ROOT, self.workspace)
        other = self.workspace / 'keep.txt'
        other.write_text('keep')
        self.manage.remove(self.workspace)
        self.assertEqual(other.read_text(), 'keep')
        self.assertFalse((self.workspace / '.codex/agents/project-researcher.toml').exists())
        self.assertFalse((self.workspace / '.agents/skills/project-research').is_symlink())

    def copied_source(self):
        import shutil
        source = Path(self.temp.name) / 'source'
        shutil.copytree(ROOT / 'project-research', source / 'project-research')
        return source

    def test_directory_symlink_is_rejected_before_staging(self):
        source = self.copied_source()
        (source / 'project-research/linked').symlink_to(ROOT / 'docs', target_is_directory=True)
        with self.assertRaises(ValueError):
            self.manage.stage(source, self.workspace)
        self.assertFalse((self.workspace / '.codex/agents/project-researcher.toml').exists())

    def test_broken_source_symlink_is_rejected(self):
        source = self.copied_source()
        (source / 'project-research/missing').symlink_to(source / 'absent')
        with self.assertRaises(ValueError):
            self.manage.stage(source, self.workspace)

    def test_new_directory_symlink_invalidates_consistency(self):
        source = self.copied_source()
        self.manage.stage(source, self.workspace)
        (source / 'project-research/linked').symlink_to(ROOT / 'docs', target_is_directory=True)
        with self.assertRaises(ValueError):
            self.manage.check(self.workspace)

    def test_source_updates_do_not_prevent_owned_registration_removal(self):
        source = self.copied_source()
        self.manage.stage(source, self.workspace)
        contract = source / 'project-research/references/contract.md'
        contract.write_text(contract.read_text() + '\nRevised contract.\n')
        with self.assertRaises(ValueError):
            self.manage.check(self.workspace)
        self.manage.remove(self.workspace)
        self.assertTrue(contract.exists())
        self.assertFalse((self.workspace / '.codex/agents/project-researcher.toml').exists())

    def test_personal_profile_check_reads_actual_registered_copy(self):
        staged = self.manage.stage(ROOT, self.workspace)
        profile = self.workspace / '.codex/agents/project-researcher.toml'
        checked = self.manage.check_profile(ROOT, profile)
        self.assertEqual(checked['profile_sha256'], staged['profile_sha256'])
        self.assertEqual(checked['scope'], 'source/profile consistency only')

    def test_personal_profile_check_rejects_stale_instructions(self):
        source = self.copied_source()
        self.manage.stage(source, self.workspace)
        profile = self.workspace / '.codex/agents/project-researcher.toml'
        contract = source / 'project-research/references/contract.md'
        contract.write_text(contract.read_text() + '\nUpdated instruction.\n')
        with self.assertRaises(ValueError):
            self.manage.check_profile(source, profile)

    def test_personal_profile_check_rejects_missing_path(self):
        with self.assertRaises(ValueError):
            self.manage.check_profile(ROOT, self.workspace / 'absent.toml')

    def test_dependency_check_detects_missing_required_leaf(self):
        pstack = self.workspace / 'resources'
        evidence = self.workspace / 'evidence.md'
        evidence.write_text('instructions')
        with self.assertRaises(ValueError):
            self.manage.doctor(pstack, evidence)

    def test_valid_receipt_is_structural_only(self):
        report = {'status': 'independently-checked', 'baseline': 'abc', 'claims': [{'id': 'c1', 'status': 'supported', 'source': 'src/app.py:12', 'category': 'observed-current-fact'}], 'review': {'reviewer_id': 'fresh-1', 'fork_turns': 'none', 'baseline': 'abc', 'checked_claims': ['c1'], 'findings': [], 'dispositions': []}}
        self.manage.validate_report(report)
        for key, value in [('fork_turns', 'all'), ('baseline', 'different'), ('reviewer_id', '')]:
            broken = copy.deepcopy(report)
            broken['review'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.manage.validate_report(broken)
        broken = copy.deepcopy(report)
        broken['review']['checked_claims'] = []
        with self.assertRaises(ValueError):
            self.manage.validate_report(broken)

    def test_review_findings_require_explicit_disposition(self):
        report = {'status': 'independently-checked', 'baseline': 'abc', 'claims': [], 'review': {'reviewer_id': 'fresh-1', 'fork_turns': 'none', 'baseline': 'abc', 'checked_claims': [], 'findings': [{'id': 'r1'}], 'dispositions': []}}
        with self.assertRaises(ValueError):
            self.manage.validate_report(report)

    def test_blocked_report_cannot_claim_independent_completion(self):
        self.manage.validate_report({'status': 'verification-blocked', 'baseline': 'abc', 'claims': []})
        with self.assertRaises(ValueError):
            self.manage.validate_report({'status': 'independently-checked', 'baseline': 'abc', 'claims': []})

if __name__ == '__main__':
    unittest.main()
