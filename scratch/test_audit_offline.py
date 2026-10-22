import sys
from pathlib import Path
import json
import datetime
import os
import re

RUNNER_DIR = Path("C:/testing/runner")
sys.path.insert(0, str(RUNNER_DIR))

import importlib
agent_runner = importlib.import_module("agent-runner")
from browser_use import Agent
from unittest.mock import MagicMock
from langchain_core.language_models import FakeListChatModel
from pydantic import BaseModel

def run_tests():
    print("Running audit logging offline tests...")
    
    agent_runner.enable_observable_dom_serialization()
    
    log_file = agent_runner.DEFAULT_RESULTS_DIR / "audit-logs" / "test_audit_123.jsonl"
    if log_file.exists():
        log_file.unlink()
    
    # Mock LLM and Agent
    FakeListChatModel.provider = "google"
    FakeListChatModel.model = "test-model"
    llm = FakeListChatModel(responses=[""])
    agent = Agent(task="dummy", llm=llm)
    
    # We will test the monkey patch on agent
    orig_prepare_step_state = agent._message_manager.prepare_step_state
    def wrapped_prepare_step_state(*args, **kwargs):
        orig_prepare_step_state(*args, **kwargs)
        pending = getattr(agent, "_pending_step_metadata", None)
        if pending:
            agent._message_manager.state.read_state_description = pending
            agent._pending_step_metadata = None
    agent._message_manager.prepare_step_state = wrapped_prepare_step_state

    orig_create_state_messages = agent._message_manager.create_state_messages
    def wrapped_create_state_messages(*args, **kwargs):
        browser_state_summary = args[0] if len(args) > 0 else kwargs.get("browser_state_summary")
        step_info = args[3] if len(args) > 3 else kwargs.get("step_info")
        url = browser_state_summary.url if browser_state_summary else "unknown"
        step_number = getattr(step_info, 'step_number', -1) if step_info else -1
        
        result_val = orig_create_state_messages(*args, **kwargs)
        actual_metadata = agent._message_manager.state.read_state_description
        
        try:
            last_msg = agent._message_manager.get_messages()[-1]
            if hasattr(last_msg, 'content'):
                if isinstance(last_msg.content, list):
                    parts = []
                    for c in last_msg.content:
                        if hasattr(c, 'text') and isinstance(c.text, str):
                            parts.append(c.text)
                        elif isinstance(c, dict) and 'text' in c:
                            parts.append(c['text'])
                    msg_text = " ".join(parts)
                else:
                    msg_text = str(last_msg.content)
            else:
                msg_text = str(last_msg)
        except Exception:
            msg_text = "ERROR_EXTRACTING_PROMPT"

        # Separate the treatment channels
        read_state_match = re.search(r'<read_state>\n(.*?)\n</read_state>', msg_text, re.DOTALL)
        read_state_metadata = read_state_match.group(1).strip() if read_state_match else "EMPTY"
        
        browser_state_match = re.search(r'<browser_state>\n(.*?)\n</browser_state>', msg_text, re.DOTALL)
        serialized_dom = browser_state_match.group(1).strip() if browser_state_match else "EMPTY"
        
        metadata_supplied_to_model = {
            "has_read_state": read_state_metadata != "EMPTY",
            "has_dom": serialized_dom != "EMPTY",
            "dom_length": len(serialized_dom) if serialized_dom != "EMPTY" else 0
        }

        audit_record = {
            "run_id": "test_audit_123",
            "variant": "offline-test",
            "task_id": "T1",
            "step_number": step_number,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "url": url,
            "read_state_metadata": read_state_metadata,
            "serialized_dom": serialized_dom,
            "metadata_supplied_to_model": metadata_supplied_to_model,
            "full_model_prompt": msg_text
        }

        audit_dir = agent_runner.DEFAULT_RESULTS_DIR / "audit-logs"
        audit_dir.mkdir(parents=True, exist_ok=True)
        audit_file = audit_dir / f"test_audit_123.jsonl"
        
        clean_record_str = agent_runner.sanitize_secret_leakage(json.dumps(audit_record, ensure_ascii=False))
        
        with open(audit_file, "a", encoding="utf-8") as f:
            f.write(clean_record_str + "\n")

        return result_val

    agent._message_manager.create_state_messages = wrapped_create_state_messages

    # Create dummy browser state
    def make_browser_state(url, dom_content):
        dummy_browser_state = MagicMock()
        dummy_browser_state.url = url
        # Setting a screenshot triggers multimodal vision payload (list of ContentPartTextParam) in browser-use 0.13.10
        dummy_browser_state.screenshot = "dummy_screenshot_data"
        dummy_browser_state.interacted_element = None
        dummy_browser_state.page_info = MagicMock()
        dummy_browser_state.page_info.viewport_height = 800
        dummy_browser_state.page_info.pixels_above = 0
        dummy_browser_state.page_info.pixels_below = 0
        
        dummy_dom = MagicMock()
        dummy_dom.llm_representation.return_value = dom_content
        dummy_browser_state.dom_state = dummy_dom
        return dummy_browser_state
        
    class DummyStepInfo(BaseModel):
        step_number: int
        max_steps: int

    def read_records():
        with open(log_file, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f.readlines()]

    # 1. Test Baseline (v0)
    agent._pending_step_metadata = None
    step_info = DummyStepInfo(step_number=1, max_steps=30)
    bs0 = make_browser_state("http://localhost:8080/variants/v0-baseline/#home", "<div>baseline content</div>")
    agent._message_manager.create_state_messages(browser_state_summary=bs0, step_info=step_info)
    
    r0 = read_records()[0]
    assert r0["read_state_metadata"] == "EMPTY"
    assert "baseline content" in r0["serialized_dom"]
    assert "data-test" not in r0["serialized_dom"]
    print("✓ Baseline (v0) validation successful.")

    # 2. Test JSON-LD (v1)
    agent._pending_step_metadata = "{'@type': 'WebSite', 'name': 'Test'}"
    step_info.step_number = 2
    bs1 = make_browser_state("http://localhost:8080/variants/v1-jsonld/#home", "<div>v1 content</div>")
    agent._message_manager.create_state_messages(browser_state_summary=bs1, step_info=step_info)
    
    r1 = read_records()[1]
    assert "WebSite" in r1["read_state_metadata"]
    assert r1["metadata_supplied_to_model"]["has_read_state"] == True
    print("✓ JSON-LD (v1) validation successful.")

    # 3. Test ARIA (v2)
    agent._pending_step_metadata = None
    step_info.step_number = 3
    bs2 = make_browser_state("http://localhost:8080/variants/v2-aria/#home", "<div aria-label='v2 button'></div>")
    agent._message_manager.create_state_messages(browser_state_summary=bs2, step_info=step_info)
    
    r2 = read_records()[2]
    assert r2["read_state_metadata"] == "EMPTY"
    assert "aria-label='v2 button'" in r2["serialized_dom"]
    print("✓ ARIA (v2) validation successful.")

    # 4. Test data-* (v3)
    agent._pending_step_metadata = None
    step_info.step_number = 4
    bs3 = make_browser_state("http://localhost:8080/variants/v3-data-attrs/#home", "<div data-test='v3 val'></div>")
    agent._message_manager.create_state_messages(browser_state_summary=bs3, step_info=step_info)
    
    r3 = read_records()[3]
    assert r3["read_state_metadata"] == "EMPTY"
    assert "data-test='v3 val'" in r3["serialized_dom"]
    print("✓ data-* (v3) validation successful.")

    # 5. Test Metadata/Evidence (v4)
    agent._pending_step_metadata = "evidence: true"
    step_info.step_number = 5
    bs4 = make_browser_state("http://localhost:8080/variants/v4-evidence-meta/#home", "<div>v4 content</div>")
    agent._message_manager.create_state_messages(browser_state_summary=bs4, step_info=step_info)
    
    r4 = read_records()[4]
    assert "evidence: true" in r4["read_state_metadata"]
    print("✓ Evidence/Temporal Metadata (v4) validation successful.")

    # 6. Test SPA Refresh
    agent._pending_step_metadata = "{'@type': 'Product', 'name': 'New Product'}"
    step_info.step_number = 6
    bs_spa = make_browser_state("http://localhost:8080/variants/v1-jsonld/#product/123", "<div>Product 123</div>")
    agent._message_manager.create_state_messages(browser_state_summary=bs_spa, step_info=step_info)
    
    r_spa = read_records()[5]
    assert r_spa["url"] == "http://localhost:8080/variants/v1-jsonld/#product/123"
    assert "New Product" in r_spa["read_state_metadata"]
    assert "Product 123" in r_spa["serialized_dom"]
    print("✓ SPA Refresh and alignment validation successful.")

    # 7. Test Secret Sanitization
    agent._pending_step_metadata = "key: AIzaSyB1234567890abcdefghijklmnopqrstuv valid_data: here"
    step_info.step_number = 7
    bs_sec = make_browser_state("http://localhost:8080/test", "<div>DOM</div>")
    agent._message_manager.create_state_messages(browser_state_summary=bs_sec, step_info=step_info)
    
    r_sec = read_records()[6]
    assert "AIzaSy" not in r_sec["read_state_metadata"]
    assert "[REDACTED_API_KEY]" in r_sec["read_state_metadata"]
    assert "valid_data: here" in r_sec["read_state_metadata"]
    print("✓ Audit log secret redaction and preservation successful.")
    
    # Clean up test file
    if log_file.exists():
        log_file.unlink()
        
    print("All offline audit logging tests passed.")

if __name__ == "__main__":
    run_tests()
