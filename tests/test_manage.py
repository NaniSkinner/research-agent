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

    def report_with_workflow(self):
        return {
            'status': 'independently-checked', 'baseline': 'abc',
            'claims': [{'id': 'c1', 'status': 'supported', 'source': 'src/app.py:12', 'category': 'observed-current-fact'}],
            'workflow': {'playbook': 'resolved/playbook.md', 'initialization': 'current-turn-only',
                         'persistence': 'unverified', 'completion': 'complete',
                         'steps': [{'name': 'Owner-defined applicable step', 'required': True, 'status': 'done', 'evidence': 'report:source-map'}]},
            'review': {'reviewer_id': 'fresh-1', 'fork_turns': 'none', 'baseline': 'abc',
                       'context_evidence': {'kind': 'host-confirmed', 'locator': 'supported-dispatch:abc'},
                       'checked_claims': ['c1'], 'findings': [], 'dispositions': []}}

    def test_valid_receipt_is_structural_only(self):
        report = self.report_with_workflow()
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

    def test_reported_context_cannot_pass_full_independence(self):
        report = self.report_with_workflow()
        report['review']['context_evidence']['kind'] = 'requested-only'
        with self.assertRaises(ValueError):
            self.manage.validate_report(report)

    def test_source_review_can_preserve_unverified_context(self):
        report = self.report_with_workflow()
        report['status'] = 'source-reviewed-context-unverified'
        report['review']['context_evidence'] = {'kind': 'requested-only', 'locator': 'caller:spawn-request'}
        self.manage.validate_report(report)

    def test_missing_workflow_cannot_pass_reviewed_report(self):
        report = self.report_with_workflow()
        del report['workflow']
        with self.assertRaises(ValueError):
            self.manage.validate_report(report)

    def test_required_blocked_step_prevents_workflow_completion(self):
        report = self.report_with_workflow()
        report['workflow']['steps'][0]['status'] = 'blocked'
        with self.assertRaises(ValueError):
            self.manage.validate_report(report)

    def test_partial_workflow_can_be_reported_without_full_pass(self):
        report = self.report_with_workflow()
        report['status'] = 'source-reviewed-context-unverified'
        report['review']['context_evidence']['kind'] = 'requested-only'
        report['workflow']['steps'][0]['status'] = 'blocked'
        report['workflow']['completion'] = 'partial'
        self.manage.validate_report(report)

    def test_trusted_persistence_requires_receipt(self):
        report = self.report_with_workflow()
        report['workflow']['initialization'] = 'trusted-sticky'
        report['workflow']['persistence'] = 'verified'
        with self.assertRaises(ValueError):
            self.manage.validate_report(report)

    def test_verified_persistence_requires_consistent_initialization(self):
        report = self.report_with_workflow()
        report['workflow']['persistence'] = 'verified'
        report['workflow']['sticky_receipt'] = 'supported:receipt'
        with self.assertRaises(ValueError):
            self.manage.validate_report(report)

    def test_empty_applicability_cannot_claim_workflow_completion(self):
        report = self.report_with_workflow()
        report['workflow']['steps'][0]['required'] = False
        report['workflow']['steps'][0]['status'] = 'not-applicable'
        with self.assertRaises(ValueError):
            self.manage.validate_report(report)

    def test_review_findings_require_explicit_disposition(self):
        report = self.report_with_workflow()
        report['review']['findings'] = [{'id': 'r1'}]
        with self.assertRaises(ValueError):
            self.manage.validate_report(report)

    def test_blocked_report_cannot_claim_independent_completion(self):
        self.manage.validate_report({'status': 'verification-blocked', 'baseline': 'abc', 'claims': []})
        with self.assertRaises(ValueError):
            self.manage.validate_report({'status': 'independently-checked', 'baseline': 'abc', 'claims': []})

class ReviewPacketTests(unittest.TestCase):
    setUp = PackageTests.setUp
    def packet_inputs(self):
        inputs = {}
        for role in ('brief', 'report', 'ledger', 'explanation', 'workflow', 'evidence-1'):
            path = self.workspace / (role + '.txt')
            path.write_bytes(role.encode() + b'\x00\xff\n')
            inputs[role] = path
        return inputs

    def test_packet_copies_bytes_and_survives_source_changes(self):
        inputs = self.packet_inputs()
        output = self.workspace / 'packet'
        receipt = self.manage.freeze_review_packet(output, inputs)
        manifest = json.loads((output / 'manifest.json').read_text())
        for role, source in inputs.items():
            self.assertEqual((output / manifest['files'][role]['filename']).read_bytes(), source.read_bytes())
            source.write_text('changed source')
        self.assertEqual(self.manage.check_review_packet(output)['packet_id'], receipt['packet_id'])
        self.assertEqual(receipt['scope'], 'content identity only; not dispatch or semantic proof')

    def test_packet_refuses_existing_destination(self):
        inputs = self.packet_inputs()
        output = self.workspace / 'packet'
        output.mkdir()
        (output / 'keep').write_text('owned elsewhere')
        with self.assertRaises((ValueError, OSError)):
            self.manage.freeze_review_packet(output, inputs)
        self.assertEqual((output / 'keep').read_text(), 'owned elsewhere')

    def test_packet_rejects_missing_roles_unsafe_roles_and_linked_inputs(self):
        inputs = self.packet_inputs()
        for bad in ({k: v for k, v in inputs.items() if k != 'brief'},
                    {**inputs, '../escape': inputs['brief']},
                    {**inputs, 'manifest': inputs['brief']}):
            with self.subTest(roles=list(bad)), self.assertRaises(ValueError):
                self.manage.freeze_review_packet(self.workspace / 'packet', bad)
        linked = self.workspace / 'link'
        linked.symlink_to(inputs['brief'])
        with self.assertRaises(ValueError):
            self.manage.freeze_review_packet(self.workspace / 'packet', {**inputs, 'brief': linked})
        self.assertFalse((self.workspace / 'packet').exists())

    def test_packet_detects_tampering_unexpected_files_and_links(self):
        inputs = self.packet_inputs()
        output = self.workspace / 'packet'
        self.manage.freeze_review_packet(output, inputs)
        manifest_path = output / 'manifest.json'
        original = manifest_path.read_bytes()
        manifest = json.loads(original)
        brief = output / manifest['files']['brief']['filename']
        contents = brief.read_bytes()
        brief.write_bytes(b'x' * len(contents))
        with self.assertRaises(ValueError):
            self.manage.check_review_packet(output)
        brief.write_bytes(contents)
        extra = output / 'extra'
        extra.write_text('extra')
        with self.assertRaises(ValueError):
            self.manage.check_review_packet(output)
        extra.unlink()
        brief.unlink()
        brief.symlink_to(inputs['brief'])
        with self.assertRaises(ValueError):
            self.manage.check_review_packet(output)
        brief.unlink()
        brief.write_bytes(contents)
        for mutation in ('identity', 'missing', 'path', 'schema'):
            broken = copy.deepcopy(manifest)
            if mutation == 'identity': broken['packet_id'] = '0' * 64
            if mutation == 'missing': del broken['files']['brief']
            if mutation == 'path': broken['files']['brief']['filename'] = '../brief.txt'
            if mutation == 'schema': broken['schema'] = True
            manifest_path.write_text(json.dumps(broken))
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.manage.check_review_packet(output)
        manifest_path.write_bytes(original)

    def test_packet_cli_roundtrip(self):
        import subprocess
        import sys
        inputs = self.packet_inputs()
        output = self.workspace / 'packet'
        command = [sys.executable, str(ROOT / 'scripts/manage.py'), 'create-review-packet', '--output', str(output)]
        for role, path in inputs.items():
            command.extend(['--evidence' if role == 'evidence-1' else '--' + role, str(path)])
        created = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(created.returncode, 0, created.stderr)
        checked = subprocess.run([sys.executable, str(ROOT / 'scripts/manage.py'), 'check-review-packet', str(output)], capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertEqual(json.loads(created.stdout)['packet_id'], json.loads(checked.stdout)['packet_id'])

if __name__ == '__main__':
    unittest.main()
