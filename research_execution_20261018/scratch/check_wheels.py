import urllib.request
import json
import os
import zipfile
import hashlib

os.makedirs('scratch/wheels', exist_ok=True)
url = 'https://pypi.org/pypi/browser-use/json'
req = urllib.request.Request(url, headers={'User-Agent': 'ResearchAuditor/1.0'})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode())

test_versions = ['0.1.0', '0.5.0', '0.13.0', '0.13.5', '0.13.10', '0.13.11']
for ver in test_versions:
    files = data['releases'].get(ver, [])
    whl_files = [f for f in files if f['filename'].endswith('.whl')]
    tar_files = [f for f in files if f['filename'].endswith('.tar.gz')]
    target = whl_files[0] if whl_files else (tar_files[0] if tar_files else None)
    if target:
        fn = target['filename']
        sz = target['size']
        h = target['digests']['sha256']
        print(f"{ver}: {fn}, size={sz}, sha256={h[:16]}..., url={target['url']}")
