# Quota & Cost Execution Plan
**Audit Date:** 2026-10-18

## Historical Failure Analysis
- Experiment ran 147 runs starting 2026-10-11 07:37 UTC.
- First 105 runs (07:37–08:29): all successful or genuine agent failures.
- Run 106 onward (08:30–08:36): all 42 runs failed within ~8–10s with `total_steps=7`.
- Pattern is consistent with HTTP 429 RESOURCE_EXHAUSTED (Gemini free-tier daily quota: 500 requests).
- Estimated requests consumed by run 105: ~105 × 4.7 steps = ~494 requests → quota exhausted.

## Protocol v3 Budget Estimate

| Scenario | Runs | Est. Steps/Run | Est. API Requests | Exceeds Free 500/day |
|----------|------|---------------|-------------------|----------------------|
| Optimistic (fast tasks) | 96 | 4 | 384 | No |
| Baseline | 96 | 6 | **576** | **Yes** |
| Conservative | 96 | 8 | 768 | Yes |

**Recommendation:** Use Gemini paid tier (Pay-As-You-Go).
- Estimated cost at $0.15/1M input tokens: **< $1.00** for 96 runs.
- No daily quota limit on paid tier.

## Required Safeguards

```python
# In agent-runner.py — required additions

# 1. Hard quota guard
consecutive_429s = 0
MAX_CONSECUTIVE_429 = 3

# 2. Per-run timeout
HARD_TIMEOUT_SECONDS = 120

# 3. Cache disable (before each run)
await page.context.clear_cookies()
await page.cdp_session.send("Network.setCacheDisabled", {"cacheDisabled": True})

# 4. Pre-run cart state assertion (before agent launch)
cart_state = await page.evaluate("window.__cart__")
assert len(cart_state) == 0, f"Cart not empty before run: {cart_state}"

# 5. Vision off
agent = Agent(use_vision=False, ...)
```

## Randomization Implementation

```python
import random

def generate_rcbd_schedule(K=4, J=6, R=4, seed=42):
    arms  = ["ABS","VIS","ARIA","DATA-CFG"]
    tasks = ["T1","T2","T3","T4","T5","T6"]
    rng   = random.Random(seed)
    schedule = []
    run_idx  = 1
    for block in range(1, R+1):
        block_runs = [(a,t) for a in arms for t in tasks]
        rng.shuffle(block_runs)
        for arm, task in block_runs:
            schedule.append({"block": block, "run_index": run_idx, "arm": arm, "task": task})
            run_idx += 1
    return schedule
```
