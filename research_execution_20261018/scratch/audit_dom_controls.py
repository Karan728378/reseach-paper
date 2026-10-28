from bs4 import BeautifulSoup
from pathlib import Path
import json

WORKSPACE = Path("C:/testing")
html_path = WORKSPACE / "variants" / "v0-baseline" / "index.html"
html = html_path.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

print("=== STATIC CONTROLS IN index.html ===")
for tag in ["a", "button", "input", "select", "form"]:
    els = soup.find_all(tag)
    print(f"Tag <{tag}>: {len(els)}")
    for e in els:
        txt = e.get_text(strip=True)[:40]
        eid = e.get("id", "")
        ecls = " ".join(e.get("class", []))
        print(f"  <{tag} id='{eid}' class='{ecls}'>{txt}</{tag}>")

# Now inspect app-core.js and products.js to see what dynamically renders on #home
products_path = WORKSPACE / "shared" / "products.js"
prod_text = products_path.read_text(encoding="utf-8")
# Count products
# products are defined in window.PRODUCTS = [...]
import re
products = re.findall(r'id:\s*[\'"]([^\'"]+)[\'"]', prod_text)
print(f"\nTotal products defined in products.js: {len(products)} -> {products}")

# On #home, renderHomeView() renders featured products.
# Let's see what renderHomeView() renders:
app_core = (WORKSPACE / "shared" / "app-core.js").read_text(encoding="utf-8")
for line in app_core.splitlines():
    if "function renderHomeView" in line or "function renderFeatured" in line:
        print("Found home render function:", line)

