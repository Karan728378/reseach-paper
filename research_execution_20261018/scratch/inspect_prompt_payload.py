import asyncio
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from browser_use import Agent, BrowserSession
from protocol_v3_runner import EXTENDED_ATTRIBUTES, ensure_server, TASK_INSTRUCTIONS

async def inspect_prompt():
    ensure_server(8080)
    session = BrowserSession(headless=True, viewport={"width": 1920, "height": 1080})
    await session.start()
    page = await session.get_current_page()
    await page.goto("http://127.0.0.1:8080/variants/v3-data-attrs/index.html#home")
    await asyncio.sleep(0.5)

    captured_payloads = []
    class DummyLLM:
        model = "openai/gpt-oss-120b"
        provider = "groq"
        name = "openai/gpt-oss-120b"
        async def ainvoke(self, messages, output_format=None, **kwargs):
            from browser_use.llm.openai.serializer import OpenAIMessageSerializer
            serialized = OpenAIMessageSerializer.serialize_messages(messages)
            captured_payloads.append((messages, serialized))
            raise RuntimeError("Halt after capturing first prompt")

    agent = Agent(
        task=TASK_INSTRUCTIONS["T2"],
        llm=DummyLLM(),
        browser_session=session,
        use_vision=False,
        include_attributes=EXTENDED_ATTRIBUTES,
        flash_mode=True
    )
    try:
        await agent.step()
    except RuntimeError:
        pass
    await session.stop()

    msgs, serialized = captured_payloads[0]
    print(f"Total messages: {len(serialized)}")
    total_chars = sum(len(json.dumps(m)) for m in serialized)
    print(f"Total serialized chars: {total_chars}")
    print(f"Estimated chars/4 tokens: {total_chars / 4:.0f}")
    for i, m in enumerate(serialized):
        content = m.get("content", "")
        role = m.get("role")
        c_len = len(content) if isinstance(content, str) else len(json.dumps(content))
        print(f"  Message {i} ({role}): {c_len} chars (~{c_len/4:.0f} tokens)")
        if c_len > 500:
            sample = content[:200] if isinstance(content, str) else str(content)[:200]
            print(f"    Sample: {sample}...")

if __name__ == "__main__":
    asyncio.run(inspect_prompt())
