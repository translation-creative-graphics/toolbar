#!/usr/bin/env python3
"""Build Toolbar module language pack ZIPs — one per locale.

Each ZIP contains just the single {locale}.mod_stackideas_toolbar.ini file,
ready to be fetched and copied directly into
pkg_toolbar/packages/mod_stackideas_toolbar/ by each CRE8 component's own
language installer. No Joomla installer manifest needed — these are not
installed through Joomla's Extension Manager, only fetched programmatically.
"""

import re
import zipfile
from pathlib import Path

DIST = Path('dist')
DIST.mkdir(exist_ok=True)

locales = sorted([
    d.name for d in Path('language').iterdir()
    if d.is_dir()
    and d.name != 'en-GB'
    and re.match(r'^[a-z]{2}-[A-Za-z]{2,3}$', d.name)
])

for locale in locales:
    src = Path('language') / locale / f'{locale}.mod_stackideas_toolbar.ini'
    if not src.exists():
        print(f'Skipping {locale}: no ini file found')
        continue

    zip_path = DIST / f'mod_stackideas_toolbar_{locale}.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(src, src.name)

    print(f'Built {zip_path.name}  ({zip_path.stat().st_size:,} bytes)')

print(f'\nTotal: {len(locales)} language packs')
