"""
TechMart Research Runner — Structured JSONL Logger
runner/logger.py — Protocol v2

Writes per-run logs to results/raw/<run_id>.jsonl
Each file contains: one header record, N action records, one summary record.
"""

import json
import uuid
import hashlib
import datetime
from pathlib import Path

RESULTS_RAW = Path("C:/testing/results/raw")


class RunLogger:
    """
    Creates and manages a single JSONL log file per agent run.

    Usage:
        logger = RunLogger(variant="v0-baseline", task_id="T1",
                           phase="pilot", repetition_index=1)
        logger.write_header(agent_model="gpt-4o", agent_temperature=0)
        logger.write_action(step_index=1, action_type="navigate", ...)
        logger.write_summary(success=True, partial_score=1.0, total_steps=7, ...)
    """

    def __init__(self, variant: str, task_id: str, phase: str, repetition_index: int):
        self.run_id = str(uuid.uuid4())
        self.variant = variant
        self.task_id = task_id
        self.phase = phase
        self.repetition_index = repetition_index
        self._step_counter = 0

        RESULTS_RAW.mkdir(parents=True, exist_ok=True)
        self._path = RESULTS_RAW / f"{self.run_id}.jsonl"
        self._file = self._path.open("w", encoding="utf-8")

    # ------------------------------------------------------------------
    def write_header(
        self,
        agent_harness: str = "browser-use",
        agent_model: str = "PLACEHOLDER",
        agent_temperature: float = 0,
        viewport: str = "1280x800",
        static_verification_passed: bool = True,
        visual_verification_passed: bool = True,
    ):
        record = {
            "record_type": "run_header",
            "run_id": self.run_id,
            "phase": self.phase,
            "repetition_index": self.repetition_index,
            "variant": self.variant,
            "task_id": self.task_id,
            "agent_harness": agent_harness,
            "agent_model": agent_model,
            "agent_temperature": agent_temperature,
            "viewport": viewport,
            "timestamp_start": _now(),
            "static_verification_passed": static_verification_passed,
            "visual_verification_passed": visual_verification_passed,
        }
        self._write(record)
        return self

    # ------------------------------------------------------------------
    def write_action(
        self,
        action_type: str,
        target_selector: str = "",
        target_visible_text: str = "",
        input_value: str = "",
        agent_reasoning: str = "",
        page_url: str = "",
        dom_snapshot: str = "",
    ):
        self._step_counter += 1
        record = {
            "record_type": "agent_action",
            "run_id": self.run_id,
            "step_index": self._step_counter,
            "timestamp": _now(),
            "action_type": action_type,
            "target_selector": target_selector,
            "target_visible_text": target_visible_text,
            "input_value": input_value,
            "agent_reasoning": agent_reasoning,
            "page_url": page_url,
            "dom_snapshot_hash": hashlib.sha256(
                dom_snapshot.encode("utf-8")
            ).hexdigest() if dom_snapshot else "",
        }
        self._write(record)

    # ------------------------------------------------------------------
    def write_summary(
        self,
        success: bool,
        partial_score: float,
        total_steps: int,
        total_time_seconds: float,
        cart_state: list = None,
        order_confirmed: bool = False,
        error_message: str = None,
        final_dom_snapshot: str = "",
    ):
        record = {
            "record_type": "run_summary",
            "run_id": self.run_id,
            "phase": self.phase,
            "repetition_index": self.repetition_index,
            "variant": self.variant,
            "task_id": self.task_id,
            "success": success,
            "partial_score": round(partial_score, 4),
            "total_steps": total_steps,
            "total_time_seconds": round(total_time_seconds, 3),
            "cart_state_at_end": cart_state or [],
            "order_confirmed": order_confirmed,
            "error_message": error_message,
            "timestamp_end": _now(),
            "final_dom_snapshot_hash": hashlib.sha256(
                final_dom_snapshot.encode("utf-8")
            ).hexdigest() if final_dom_snapshot else "",
        }
        self._write(record)
        self._file.close()
        return self._path

    # ------------------------------------------------------------------
    def _write(self, record: dict):
        self._file.write(json.dumps(record, ensure_ascii=False) + "\n")
        self._file.flush()

    # ------------------------------------------------------------------
    def __repr__(self):
        return f"RunLogger(run_id={self.run_id}, variant={self.variant}, task={self.task_id})"


# ------------------------------------------------------------------
def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


# ------------------------------------------------------------------
def append_to_summary_csv(csv_path: Path, run_summary: dict):
    """Append one run's summary to the flat CSV aggregation file."""
    import csv

    fieldnames = [
        "run_id", "phase", "repetition_index", "variant", "task_id",
        "success", "partial_score", "total_steps", "total_time_seconds",
        "order_confirmed", "error_message", "timestamp_end",
    ]
    write_header = not csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow(run_summary)


# ------------------------------------------------------------------
if __name__ == "__main__":
    # Quick self-test
    logger = RunLogger("v0-baseline", "T1", "pilot", 1)
    logger.write_header(agent_model="test-model")
    logger.write_action("navigate", page_url="http://localhost:8080/variants/v0-baseline/")
    logger.write_action("type", target_selector="#search-input", input_value="wireless headphones")
    logger.write_action("click", target_selector="#search-submit-btn")
    logger.write_action("click", target_selector="#product-card-wh-001 .btn-add-cart",
                        target_visible_text="Add to Cart")
    path = logger.write_summary(
        success=True, partial_score=1.0, total_steps=4,
        total_time_seconds=8.5, cart_state=[{"sku": "wh-001", "name": "SoundFlow Air 3",
                                              "quantity": 1, "price": 49.99}]
    )
    print(f"Test log written: {path}")
    with path.open() as f:
        for line in f:
            print(json.loads(line)["record_type"])
