import urllib.request, json
url = 'https://pypi.org/pypi/browser-use/json'
req = urllib.request.Request(url, headers={'User-Agent': 'ResearchAuditor/1.0'})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode())
for v in ['0.1.0', '0.5.0', '0.13.0', '0.13.5', '0.13.10', '0.13.11']:
    files = data['releases'][v]
    for f in files:
        if f['filename'].endswith('.whl'):
            print(f"{v}: {f['filename']} -> {f['digests']['sha256']}")
