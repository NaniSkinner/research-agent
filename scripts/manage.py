#!/usr/bin/env python3
"""Stage project-scoped research resources; never change global Codex configuration."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tomllib


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def paths(workspace):
    workspace = Path(workspace).expanduser().resolve(strict=True)
    return workspace, workspace / '.agents/skills/project-research', workspace / '.codex/agents/project-researcher.toml', workspace / '.research-agent-installation.json'


def safe_parents(workspace, target):
    for parent in target.relative_to(workspace).parents:
        part = workspace / parent
        if part.is_symlink():
            raise ValueError(f'Registration parent is a symlink: {part}')


def profile_text(source):
    skill = source / 'project-research'
    instructions = (
        'You are the dedicated project-researcher. Read ' + str(skill / 'SKILL.md') +
        ' and its supporting resources before work. The canonical mandatory contract follows. '
        'Use live caller inputs, not project-specific defaults.\n\n' +
        (skill / 'references/contract.md').read_text()
    )
    return ('name = "project-researcher"\n'
            'description = "Brownfield factual researcher for broad project context and focused investigation supporting ongoing development. Not a builder or plan approver."\n'
            'developer_instructions = ' + json.dumps(instructions, ensure_ascii=False) + '\n\n'
            '[features]\nmemories = false\n')


def package_files(source):
    package = source / 'project-research'
    entries = [package, *package.rglob('*')]
    if any(p.is_symlink() or not p.resolve().is_relative_to(source) for p in entries):
        raise ValueError('Source package contains unsafe links')
    return {str(p.relative_to(source)): digest(p) for p in entries if p.is_file()}


def stage(source, workspace):
    source = Path(source).expanduser().resolve(strict=True)
    workspace, skill, profile, receipt_path = paths(workspace)
    if workspace == source or workspace.is_relative_to(source) or source.is_relative_to(workspace):
        raise ValueError('Use a separate workspace outside the source checkout')
    for path in (skill, profile, receipt_path):
        safe_parents(workspace, path)
        if path.exists() or path.is_symlink():
            raise ValueError(f'Refusing existing registration: {path}')
    package = source / 'project-research'
    manifest = package_files(source)
    if not (package / 'SKILL.md').is_file() or not (package / 'references/contract.md').is_file():
        raise ValueError('Incomplete source package')
    generated = profile_text(source)
    tomllib.loads(generated)
    receipt = {'schema': 1, 'source': str(source), 'workspace': str(workspace),
               'contract_sha256': digest(package / 'references/contract.md'),
               'profile_sha256': hashlib.sha256(generated.encode()).hexdigest(),
               'package_files': manifest,
               'desktop_dispatch': 'not-verified', 'behavioral_acceptance': 'not-run'}
    created = []
    try:
        skill.parent.mkdir(parents=True, exist_ok=True)
        profile.parent.mkdir(parents=True, exist_ok=True)
        skill.symlink_to(package, target_is_directory=True)
        created.append(skill)
        with profile.open('x') as stream:
            created.append(profile)
            stream.write(generated)
        with receipt_path.open('x') as stream:
            created.append(receipt_path)
            stream.write(json.dumps(receipt, indent=2) + '\n')
    except (OSError, ValueError):
        for path in reversed(created):
            path.unlink()
        raise
    return receipt


def owned_registration(workspace):
    workspace, skill, profile, receipt_path = paths(workspace)
    for path in (skill, profile, receipt_path):
        safe_parents(workspace, path)
    if receipt_path.is_symlink() or profile.is_symlink():
        raise ValueError('Unexpected linked receipt/profile')
    receipt = json.loads(receipt_path.read_text())
    if receipt.get('schema') != 1 or receipt.get('workspace') != str(workspace):
        raise ValueError('Invalid registration receipt')
    source = Path(receipt['source']).resolve()
    if not skill.is_symlink() or skill.resolve() != source / 'project-research':
        raise ValueError('Skill ownership changed')
    if digest(profile) != receipt['profile_sha256']:
        raise ValueError('Installed profile changed outside this registration')
    return receipt


def check(workspace):
    receipt = owned_registration(workspace)
    _, _, profile, _ = paths(workspace)
    source = Path(receipt['source']).resolve(strict=True)
    if package_files(source) != receipt['package_files'] or digest(source / 'project-research/references/contract.md') != receipt['contract_sha256']:
        raise ValueError('Package changed; reconcile and restage deliberately')
    if profile.read_text() != profile_text(source):
        raise ValueError('Profile/contract mismatch')
    return receipt


def remove(workspace):
    receipt = owned_registration(workspace)
    _, skill, profile, receipt_path = paths(workspace)
    for path in (skill, profile, receipt_path):
        path.unlink()
    return {'removed': True, 'workspace': receipt['workspace']}


def doctor(pstack, evidence):
    pstack = Path(pstack).expanduser().resolve()
    evidence = Path(evidence).expanduser()
    required = ['poteto-mode/SKILL.md', 'poteto-mode/references/codex-agent-runtime.md',
                'poteto-mode/references/poteto-agent-prompt.md', 'poteto-mode/playbooks/investigation.md',
                'how/SKILL.md', 'principle-prove-it-works/SKILL.md']
    resources = [pstack / item for item in required] + [evidence]
    missing = [str(p) for p in resources if not p.is_file()]
    if missing:
        raise ValueError('Missing required resources: ' + ', '.join(missing))
    return {'resources': {str(p.resolve()): digest(p) for p in resources},
            'scope': 'file availability and identity only; not reading, skill compliance or behavioral proof'}


def validate_report(report):
    """Check declared structure, never semantic truth or actual runtime metadata."""
    statuses = {'independently-checked', 'verification-blocked', 'needs-clarification'}
    if report.get('status') not in statuses or not isinstance(report.get('baseline'), str) or not report['baseline'].strip():
        raise ValueError('Missing status or baseline')
    claims = report.get('claims')
    if not isinstance(claims, list):
        raise ValueError('Claims must be a list')
    categories = {'observed-current-fact', 'historical-record', 'external-evidence', 'reported-not-reverified', 'inference', 'unknown'}
    ids = []
    for claim in claims:
        if not isinstance(claim, dict) or not claim.get('id') or claim.get('status') not in {'supported', 'contradicted', 'unverified'} or claim.get('category') not in categories or not claim.get('source'):
            raise ValueError('Claim lacks identity, classification, source or status')
        ids.append(claim['id'])
    if len(set(ids)) != len(ids):
        raise ValueError('Duplicate claim ids')
    if report['status'] != 'independently-checked':
        return
    review = report.get('review', {})
    if not review.get('reviewer_id') or review.get('fork_turns') != 'none' or review.get('baseline') != report['baseline']:
        raise ValueError('Missing fresh reviewer identity/context or matching baseline')
    checked = review.get('checked_claims')
    if not isinstance(checked, list) or set(checked) != set(ids):
        raise ValueError('Review coverage does not match claims')
    findings, dispositions = review.get('findings'), review.get('dispositions')
    if not isinstance(findings, list) or not isinstance(dispositions, list):
        raise ValueError('Missing review findings/dispositions')
    finding_ids = [item.get('id') for item in findings]
    handled = [item.get('finding_id') for item in dispositions if item.get('resolution') in {'corrected', 'rejected-with-evidence', 'unresolved'} and item.get('evidence')]
    if None in finding_ids or len(set(finding_ids)) != len(finding_ids) or set(finding_ids) != set(handled) or len(handled) != len(dispositions):
        raise ValueError('Review findings require explicit evidenced dispositions')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('stage', 'check', 'remove'):
        command = sub.add_parser(name)
        command.add_argument('--workspace', type=Path, required=True)
        if name == 'stage':
            command.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1])
    command = sub.add_parser('doctor')
    command.add_argument('--pstack-skills', type=Path, required=True)
    command.add_argument('--evidence-first', type=Path, required=True)
    command = sub.add_parser('validate-report')
    command.add_argument('report', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'stage':
            result = stage(args.source, args.workspace)
        elif args.command in ('check', 'remove'):
            result = globals()[args.command](args.workspace)
        elif args.command == 'doctor':
            result = doctor(args.pstack_skills, args.evidence_first)
        else:
            validate_report(json.loads(args.report.read_text()))
            result = {'structurally_valid': True, 'semantic_truth': 'not-established'}
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
