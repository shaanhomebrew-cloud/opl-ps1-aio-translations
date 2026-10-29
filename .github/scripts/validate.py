import json, re, sys, pathlib

root = pathlib.Path('.').resolve()
en_path = root / 'en-US.json'

if not en_path.exists():
    print('FAIL: en-US.json missing')
    sys.exit(1)

try:
    en = json.loads(en_path.read_text(encoding='utf-8'))
except Exception as e:
    print(f'FAIL: en-US.json invalid — {e}')
    sys.exit(1)

en_keys = {k for k in en if not k.startswith('_meta.')}
errors = []
warnings = []

def placeholders(s):
    return sorted(re.findall(r'\{\d+\}', s or ''))

for f in sorted(root.glob('*.json')):
    if f.name in ('manifest.json', 'en-US.json'):
        continue

    try:
        data = json.loads(f.read_text(encoding='utf-8'))
    except Exception as e:
        errors.append(f'{f.name}: invalid JSON — {e}')
        continue

    keys = {k for k in data if not k.startswith('_meta.')}

    for k in sorted(en_keys - keys):
        errors.append(f'{f.name}: missing key {k}')
    for k in sorted(keys - en_keys):
        errors.append(f'{f.name}: unexpected key {k}')

    for k in sorted(en_keys & keys):
        pe, pt = placeholders(en[k]), placeholders(data[k])
        if pe != pt:
            errors.append(f'{f.name}: placeholder mismatch in {k} (en={pe}, tr={pt})')

    untouched = [k for k in (en_keys & keys) if data[k] == en[k]]
    if untouched:
        warnings.append(f'{f.name}: {len(untouched)} key(s) identical to English')

if warnings:
    print('WARNINGS:')
    for w in warnings:
        print('  ' + w)
    print()

if errors:
    print(f'{len(errors)} error(s):')
    for e in errors:
        print('  ' + e)
    sys.exit(1)

print(f'✅ All checks passed. {len(en_keys)} canonical keys across {len(list(root.glob("*.json")))-2} translation files.')
