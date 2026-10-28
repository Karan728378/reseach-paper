"""
Defensible Budget Controls and Preflight Cost Estimation Module
Part of: "The DOM Serialization Gap" Research Infrastructure

Provides:
1. Model pricing tables with fail-closed behavior for unknown models.
2. Conservative preflight budget bounding before trial dispatch.
3. Real-time per-step and per-run accumulation using provider metadata when present,
   falling back to verified conservative estimates.
4. Pre-run check preventing trial dispatch when worst-case step budget exceeds remaining ceiling.
5. Explicit documentation of client-side guard limitations vs provider billing caps.
"""

import threading
from typing import Dict, Any, Optional, Tuple, List
import math
import json
import csv
from pathlib import Path
from datetime import datetime

# Default path for persistent daily quota accounting
DEFAULT_LEDGER_PATH = Path("C:/testing/research_execution_20261018/results/daily_quota_ledger.json")


def load_daily_requests_offset(
    ledger_path: Optional[Path] = None,
    summary_csvs: Optional[List[Path]] = None,
    target_date: Optional[str] = None,
    provider: Optional[str] = None
) -> Tuple[int, float]:
    """
    Computes cumulative daily usage offset from persisted ledger and summary CSV files.
    Ensures process restarts do NOT reset daily request accounting.
    Deduplicates across multiple summary CSVs and avoids cross-provider contamination.

    Returns:
        Tuple[int, float]: (cumulative_requests_offset, cumulative_cost_offset_usd)

    ACCOUNTING SCOPE & BOUNDARIES:
    What this function CAN observe:
    1. Model requests and estimated costs recorded in summary CSV rows timestamped on target_date.
    2. Persisted state from prior runner executions recorded in daily_quota_ledger.json.

    What this function CANNOT observe:
    1. Provider-side network retries or transient backend redirects that did not surface to the client.
    2. Out-of-band requests made by other scripts, machines, or processes sharing the API key.
    3. Exact provider-level quota meter readings (neither Google AI Studio nor Groq provide live quota polling).
    """
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")

    ledger_reqs = 0
    ledger_cost = 0.0

    # 1. Read from ledger JSON if available
    lpath = Path(ledger_path) if ledger_path else DEFAULT_LEDGER_PATH
    if lpath.exists():
        try:
            data = json.loads(lpath.read_text(encoding="utf-8"))
            if data.get("date") == target_date:
                ledger_provider = str(data.get("provider", "gemini")).lower()
                if provider is None or ledger_provider == provider.lower():
                    ledger_reqs = int(data.get("cumulative_requests", 0))
                    ledger_cost = float(data.get("cumulative_cost_usd", 0.0))
        except Exception:
            pass

    # 2. Inspect summary CSVs to ensure any completed/aborted runs recorded on target_date are included
    # Deduplicate runs across CSV files using (run_index, timestamp_start, timestamp_end)
    csv_reqs = 0
    csv_cost = 0.0
    seen_runs = set()

    if summary_csvs:
        for cpath in summary_csvs:
            p = Path(cpath)
            if not p.exists():
                continue
            try:
                with p.open("r", encoding="utf-8-sig", errors="replace") as f:
                    reader = csv.DictReader(f)
                    for r in reader:
                        t_start = r.get("timestamp_start", "")
                        t_end = r.get("timestamp_end", "")
                        if target_date in t_start or target_date in t_end or not target_date:
                            row_model = str(r.get("model", "")).lower()
                            # Filter by provider if specified
                            if provider == "groq" and row_model and "gemini" in row_model:
                                continue
                            if provider == "gemini" and row_model and any(g in row_model for g in ["gpt-oss", "llama", "mixtral", "groq"]):
                                continue

                            # Deduplicate identical run recorded in multiple summary CSVs
                            run_key = (r.get("run_index", ""), t_start, t_end)
                            if run_key in seen_runs and (t_start or t_end):
                                continue
                            seen_runs.add(run_key)

                            # Prefer explicit model_requests if recorded; fallback to total_steps for legacy rows
                            if "model_requests" in r and r.get("model_requests"):
                                try:
                                    reqs = int(float(r.get("model_requests", 0)))
                                except (ValueError, TypeError):
                                    reqs = 0
                            else:
                                try:
                                    reqs = int(float(r.get("total_steps", 0)))
                                except (ValueError, TypeError):
                                    reqs = 0

                            try:
                                cost = float(r.get("estimated_cost_usd", 0.0))
                            except (ValueError, TypeError):
                                cost = 0.0

                            csv_reqs += reqs
                            csv_cost += cost
            except Exception:
                pass

    reqs_offset = max(ledger_reqs, csv_reqs)
    cost_offset = max(ledger_cost, csv_cost)
    return reqs_offset, cost_offset


# Authoritative standard pricing table (USD per 1,000,000 tokens) as of late 2024 / 2025
# Standardized to conservative upper tiers (<= 128k prompt context)
MODEL_PRICING_TABLE = {
    # Gemini models
    "gemini-flash-lite-latest": {"input_per_million": 0.15, "output_per_million": 0.60},
    "gemini-2.0-flash-lite": {"input_per_million": 0.15, "output_per_million": 0.60},
    "gemini-2.0-flash-lite-preview-02-05": {"input_per_million": 0.15, "output_per_million": 0.60},
    "gemini-1.5-flash": {"input_per_million": 0.15, "output_per_million": 0.60},
    "gemini-1.5-flash-8b": {"input_per_million": 0.075, "output_per_million": 0.30},
    "gemini-1.5-pro": {"input_per_million": 2.50, "output_per_million": 10.00},
    "gemini-2.0-flash": {"input_per_million": 0.15, "output_per_million": 0.60},
    "gemini-3-flash-preview": {"input_per_million": 0.15, "output_per_million": 0.60},
    "gemini-3.1-flash-lite": {"input_per_million": 0.15, "output_per_million": 0.60},
    # Anthropic models
    "claude-3-5-sonnet-20241022": {"input_per_million": 3.00, "output_per_million": 15.00},
    "claude-3-5-haiku-20241022": {"input_per_million": 1.00, "output_per_million": 5.00},
    # OpenAI models
    "gpt-4o": {"input_per_million": 2.50, "output_per_million": 10.00},
    "gpt-4o-mini": {"input_per_million": 0.15, "output_per_million": 0.60},
    # Groq models
    "openai/gpt-oss-120b": {"input_per_million": 0.15, "output_per_million": 0.60},
    "gpt-oss-120b": {"input_per_million": 0.15, "output_per_million": 0.60},
    "llama-3.3-70b-versatile": {"input_per_million": 0.59, "output_per_million": 0.79},
    "llama-3.1-8b-instant": {"input_per_million": 0.05, "output_per_million": 0.08},
    "mixtral-8x7b-32768": {"input_per_million": 0.24, "output_per_million": 0.24},
}

DEFAULT_GROQ_LEDGER_PATH = Path("results/daily_groq_quota_ledger.json")

# Conservative default upper bounds per step
WORST_CASE_INPUT_TOKENS_PER_STEP = 10000
WORST_CASE_OUTPUT_TOKENS_PER_STEP = 500

class BudgetExceededError(RuntimeError):
    """Raised when an operation would exceed the configured client budget ceiling."""
    pass

class UnknownModelPricingError(ValueError):
    """Raised when a model has no pricing defined, failing closed."""
    pass

def get_model_pricing(model_name: str) -> Dict[str, float]:
    """
    Look up pricing for a model name. Normalizes case and common prefixes.
    Fails closed if the model pricing cannot be bounded.
    """
    clean_name = model_name.strip().lower()
    # Remove provider prefixes if present (e.g., 'google/', 'anthropic/')
    if "/" in clean_name:
        clean_name = clean_name.split("/", 1)[1]
        
    for key, pricing in MODEL_PRICING_TABLE.items():
        if key.lower() == clean_name or clean_name.startswith(key.lower()):
            return pricing
            
    raise UnknownModelPricingError(
        f"UNKNOWN MODEL PRICING: Cannot establish bounded budget for '{model_name}'. "
        f"Known models: {list(MODEL_PRICING_TABLE.keys())}. "
        f"Failing closed to prevent unbounded financial risk."
    )

def compute_step_cost(
    model_name: str,
    prompt_tokens: int,
    completion_tokens: int
) -> float:
    """Compute cost in USD for given token counts."""
    pricing = get_model_pricing(model_name)
    input_cost = (prompt_tokens / 1_000_000.0) * pricing["input_per_million"]
    output_cost = (completion_tokens / 1_000_000.0) * pricing["output_per_million"]
    return input_cost + output_cost

def compute_worst_case_run_cost(
    model_name: str,
    max_steps: int = 15,
    worst_case_input_per_step: int = WORST_CASE_INPUT_TOKENS_PER_STEP,
    worst_case_output_per_step: int = WORST_CASE_OUTPUT_TOKENS_PER_STEP
) -> float:
    """Compute the theoretical maximum cost of a single trial at max steps."""
    max_in = max_steps * worst_case_input_per_step
    max_out = max_steps * worst_case_output_per_step
    return compute_step_cost(model_name, max_in, max_out)

def estimate_preflight_budget(
    total_runs: int,
    model_name: str,
    cost_ceiling_usd: float,
    max_steps: int = 15
) -> Dict[str, Any]:
    """
    Perform conservative preflight cost calculation across an entire planned schedule.
    Returns audit details and indicates whether the budget is sufficient under worst-case bounds.
    """
    pricing = get_model_pricing(model_name)
    worst_case_single_run = compute_worst_case_run_cost(model_name, max_steps=max_steps)
    worst_case_total_usd = total_runs * worst_case_single_run
    
    # Expected realistic cost (e.g. average 5.5 steps, ~6,500 input tokens/step)
    realistic_single_run = compute_step_cost(model_name, int(5.5 * 6500), int(5.5 * 100))
    realistic_total_usd = total_runs * realistic_single_run
    
    worst_case_exceeds = worst_case_total_usd > cost_ceiling_usd
    
    return {
        "model_name": model_name,
        "pricing": pricing,
        "total_runs": total_runs,
        "max_steps_per_run": max_steps,
        "worst_case_single_run_usd": round(worst_case_single_run, 6),
        "worst_case_total_usd": round(worst_case_total_usd, 4),
        "realistic_expected_total_usd": round(realistic_total_usd, 4),
        "cost_ceiling_usd": cost_ceiling_usd,
        "worst_case_exceeds_ceiling": worst_case_exceeds,
        "guaranteed_provider_limit": False,
        "disclaimer": (
            "NOTICE: The local cost ceiling is a client-side software guardrail that halts "
            "execution when cumulative estimated or provider-reported cost reaches the limit. "
            "It does NOT replace provider-side billing caps. In the event of network timeouts, "
            "partial stream billing, or out-of-band requests, charges may occur before the client "
            "can halt. Users MUST configure provider-side billing limits in their cloud console."
        )
    }

class LocalBudgetGuard:
    """
    Thread-safe client-side budget accumulator and guard.
    Fails closed when:
    - Model pricing is undefined.
    - Cumulative cost reaches or exceeds ceiling (when ceiling > 0).
    - Cumulative model requests reach or exceed free-tier ceiling (when is_free_tier or ceiling == 0).
    - Pre-run check shows remaining budget or request headroom cannot accommodate the trial.

    ACCOUNTING BOUNDARY NOTICE:
    What this guard CAN count:
    1. Client-side HTTP model requests dispatched by the current process.
    2. Persisted cumulative requests recorded in the daily ledger and completed summary CSVs across restarts.
    3. Conservative step-level token approximations when provider metadata is absent.

    What this guard CANNOT count:
    1. Provider-side network retries or transient backend redirects that do not surface to the client.
    2. Diagnostic or ad-hoc API calls made by other scripts or external processes without this guard.
    3. Out-of-band usage by other developers or tools sharing the same API key.
    4. Exact provider-level billing or quota meter readings, as Google AI Studio free-tier quotas cannot be polled via API.
    Therefore, this guard operates fail-closed and conservatively, but users must monitor the Google Cloud / AI Studio console for true provider-side quota consumption.
    """
    def __init__(
        self,
        cost_ceiling_usd: float,
        model_name: str,
        max_steps_per_run: int = 15,
        max_requests_ceiling: Optional[int] = None,
        max_tokens_ceiling: Optional[int] = None,
        is_free_tier: bool = False,
        initial_requests_offset: int = 0,
        initial_cost_offset_usd: float = 0.0,
        ledger_path: Optional[Path] = None,
        provider: str = "gemini"
    ):
        self.cost_ceiling_usd = float(cost_ceiling_usd)
        self.model_name = model_name
        self.max_steps_per_run = max_steps_per_run
        self.max_requests_ceiling = max_requests_ceiling
        self.max_tokens_ceiling = max_tokens_ceiling
        self.is_free_tier = is_free_tier or (self.cost_ceiling_usd == 0.0)
        self.pricing = get_model_pricing(model_name)
        self.initial_requests_offset = int(initial_requests_offset)
        self.initial_cost_offset_usd = float(initial_cost_offset_usd)
        self.cumulative_cost_usd = float(initial_cost_offset_usd)
        self.cumulative_prompt_tokens = 0
        self.cumulative_completion_tokens = 0
        self.cumulative_requests = int(initial_requests_offset)
        self.runs_completed = 0
        self.halted_due_to_ceiling = False
        self.ledger_path = Path(ledger_path) if ledger_path else None
        self.provider = provider
        self._lock = threading.RLock()


    def save_daily_ledger(self, ledger_path: Optional[Path] = None) -> Optional[Path]:
        """Persists current cumulative request and cost ledger to disk."""
        target_path = Path(ledger_path) if ledger_path else self.ledger_path
        if not target_path:
            return None
        target_path.parent.mkdir(parents=True, exist_ok=True)
        today_str = datetime.now().strftime("%Y-%m-%d")
        ledger_data = {
            "date": today_str,
            "provider": self.provider,
            "cumulative_requests": self.cumulative_requests,
            "cumulative_cost_usd": round(self.cumulative_cost_usd, 6),
            "cumulative_prompt_tokens": self.cumulative_prompt_tokens,
            "cumulative_completion_tokens": self.cumulative_completion_tokens,
            "cumulative_total_tokens": self.cumulative_prompt_tokens + self.cumulative_completion_tokens,
            "runs_completed": self.runs_completed,
            "model_name": self.model_name,
            "cost_ceiling_usd": self.cost_ceiling_usd,
            "max_requests_ceiling": self.max_requests_ceiling,
            "max_tokens_ceiling": self.max_tokens_ceiling,
            "is_free_tier": self.is_free_tier,
            "halted_due_to_ceiling": self.halted_due_to_ceiling,
            "last_updated": datetime.now().isoformat(),
            "accounting_scope_and_limitations": {
                "counted": "In-process steps, persisted offsets from today's summary CSVs/ledger, conservative token estimates",
                "not_counted": "Provider-side hidden retries, out-of-band requests from external scripts, provider billing meter",
                "guarantee": "Fail-closed client-side bounded requests; does not replace provider cloud console quotas"
            }
        }
        target_path.write_text(json.dumps(ledger_data, indent=2), encoding="utf-8")
        return target_path

    def check_can_dispatch_trial(self, require_worst_case_headroom: bool = False) -> Tuple[bool, str]:
        """
        Check if another trial can be safely dispatched.
        Enforces both dollar spending limits and free-tier request ceilings.
        """
        total_tokens = self.cumulative_prompt_tokens + self.cumulative_completion_tokens
        if self.max_tokens_ceiling is not None and total_tokens >= self.max_tokens_ceiling:
            self.halted_due_to_ceiling = True
            return False, (
                f"Cumulative tokens ({total_tokens}) reached ceiling ({self.max_tokens_ceiling}). "
                f"Failing closed to prevent quota overrun."
            )

        if self.is_free_tier:
            if self.max_requests_ceiling is not None:
                if self.cumulative_requests >= self.max_requests_ceiling:
                    self.halted_due_to_ceiling = True
                    return False, (
                        f"Cumulative requests ({self.cumulative_requests}) reached free-tier quota ceiling "
                        f"({self.max_requests_ceiling}). Failing closed to maintain $0.00 spending."
                    )
                if require_worst_case_headroom and (self.cumulative_requests + self.max_steps_per_run > self.max_requests_ceiling):
                    return False, (
                        f"Remaining free-tier requests ({self.max_requests_ceiling - self.cumulative_requests}) "
                        f"is less than worst-case trial steps ({self.max_steps_per_run}). Failing closed."
                    )
            return True, f"Free-tier quota available ({self.cumulative_requests}/{self.max_requests_ceiling or 'unlimited'} requests used). Billed spend locked at $0.00."

        remaining = self.cost_ceiling_usd - self.cumulative_cost_usd
        if remaining <= 0.0:
            self.halted_due_to_ceiling = True
            return False, f"Cumulative cost (${self.cumulative_cost_usd:.4f}) reached or exceeded ceiling (${self.cost_ceiling_usd:.2f})."
            
        if require_worst_case_headroom:
            worst_case_run = compute_worst_case_run_cost(self.model_name, self.max_steps_per_run)
            if remaining < worst_case_run:
                return False, (
                    f"Remaining budget (${remaining:.4f}) is less than worst-case trial cost (${worst_case_run:.4f}). "
                    f"Failing closed before trial dispatch."
                )
                
        return True, "Budget available."

    def check_can_dispatch_request(self) -> Tuple[bool, str]:
        """
        Check if a single in-flight LLM request can be safely dispatched.
        Evaluated immediately before every individual model API call.
        Thread-safe under self._lock.
        """
        with self._lock:
            total_tokens = self.cumulative_prompt_tokens + self.cumulative_completion_tokens
            if self.max_tokens_ceiling is not None and total_tokens >= self.max_tokens_ceiling:
                self.halted_due_to_ceiling = True
                return False, (
                    f"Pre-dispatch request blocked: cumulative tokens ({total_tokens}) "
                    f"reached ceiling ({self.max_tokens_ceiling}). Failing closed."
                )

            if self.is_free_tier:
                if self.max_requests_ceiling is not None:
                    if self.cumulative_requests >= self.max_requests_ceiling:
                        self.halted_due_to_ceiling = True
                        return False, (
                            f"Pre-dispatch request blocked: cumulative requests ({self.cumulative_requests}) "
                            f"reached ceiling ({self.max_requests_ceiling}). Failing closed to maintain $0.00 spend."
                        )
                return True, f"Request permitted ({self.cumulative_requests}/{self.max_requests_ceiling or 'unlimited'})."

            remaining = self.cost_ceiling_usd - self.cumulative_cost_usd
            if remaining <= 0.0:
                self.halted_due_to_ceiling = True
                return False, f"Pre-dispatch request blocked: cost ceiling (${self.cost_ceiling_usd:.4f}) reached."
            return True, "Request permitted."

    def record_request_pre_dispatch(
        self,
        estimated_prompt_tokens: Optional[int] = None,
        estimated_completion_tokens: Optional[int] = None
    ) -> float:
        """
        Atomically increments request counter BEFORE network dispatch.
        Guarantees that even if the network call times out, drops, or errors,
        the attempt is accounted for against the ceiling.
        Thread-safe under self._lock.
        """
        with self._lock:
            can_dispatch, msg = self.check_can_dispatch_request()
            if not can_dispatch:
                raise BudgetExceededError(msg)

            p_tokens = estimated_prompt_tokens if estimated_prompt_tokens is not None else WORST_CASE_INPUT_TOKENS_PER_STEP
            c_tokens = estimated_completion_tokens if estimated_completion_tokens is not None else WORST_CASE_OUTPUT_TOKENS_PER_STEP
            step_cost = compute_step_cost(self.model_name, p_tokens, c_tokens)

            self.cumulative_requests += 1
            self.cumulative_prompt_tokens += p_tokens
            self.cumulative_completion_tokens += c_tokens
            self.cumulative_cost_usd += step_cost

            if self.is_free_tier and self.max_requests_ceiling is not None and self.cumulative_requests >= self.max_requests_ceiling:
                self.halted_due_to_ceiling = True
            elif not self.is_free_tier and self.cumulative_cost_usd >= self.cost_ceiling_usd:
                self.halted_due_to_ceiling = True

            if self.ledger_path:
                self.save_daily_ledger()

            return step_cost

    def record_request_post_dispatch(
        self,
        actual_prompt_tokens: Optional[int] = None,
        actual_completion_tokens: Optional[int] = None
    ) -> None:
        """
        Updates token and cost accounting with actual provider-returned usage,
        correcting the pre-dispatch estimate without double-counting requests.
        Thread-safe under self._lock.
        """
        with self._lock:
            if actual_prompt_tokens is not None and actual_completion_tokens is not None:
                pre_p = WORST_CASE_INPUT_TOKENS_PER_STEP
                pre_c = WORST_CASE_OUTPUT_TOKENS_PER_STEP
                pre_cost = compute_step_cost(self.model_name, pre_p, pre_c)
                actual_cost = compute_step_cost(self.model_name, actual_prompt_tokens, actual_completion_tokens)

                self.cumulative_prompt_tokens += (actual_prompt_tokens - pre_p)
                self.cumulative_completion_tokens += (actual_completion_tokens - pre_c)
                self.cumulative_cost_usd += (actual_cost - pre_cost)
                if self.ledger_path:
                    self.save_daily_ledger()

    def record_step(
        self,
        prompt_tokens: Optional[int] = None,
        completion_tokens: Optional[int] = None
    ) -> float:
        """
        Record a step's token consumption and increment request counter.
        Thread-safe under self._lock.
        """
        with self._lock:
            p_tokens = prompt_tokens if prompt_tokens is not None else WORST_CASE_INPUT_TOKENS_PER_STEP
            c_tokens = completion_tokens if completion_tokens is not None else WORST_CASE_OUTPUT_TOKENS_PER_STEP
            
            step_cost = compute_step_cost(self.model_name, p_tokens, c_tokens)
            self.cumulative_prompt_tokens += p_tokens
            self.cumulative_completion_tokens += c_tokens
            self.cumulative_cost_usd += step_cost
            self.cumulative_requests += 1
            
            if not self.is_free_tier and self.cumulative_cost_usd >= self.cost_ceiling_usd:
                self.halted_due_to_ceiling = True
            elif self.is_free_tier and self.max_requests_ceiling is not None and self.cumulative_requests >= self.max_requests_ceiling:
                self.halted_due_to_ceiling = True
                
            if self.ledger_path:
                self.save_daily_ledger()

            return step_cost

    def record_trial_completion(
        self,
        total_steps: int,
        provider_prompt_tokens: Optional[int] = None,
        provider_completion_tokens: Optional[int] = None,
        requests_already_recorded: bool = False
    ) -> Dict[str, Any]:
        """
        Finalize a trial and update cumulative ledger.
        If requests_already_recorded=True, cumulative_requests is not re-incremented.
        Thread-safe under self._lock.
        """
        with self._lock:
            if provider_prompt_tokens is not None and provider_completion_tokens is not None:
                p_tokens = provider_prompt_tokens
                c_tokens = provider_completion_tokens
                source = "provider_reported"
            else:
                p_tokens = total_steps * 7000
                c_tokens = total_steps * 100
                source = "conservative_step_estimate"
                
            trial_cost = compute_step_cost(self.model_name, p_tokens, c_tokens)
            if not requests_already_recorded:
                self.cumulative_prompt_tokens += p_tokens
                self.cumulative_completion_tokens += c_tokens
                self.cumulative_cost_usd += trial_cost
                self.cumulative_requests += total_steps

            self.runs_completed += 1
            
            if not self.is_free_tier and self.cumulative_cost_usd >= self.cost_ceiling_usd:
                self.halted_due_to_ceiling = True
            elif self.is_free_tier and self.max_requests_ceiling is not None and self.cumulative_requests >= self.max_requests_ceiling:
                self.halted_due_to_ceiling = True
                
            if self.ledger_path:
                self.save_daily_ledger()

            return {
                "trial_cost_usd": round(trial_cost, 6),
                "token_source": source,
                "prompt_tokens": p_tokens,
                "completion_tokens": c_tokens,
                "cumulative_cost_usd": round(self.cumulative_cost_usd, 6),
                "remaining_budget_usd": round(max(0.0, self.cost_ceiling_usd - self.cumulative_cost_usd), 6) if not self.is_free_tier else 0.0,
                "cumulative_requests": self.cumulative_requests,
                "max_requests_ceiling": self.max_requests_ceiling,
                "halted": self.halted_due_to_ceiling
            }


class BudgetGuardedChatModel:
    """
    Instrumented proxy wrapper around any LLM (LangChain BaseChatModel or browser_use BaseChatModel).
    Guarantees that EVERY individual model request (including retries, tool calls, and in-flight steps)
    is checked and metered against LocalBudgetGuard BEFORE network dispatch.
    """
    def __init__(self, wrapped_model: Any, guard: LocalBudgetGuard):
        self._wrapped_model = wrapped_model
        self._guard = guard
        for attr in ["model_name", "model", "provider", "name"]:
            if hasattr(wrapped_model, attr):
                setattr(self, attr, getattr(wrapped_model, attr))

    def check_and_record_pre_dispatch(self):
        can_dispatch, msg = self._guard.check_can_dispatch_request()
        if not can_dispatch:
            raise BudgetExceededError(msg)
        self._guard.record_request_pre_dispatch()

    def update_post_dispatch(self, response: Any):
        p_tokens, c_tokens = None, None
        try:
            if hasattr(response, "usage") and response.usage:
                p_tokens = getattr(response.usage, "prompt_tokens", None) or getattr(response.usage, "input_tokens", None)
                c_tokens = getattr(response.usage, "completion_tokens", None) or getattr(response.usage, "output_tokens", None)
            elif hasattr(response, "response_metadata") and response.response_metadata:
                usage = response.response_metadata.get("token_usage") or response.response_metadata.get("usage", {})
                p_tokens = usage.get("prompt_tokens") or usage.get("input_tokens")
                c_tokens = usage.get("completion_tokens") or usage.get("output_tokens")
        except Exception:
            pass
        self._guard.record_request_post_dispatch(p_tokens, c_tokens)

    async def ainvoke(self, *args, **kwargs) -> Any:
        self.check_and_record_pre_dispatch()
        response = await self._wrapped_model.ainvoke(*args, **kwargs)
        self.update_post_dispatch(response)
        return response

    def invoke(self, *args, **kwargs) -> Any:
        self.check_and_record_pre_dispatch()
        response = self._wrapped_model.invoke(*args, **kwargs)
        self.update_post_dispatch(response)
        return response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._wrapped_model, name)


