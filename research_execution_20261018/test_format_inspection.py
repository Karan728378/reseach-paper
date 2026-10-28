import asyncio
from browser_use import BrowserSession
from browser_use.dom.service import DomService

html = '<html><body><button id="btn1" aria-label="Add SoundFlow Air 3 to cart" data-action="add-to-cart">Click Me</button></body></html>'

async def check_format():
    session = BrowserSession(headless=True)
    await session.start()
    page = await session.get_current_page()
    await page.set_content(html)
    dom_service = DomService(session)
    state = await dom_service.get_clickable_elements()
    print("Selector map elements count:", len(state.selector_map))
    for idx, node in state.selector_map.items():
        print(f"Node {idx}:")
        print(f"  tag: {node.tag_name}")
        print(f"  attributes: {node.attributes}")
    if hasattr(state, "element_tree"):
        llm_repr = state.element_tree.llm_representation()
        print("Element tree llm_representation:")
        print(repr(llm_repr))
        print("Decoded:")
        print(llm_repr)
    await session.stop()

if __name__ == "__main__":
    asyncio.run(check_format())
