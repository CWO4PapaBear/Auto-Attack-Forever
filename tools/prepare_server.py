#!/usr/bin/env python3
"""Check the supported core; optionally apply the integration patch. Never restarts services."""
import argparse, hashlib, json, subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--core', required=True, type=Path)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    module = Path(__file__).resolve().parents[1]
    core = args.core.resolve()
    if module != core / 'modules/mod-adaptive-autoattack':
        parser.error('Place this package in CORE/modules/mod-adaptive-autoattack first.')
    if (core / 'modules/mod-ranged-autoattack').exists():
        parser.error('Conflicting experimental module is present; migrate separately.')
    baseline = json.loads((module / 'patches/baseline.json').read_text())
    revision = subprocess.check_output(['git', '-C', str(core), 'rev-parse', 'HEAD'], text=True).strip()
    if revision != baseline['revision']:
        parser.error('Unsupported core revision: ' + revision)
    for relative, expected in baseline['normalized_sha256'].items():
        data = (core / relative).read_bytes().replace(b'\r\n', b'\n')
        if hashlib.sha256(data).hexdigest() != expected:
            parser.error('Core file differs from reviewed baseline: ' + relative)
    patch = module / 'patches/azerothcore-e1823bb.patch'
    subprocess.run(['git', '-C', str(core), 'apply', '--check', str(patch)], check=True)
    print('PASS: supported revision, unchanged integration files and applicable patch.')
    if args.apply:
        subprocess.run(['git', '-C', str(core), 'apply', str(patch)], check=True)
        print('Patch applied. Build, database checks, configuration and client installation remain.')
    else:
        print('Read-only check complete. Use --apply after creating your backups.')
if __name__ == '__main__':
    main()
