# Data Dictionary & Codebook
**Protocol Version:** v3  
**Date:** 2026-10-18  

This document provides complete, exhaustive definitions for all schemas, variables, units, valid ranges, and codes used across the experimental package.

---

## 1. Experimental Run Manifest Schema (`run_manifest_schema.json`)

| Variable Name | Type | Unit / Format | Permitted Values | Description |
|---------------|------|---------------|------------------|-------------|
| `run_id` | String | UUIDv4 / Canonical | `run_[a-f0-9]{12}` | Unique hexadecimal identifier for the individual run. |
| `scheduled_run_index` | Integer | Scalar | `1` to `96` | 1-indexed order in the randomized schedule. |
| `block_id` | Integer | Scalar | `1` to `4` | RCBD block number. |
| `within_block_order` | Integer | Scalar | `1` to `24` | Execution sequence position within the assigned block. |
| `arm` | String | Categorical | `ABS`, `VIS`, `ARIA`, `DATA-CFG` | Experimental information-delivery channel condition. |
| `task_id` | String | Categorical | `T1`, `T2`, `T3`, `T4`, `T5`, `T6` | Canonical task identifier. |
| `variant` | String | Identifier | `v0-baseline`, `v2-aria`, `v3-data-attrs` | Web codebase variant serving the DOM. |
| `agent_model` | String | String | `gemini-flash-lite-latest` | LLM model identifier. |
| `use_vision` | Boolean | Boolean | `False` | Multimodal screenshot processing flag (must be False). |
| `temperature` | Float / Null | Scalar | `null` | Sampling temperature parameter. |
| `timestamp_start` | String | ISO 8601 | `YYYY-MM-DDTHH:MM:SSZ` | UTC start timestamp. |
| `timestamp_end` | String | ISO 8601 | `YYYY-MM-DDTHH:MM:SSZ` | UTC completion timestamp. |
| `total_time_seconds` | Float | Seconds | $\ge 0.0$ | Total wall-clock duration of the run. |
| `total_steps` | Integer | Count | $0$ to $30$ | Total interaction steps taken by agent. |
| `success` | Boolean | Boolean | `True`, `False` | Primary outcome: binary task success verified by post-state. |
| `partial_score` | Float | Ratio | `0.0` to `1.0` | Secondary metric: weighted step completion score. |
| `error_code` | String / Null | Enum | `null`, `HTTP_429`, `TIMEOUT`, `PRE_STATE_ERROR`, `NAV_FAIL` | Standardized error categorization. |
| `raw_cart_state` | Array | JSON Array | Array of SKU objects | Snapshot of `window.__cart__` at termination. |
| `order_confirmed` | Boolean | Boolean | `True`, `False` | Snapshot of `window.__orderConfirmed__`. |
| `verifier_details` | Object | JSON Object | Object | Key-value pairs output by task verifier. |

---

## 2. Treatment Design Matrix (`treatment_matrix.csv`)

| Variable Name | Type | Description |
|---------------|------|-------------|
| `task_id` | String | Task identifier (`T1` to `T6`). |
| `arm` | String | Experimental treatment arm (`ABS`, `VIS`, `ARIA`, `DATA-CFG`). |
| `target_entity` | String | SKU or entity ID intended for grounding (e.g. `wh-001`, `mkp-001`). |
| `target_field` | String | Entity attribute under manipulation (e.g. `price`, `rating`, `warranty`). |
| `target_token` | String | Literal token value that represents the ground truth. |
| `source_channel_location` | String | DOM selector or attribute where token is placed. |
| `expected_serialized_observation` | String | Expected serialized text representation received by LLM. |
| `prohibited_leakage_channels` | String | Explicit list of channels where target token must NOT appear. |
| `verifier_type` | String | Programmatic verifier function identifier. |
| `success_criterion` | String | Human-readable boolean success condition. |

---

## 3. Results Summary CSV (`results/main_experiment/full-summary.csv`)

| Column Name | Type | Format | Description |
|-------------|------|--------|-------------|
| `run_id` | String | String | Run identifier. |
| `scheduled_run_index` | Integer | `1` to `96` | Schedule index. |
| `block_id` | Integer | `1` to `4` | Block number. |
| `arm` | String | Categorical | Treatment condition. |
| `task_id` | String | Categorical | Task ID. |
| `success` | Integer | `0` or `1` | Binary success indicator (1=Success, 0=Failure). |
| `partial_score` | Float | `0.00` to `1.00` | Partial score. |
| `total_steps` | Integer | Count | Step count. |
| `total_time` | Float | Seconds | Elapsed duration. |
| `error_category` | String | String | Error classification if failed. |
