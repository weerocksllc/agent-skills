#!/usr/bin/env python3
"""Check distributable file hashes, resource links and runtime version metadata."""
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
manifests = sorted((root / 'manifests').glob('*.json'))
assert manifests, 'No published skill manifests'
total = 0
for manifest in manifests:
    data = json.loads(manifest.read_text())
    name = data['skill']
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) and len(name) <= 64
    skill = root / 'skills' / name
    expected = set()
    for entry in data['files']:
        file = root / entry['path']
        assert '..' not in Path(entry['path']).parts and not Path(entry['path']).is_absolute()
        assert not file.is_symlink() and file.resolve().is_relative_to(skill.resolve())
        body = file.read_bytes()
        assert len(body) == entry['bytes'] and hashlib.sha256(body).hexdigest() == entry['sha256'], entry['path']
        expected.add(file.resolve())
        if file.suffix == '.md':
            for link in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', body.decode()):
                target = link.split('#', 1)[0]
                if not target or re.match(r'^[a-z][a-z0-9+.-]*:', target, re.I):
                    continue
                resource = (file.parent / target).resolve()
                assert resource.is_relative_to(skill.resolve()) and resource.is_file(), (file, link)
        total += 1
    actual = {p.resolve() for p in skill.rglob('*') if p.is_file()}
    assert actual == expected, f'Unexpected or missing distributable files in {name}'
    text = (skill / 'SKILL.md').read_text()
    assert text.startswith('---\n') and f'\nname: {name}\n' in text
    assert re.search(r'^description: .+', text, re.M)
    assert f'product-version: "{data["release"]["version"]}"' in text
    assert f'product-build: "{data["release"]["build"]}"' in text
    assert len(text.splitlines()) < 500
print(f'Validated {len(manifests)} skill(s), {total} public files; no program installed or remote session opened.')
