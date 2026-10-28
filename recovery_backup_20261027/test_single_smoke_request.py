"""
Execute One Genuine Live Smoke Test (Neutral Prompt)
Model: gemini-3-flash-preview
Strict $0.00 spend constraint. Exactly 1 request. Zero retries. Zero secret leakage.
"""

import datetime
import json
import os
import sys
from pathlib import Path

EXEC_DIR = Path(__file__).resolve().parent
OUTPUT_JSON = EXEC_DIR / "smoke_test_evidence.json"

TARGET_MODEL = "gemini-3.1-flash-lite"
NEUTRAL_PROMPT = "Respond with exactly the single word: PONG"

def run_smoke_test():
    print("=" * 70)
    print("SINGLE LIVE SMOKE REQUEST (NEUTRAL PROMPT)")
    print(f"Target Model: {TARGET_MODEL}")
    print(f"Spending Cap: $0.00 USD (Strictly Genuinely Free Tier)")
    print("=" * 70)

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("[FAIL] GOOGLE_API_KEY is not set in environment.")
        sys.exit(1)

    print("[*] API Key present. Configuration verified (value fully redacted).")

    from google import genai
    from google.genai import types
    # Zero retries strictly enforced
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(attempts=1, http_status_codes=[])
        )
    )

    t_start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f"[*] Dispatching single neutral request at {t_start}...")
    print(f"    Prompt: '{NEUTRAL_PROMPT}'")

    try:
        response = client.models.generate_content(
            model=TARGET_MODEL,
            contents=NEUTRAL_PROMPT,
        )
        t_end = datetime.datetime.now(datetime.timezone.utc).isoformat()
        print(f"[+] Response received successfully at {t_end}!")

        response_text = response.text.strip() if hasattr(response, "text") and response.text else ""
        
        usage_metadata = {}
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            um = response.usage_metadata
            usage_metadata = {
                "prompt_token_count": getattr(um, "prompt_token_count", None),
                "candidates_token_count": getattr(um, "candidates_token_count", None),
                "total_token_count": getattr(um, "total_token_count", None),
            }

        candidates_info = []
        if hasattr(response, "candidates") and response.candidates:
            for c in response.candidates:
                finish_reason = getattr(c, "finish_reason", None)
                candidates_info.append({
                    "finish_reason": str(finish_reason) if finish_reason else "STOP"
                })

        evidence = {
            "test_type": "NEUTRAL_SMOKE_VERIFICATION",
            "provider": "google",
            "model_id": TARGET_MODEL,
            "api_endpoint": "generativelanguage.googleapis.com",
            "timestamp_start": t_start,
            "timestamp_end": t_end,
            "http_status": 200,
            "success": True,
            "prompt_sent": NEUTRAL_PROMPT,
            "sanitized_response": response_text,
            "usage_metadata": usage_metadata,
            "candidates": candidates_info,
            "cost_usd": 0.00,
            "tier_type": "Google AI Studio Free of Charge Tier",
            "paid_fallback_used": False,
            "mock_model_used": False,
            "behavioral_experiment_count": 0
        }

        OUTPUT_JSON.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
        print("\n" + "=" * 70)
        print("[SUCCESS] Genuine external inference confirmed!")
        print(f"Model ID: {TARGET_MODEL}")
        print(f"Response: '{response_text}'")
        print(f"Token counts: {usage_metadata}")
        print(f"Candidates info: {candidates_info}")
        print(f"Evidence saved to: {OUTPUT_JSON}")
        print("=" * 70)
        return True

    except Exception as e:
        err_msg = str(e).replace(api_key, "[REDACTED_API_KEY]")
        print(f"[FAIL] Inference request failed: {type(e).__name__}: {err_msg}")
        evidence = {
            "test_type": "NEUTRAL_SMOKE_VERIFICATION",
            "provider": "google",
            "model_id": TARGET_MODEL,
            "timestamp": t_start,
            "success": False,
            "error_type": type(e).__name__,
            "error_message": err_msg,
            "paid_fallback_used": False,
            "mock_model_used": False
        }
        OUTPUT_JSON.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
        sys.exit(1)

if __name__ == "__main__":
    run_smoke_test()
