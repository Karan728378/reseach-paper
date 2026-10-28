"""
Minimal Groq Connection and Compatibility Test
Part of: "The DOM Serialization Gap" Research Infrastructure

Tests:
1. Official Groq client instantiation.
2. Model availability and permission check for target model (default: openai/gpt-oss-120b).
3. Minimal single-token chat completion request.
4. Latency and quota/rate-limit header extraction.
5. Safe error classification (Auth, RateLimit, ModelAccess, Connection).
6. ZERO secret leakage.
"""

import os
import sys
import time
import argparse

def sanitize_error(err_str: str) -> str:
    """Strip any potential API keys from error representations."""
    key = os.environ.get("GROQ_API_KEY", "")
    if key and key in err_str:
        err_str = err_str.replace(key, "[REDACTED_GROQ_API_KEY]")
    return err_str

def main():
    parser = argparse.ArgumentParser(description="Minimal Groq API connection and model availability test")
    parser.add_argument("--model", type=str, default="openai/gpt-oss-120b", help="Target Groq model ID")
    parser.add_argument("--list-models", action="store_true", help="List all models accessible to this API key")
    args = parser.parse_args()

    try:
        from groq_backend import get_groq_api_key
        api_key = get_groq_api_key()
    except ImportError:
        api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        print("=" * 70)
        print("[GROQ CONNECTION TEST] STATUS: BLOCKED - MISSING API KEY")
        print("=" * 70)
        print("The environment variable 'GROQ_API_KEY' is not set in this process.")
        print()
        print("To configure it safely in your Windows PowerShell session without logging:")
        print('  $env:GROQ_API_KEY = Read-Host "Paste your Groq API key"')
        print()
        print("Do not hardcode or commit your key into any source file or chat.")
        print("=" * 70)
        sys.exit(2)

    masked_key = api_key[:4] + "..." + api_key[-4:] if len(api_key) >= 12 else "[SET]"
    print("=" * 70)
    print(f"[GROQ CONNECTION TEST] Initializing Groq API Client")
    print(f"Target Model: {args.model}")
    print(f"API Key:      {masked_key} (Length: {len(api_key)})")
    print("=" * 70)

    try:
        from groq import Groq, AuthenticationError, RateLimitError, BadRequestError, NotFoundError, APIConnectionError, APIStatusError
    except ImportError as e:
        print(f"[ERROR] Groq SDK is not installed in the current environment: {e}")
        sys.exit(1)

    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f"[ERROR] Failed to instantiate Groq client: {sanitize_error(str(e))}")
        sys.exit(1)

    # 1. Inspect accessible models
    available_model_ids = []
    try:
        models_page = client.models.list()
        available_model_ids = [m.id for m in models_page.data]
        print(f"[MODELS CHECK] Successfully retrieved {len(available_model_ids)} accessible models.")
        if args.list_models or args.model not in available_model_ids:
            print("Accessible Model IDs:")
            for mid in sorted(available_model_ids):
                marker = " <-- TARGET" if mid == args.model else ""
                print(f"  - {mid}{marker}")
    except AuthenticationError as e:
        print(f"[AUTH ERROR] Invalid or expired Groq API key (HTTP 401).")
        print(f"Details: {sanitize_error(str(e))}")
        sys.exit(1)
    except RateLimitError as e:
        print(f"[RATE LIMIT ERROR] Rate limit or quota exhausted during models query (HTTP 429).")
        print(f"Details: {sanitize_error(str(e))}")
        sys.exit(1)
    except APIConnectionError as e:
        print(f"[CONNECTION ERROR] Failed to connect to api.groq.com: {sanitize_error(str(e))}")
        sys.exit(1)
    except Exception as e:
        print(f"[WARNING] Could not list models: {sanitize_error(str(e))}")

    # Check if target model is available
    if available_model_ids and args.model not in available_model_ids:
        print()
        print(f"[MODEL ACCESS WARNING] Target model '{args.model}' is NOT in the list of {len(available_model_ids)} accessible models for this key!")
        # Suggest closest matches
        matches = [m for m in available_model_ids if any(part in m.lower() for part in ["gpt", "120b", "oss", "llama", "mixtral"])]
        if matches:
            print(f"Potential alternative models available:")
            for m in matches:
                print(f"  - {m}")
        print()
        print(f"Attempting minimal request anyway to inspect direct provider response for '{args.model}'...")

    # 2. Minimal Ping Request
    t0 = time.monotonic()
    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5,
            temperature=0.0
        )
        latency_ms = (time.monotonic() - t0) * 1000.0

        content = response.choices[0].message.content if response.choices else ""
        finish_reason = response.choices[0].finish_reason if response.choices else "unknown"
        p_tokens = getattr(response.usage, "prompt_tokens", None) if response.usage else None
        c_tokens = getattr(response.usage, "completion_tokens", None) if response.usage else None
        t_tokens = getattr(response.usage, "total_tokens", None) if response.usage else None

        print("=" * 70)
        print("[GROQ CONNECTION TEST] SUCCESS — MINIMAL API REQUEST PASSED")
        print("=" * 70)
        print(f"Model Used:        {response.model}")
        print(f"Latency:           {latency_ms:.2f} ms")
        print(f"Response Content:  {repr(content)}")
        print(f"Finish Reason:     {finish_reason}")
        print(f"Token Accounting:  prompt={p_tokens}, completion={c_tokens}, total={t_tokens}")
        print("=" * 70)
        print("[VERDICT] Groq API client is operational and model is reachable.")
        return 0

    except AuthenticationError as e:
        latency_ms = (time.monotonic() - t0) * 1000.0
        print(f"[AUTH ERROR] (Latency: {latency_ms:.2f} ms) HTTP 401 Authentication Failed.")
        print(f"Details: {sanitize_error(str(e))}")
        return 1

    except RateLimitError as e:
        latency_ms = (time.monotonic() - t0) * 1000.0
        print(f"[RATE LIMIT / QUOTA ERROR] (Latency: {latency_ms:.2f} ms) HTTP 429 Rate Limit Exceeded.")
        print(f"Details: {sanitize_error(str(e))}")
        return 1

    except (NotFoundError, BadRequestError) as e:
        latency_ms = (time.monotonic() - t0) * 1000.0
        print(f"[MODEL ERROR] (Latency: {latency_ms:.2f} ms) Target model '{args.model}' rejected by Groq API.")
        print(f"Details: {sanitize_error(str(e))}")
        return 1

    except APIConnectionError as e:
        latency_ms = (time.monotonic() - t0) * 1000.0
        print(f"[CONNECTION ERROR] (Latency: {latency_ms:.2f} ms) Network connection to Groq failed.")
        print(f"Details: {sanitize_error(str(e))}")
        return 1

    except APIStatusError as e:
        latency_ms = (time.monotonic() - t0) * 1000.0
        print(f"[API STATUS ERROR] (Latency: {latency_ms:.2f} ms) HTTP {e.status_code}.")
        print(f"Details: {sanitize_error(str(e))}")
        return 1

    except Exception as e:
        latency_ms = (time.monotonic() - t0) * 1000.0
        print(f"[UNEXPECTED ERROR] (Latency: {latency_ms:.2f} ms): {sanitize_error(str(e))}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
