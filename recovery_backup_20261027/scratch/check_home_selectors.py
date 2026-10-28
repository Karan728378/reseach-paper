import json
from pathlib import Path

p = Path("accessibility_tree_comparison.json")
d = json.loads(p.read_text(encoding="utf-8"))
nc = d["node_level_correspondence"]

# Check v0_baseline or v2_aria
for vname in ["v0_baseline", "v2_aria"]:
    if vname in nc:
        print(f"=== {vname} ===")
        sample = nc[vname].get("matched_sample", [])
        print(f"matched_sample length: {len(sample)}")
        for s in sample:
            print(" ", s.get("selector_index"), s.get("tag"), s.get("dom_attributes"), s.get("ax_role"), s.get("ax_name"))

# Check where the 34 selectors on #home are listed
# Let's check live single attempt trace or multi_route_observation_audit.json
p_multi = Path("local_closure_results/multi_route_observation_audit.json")
if p_multi.exists():
    d_multi = json.loads(p_multi.read_text(encoding="utf-8"))
    home = d_multi["multi_route_census"]["route_home"]
    print("\n=== multi_route_census route_home ===")
    print("total_selector_elements:", home.get("total_selector_elements"))
    print("matched_selector_elements:", home.get("matched_selector_elements"))
    print("unmatched_selector_elements:", home.get("unmatched_selector_elements"))
    print("total_semantic_controls:", home.get("total_semantic_controls"))
    print("unmatched_details:", home.get("unmatched_details"))

