import sys
from pathlib import Path
import asyncio

RUNNER_DIR = Path("C:/testing/runner")
sys.path.insert(0, str(RUNNER_DIR))

import importlib
agent_runner = importlib.import_module("agent-runner")
from browser_use import Agent, BrowserSession
from langchain_core.language_models import FakeListChatModel

dummy_response = '''```json
{"current_state": {"evaluation_previous_goal": "Success", "memory": "test", "next_goal": "done"}, "action": [{"done": {"text": "Finished"}}]}
```'''
llm = FakeListChatModel(responses=[dummy_response])

async def test():
    print("Starting BrowserSession")
    session = BrowserSession(headless=True, keep_alive=True)
    await session.start()
    
    agent_runner.enable_observable_dom_serialization()

    task = {"instruction": "test", "id": "T1"}
    
    # We will test variant v1-jsonld
    agent = Agent(
        task=task["instruction"],
        llm=llm,
        browser_session=session,
        initial_actions=[{"navigate": {"url": "http://localhost:8080/variants/v1-jsonld/#home", "new_tab": False}}],
        include_attributes=agent_runner.OBSERVABLE_ATTRIBUTES,
    )

    # Patch it like the runner
    orig_create_state_messages = agent._message_manager.create_state_messages

    def wrapped_create_state_messages(*args, **kwargs):
        browser_state_summary = args[0] if len(args) > 0 else kwargs.get("browser_state_summary")
        step_info = args[3] if len(args) > 3 else kwargs.get("step_info")
        url = browser_state_summary.url if browser_state_summary else "unknown"
        step_number = step_info.step_number if step_info else -1

        pending = getattr(agent, "_pending_step_metadata", None)
        if pending:
            agent._message_manager.state.read_state_description = pending
            agent._pending_step_metadata = None

        actual_metadata = agent._message_manager.state.read_state_description
        
        result_val = orig_create_state_messages(*args, **kwargs)
        
        try:
            last_msg = agent._message_manager.get_messages()[-1]
            if hasattr(last_msg, 'content'):
                if isinstance(last_msg.content, list):
                    msg_text = " ".join([c.get("text", "") for c in last_msg.content if isinstance(c, dict) and "text" in c])
                else:
                    msg_text = str(last_msg.content)
            else:
                msg_text = str(last_msg)
        except Exception as e:
            msg_text = f"ERROR_EXTRACTING_PROMPT: {e}"

        print(f"--- INTERCEPTED STEP {step_number} ---")
        print(f"URL: {url}")
        print(f"Metadata provided: {bool(actual_metadata)}")
        print(f"Prompt length: {len(msg_text)}")
        print(f"JSON-LD in prompt? {'WebSite' in msg_text}")
        return result_val

    agent._message_manager.create_state_messages = wrapped_create_state_messages

    async def on_step_start_hook(curr_agent):
        try:
            page = await curr_agent.browser_session.get_current_page()
            meta_str = await agent_runner.extract_active_page_metadata(page)
            curr_agent._pending_step_metadata = meta_str
        except Exception:
            curr_agent._pending_step_metadata = None

    print("Running agent...")
    await agent.run(max_steps=2, on_step_start=on_step_start_hook)
    
    await session.stop()

if __name__ == "__main__":
    asyncio.run(test())
