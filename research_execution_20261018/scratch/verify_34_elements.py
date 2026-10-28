import asyncio
import sys
import json
from pathlib import Path
sys.path.insert(0, r"C:\testing\research_execution_20261018")
import compare_accessibility_tree as cat

async def run_audit():
    server = cat.start_server()
    try:
        url_path = "variants/v0-baseline/index.html#home"
        source_path = Path(r"C:\testing\variants\v0-baseline\index.html")
        print(f"Capturing representations for {url_path}...")
        
        # We can run session directly and inspect both ax_nodes and summary.dom_state.selector_map
        session = cat.BrowserSession(headless=True)
        await session.start()
        try:
            url = f"http://127.0.0.1:{cat.PORT}/{url_path}"
            await session.navigate_to(url)
            await asyncio.sleep(0.5)
            
            target_info = await session.get_current_target_info()
            tid = target_info.get("targetId") or target_info.get("target_id")
            cdp_session = await session.get_or_create_cdp_session(target_id=tid, focus=False)
            
            ax_response = await cdp_session.cdp_client.send.Accessibility.getFullAXTree(
                session_id=cdp_session.session_id
            )
            ax_nodes = ax_response.get("nodes", [])
            summary = await session.get_browser_state_summary()
            
            ax_by_bid = {n.get("backendDOMNodeId"): n for n in ax_nodes if "backendDOMNodeId" in n}
            selector_map = summary.dom_state.selector_map
            
            elements_data = []
            for sel_idx, elem in sorted(selector_map.items()):
                bid = elem.backend_node_id
                ax_node = ax_by_bid.get(bid)
                
                # Check text extraction method
                text_content = ""
                if hasattr(elem, "get_all_text_till_next_clickable_element"):
                    text_content = elem.get_all_text_till_next_clickable_element()
                elif hasattr(elem, "node_value"):
                    text_content = elem.node_value or ""
                    
                elements_data.append({
                    "selector_index": sel_idx,
                    "tag": elem.tag_name,
                    "backend_node_id": bid,
                    "text": text_content.strip()[:60] if text_content else "",
                    "classes": elem.attributes.get("class", "") if elem.attributes else "",
                    "attributes": elem.attributes or {},
                    "is_interactive": getattr(elem, "is_interactive", None),
                    "matched": ax_node is not None,
                    "ax_role": ax_node.get("role", {}).get("value") if ax_node else None,
                    "ax_name": ax_node.get("name", {}).get("value") if ax_node else None,
                    "ax_ignored": ax_node.get("ignored") if ax_node else None,
                })
                
            matched = [e for e in elements_data if e["matched"]]
            unmatched = [e for e in elements_data if not e["matched"]]
            
            print(f"\nTotal interactive elements in selector_map: {len(elements_data)}")
            print(f"Matched count: {len(matched)}")
            print(f"Unmatched count: {len(unmatched)}")
            
            print("\n=== ALL 34 ELEMENTS IN SELECTOR MAP ===")
            for i, e in enumerate(elements_data, 1):
                status = "MATCH" if e["matched"] else "UNMATCHED"
                print(f"{i:2d}. [{status:9s}] idx={e['selector_index']:3d} | tag={e['tag']:8s} | bid={e['backend_node_id']:3d} | ax_role={str(e['ax_role']):12s} | ax_name={str(e['ax_name'])[:20]:20s} | text='{e['text']}' | attrs={e['attributes']}")
                
            print("\n=== FORENSIC BREAKDOWN OF 7 UNMATCHED ELEMENTS ===")
            for i, u in enumerate(unmatched, 1):
                print(f"\nUnmatched #{i}:")
                print(f"  Selector Index: {u['selector_index']}")
                print(f"  Tag Name: {u['tag']}")
                print(f"  Backend Node ID: {u['backend_node_id']}")
                print(f"  Text Content: '{u['text']}'")
                print(f"  Classes: '{u['classes']}'")
                print(f"  Attributes: {u['attributes']}")
                
            # Save to JSON
            out_path = Path(r"C:\testing\research_execution_20261018\scratch\elements_audit.json")
            out_path.write_text(json.dumps(elements_data, indent=2), encoding="utf-8")
            print(f"\nSaved full elements audit to {out_path}")
            
        finally:
            await session.stop()
    finally:
        server.shutdown()

if __name__ == "__main__":
    asyncio.run(run_audit())
