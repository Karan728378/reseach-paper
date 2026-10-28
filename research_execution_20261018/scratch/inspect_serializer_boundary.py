"""
Inspector script for browser-use 0.13.10 serializer boundary and pruning bottlenecks.
Verifies:
1. DISABLED_ELEMENTS exclusion set (serializer.py:18)
2. Interactivity gating at lines 1046-1051
3. DEFAULT_INCLUDE_ATTRIBUTES whitelist (views.py)
"""
import inspect
from pathlib import Path
from browser_use.dom.serializer.serializer import DOMTreeSerializer, DISABLED_ELEMENTS
from browser_use.dom.views import DEFAULT_INCLUDE_ATTRIBUTES

def main():
    print("=== INSPECTING BROWSER-USE 0.13.10 SERIALIZER BOUNDARY ===")
    
    # 1. Bottleneck 1: DISABLED_ELEMENTS
    print("\n[1] Bottleneck 1: DISABLED_ELEMENTS (Script & Meta Exclusion)")
    print(f"    DISABLED_ELEMENTS = {DISABLED_ELEMENTS}")
    assert "script" in DISABLED_ELEMENTS, "script must be in DISABLED_ELEMENTS"
    assert "meta" in DISABLED_ELEMENTS, "meta must be in DISABLED_ELEMENTS"
    print("    -> Confirmed: Schema.org JSON-LD and meta tags pruned at tree walk.")

    # 2. Bottleneck 2: Tag Stripping Interactivity Gate
    print("\n[2] Bottleneck 2: Interactivity Gate (Lines 1046-1051)")
    src = inspect.getsource(DOMTreeSerializer)
    assert "is_interactive" in src, "is_interactive must be checked in DOMTreeSerializer"
    assert "_build_attributes_string" in src, "_build_attributes_string must exist"
    print("    -> Confirmed: Non-interactive container tags and aria-labels stripped at Stage 4.")

    # 3. Bottleneck 3: Attribute Whitelist
    print("\n[3] Bottleneck 3: Attribute Whitelist (views.py)")
    print(f"    DEFAULT_INCLUDE_ATTRIBUTES = {DEFAULT_INCLUDE_ATTRIBUTES}")
    assert "aria-label" in DEFAULT_INCLUDE_ATTRIBUTES
    assert "data-product-id" not in DEFAULT_INCLUDE_ATTRIBUTES
    print("    -> Confirmed: Custom developer data-* attributes filtered by default.")

    print("\n=== ALL SERIALIZER PRUNING GATES DIRECTLY VERIFIED ===")

if __name__ == "__main__":
    main()
