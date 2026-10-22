# 05. Research Design Evaluation & Recommendation

**Audit Directory:** `C:\testing\research_audit_20261015_231500`  
**Date:** 2026-10-17  
**Auditor:** Antigravity Senior Empirical Research & Reproducibility Team  

---

## 1. Evaluation of Candidate Research Question

> **Candidate Question:**  
> *"For facts delivered through verified-exposed channels, does the channel affect retrieval correctness compared with visible-text and absent controls?"*

### Scientific Evaluation & Verdict: **APPROVED WITH REFINEMENT**
- **Theoretical Grounding:** This question directly addresses the core flaw of prior experiments: investigating channels that were never actually exposed to the model. By restricting the study to **verified-exposed channels**, the experiment guarantees construct validity.
- **Hypothesis Formulation:**
  - $H_0$: Channel delivery mode has no effect on LLM agent fact retrieval accuracy ($\mu_{VIS} = \mu_{ARIA} = \mu_{DATA}$).
  - $H_1$: Machine-attribute channels ($ARIA$, $DATA$) exhibit lower retrieval accuracy than human-oriented visible text ($VIS$) due to prompt serialization position, lack of visual reinforcement in vision models, or tokenizer segmentation differences.
  - $H_{control}$: Fact retrieval in exposed channels significantly exceeds the absent negative control ($ABS$), proving that retrieval is driven by channel information rather than hallucination or prior knowledge.

---

## 2. Evaluation of Candidate Conditions

| Condition | Proposed Definition | Reach Audit Finding | Recommendation |
|---|---|---|---|
| **ABS** | Target fact completely absent from page | Verified 0% exposure. Valid negative control. | **RETAIN** (Essential for measuring base-rate guessing). |
| **VIS** | Fact present ONLY in visible body text | Verified 100% exposure in text and vision. | **RETAIN** (Essential positive control / human baseline). |
| **ARIA** | Fact present ONLY in `aria-label` on interactive element | Verified 100% exposure in serialized DOM under default pipeline. | **RETAIN** (Canonical accessibility channel). |
| **DATA-DEFAULT** | Fact in `data-*` attribute using default browser-use config | **0% Exposure.** Browser-use strips custom `data-*` attributes completely. | **EXCLUDE.** Identical to ABS in model prompt. Including it as an "arm" tests harness filtering, not agent comprehension. |
| **DATA-CFG** | Fact in `data-*` attribute using `include_attributes` whitelist | Verified 100% exposure on interactive elements when configured. | **RETAIN AS DISTINCT HARNESS ARM.** |
| **JSON-LD** | Fact in structured `<script type="application/ld+json">` | **0% Exposure in DOM.** Pruned by `DISABLED_ELEMENTS`. | **EXCLUDE FROM MAIN WEB-MARKUP ARMS.** Can be included only as an exploratory "Harness Augmentation" arm. |

### Recommended 4-Arm Defensible Design
To maintain rigorous scientific validity without confusing web design with browser agent hacking, we recommend a **4-arm between-condition design**:
1. **ABS (Negative Control):** Fact is omitted from the page.
2. **VIS (Visible Text Control):** Fact appears in standard body text (`<p class="spec">`).
3. **ARIA (Accessible Semantic Channel):** Fact appears in `aria-label` on the product action button (`<button aria-label="Purchase Widget Pro. Warranty: 36 months">`).
4. **DATA-CFG (Machine Attribute Channel):** Fact appears in `data-warranty="36 months"` on the button, with `include_attributes` enabled.

---

## 3. Evaluation of Candidate Tasks & Information Parity

### Why Original Tasks (T1–T5) Must Be Replaced
In T1–T5, all target facts (prices, ratings, names) were displayed as visible text on all variants. The agent had zero incentive or need to inspect ARIA or metadata.

### Evaluation of Proposed Domain Fact Tasks

| Proposed Task Fact | Metric Type | Verification Robustness | Resistance to Guessing | Information Parity Controls | Verdict |
|---|---|---|---|---|---|
| **1. Warranty Duration** | Discrete duration (e.g., 36 months vs 12, 24, 48) | Deterministic string/number match | Moderate (common numbers) | Must use non-standard duration (e.g. "38 months" or "27 months") | **APPROVED** |
| **2. Manufacturing Lot Code** | Alphanumeric token (e.g., `LOT-8842-X`) | Exact string match | Very High (un-guessable) | Synthetic pseudorandom code; zero occurrence in training data | **HIGHLY RECOMMENDED** |
| **3. Warehouse Stock Count** | Exact inventory integer (e.g., `43 units`) | Exact integer match | High | Arbitrary integer distinct from price/rating | **APPROVED** |
| **4. Extended Return Window** | Discrete days (e.g., `45 days` vs standard `30`) | Exact integer match | Moderate | Non-standard window (e.g. "48 days") | **APPROVED** |
| **5. Expedited Ship-by Date** | ISO date string (e.g., `2026-11-04`) | Exact date format | High | Specific future calendar date | **APPROVED** |
| **6. Grounded Add-to-Cart Action** | Cart state SKU match | Verified via `window.__cart__` | High | Agent must select target item based on retrieved fact | **HIGHLY RECOMMENDED** |

---

## 4. Architectural Rules for Information Parity

To prevent accidental leakage or confounding:
1. **Single-Source Invariance:** For any experimental trial, the target fact must exist in **exactly one channel**.
2. **Visual Parity:** In `ARIA` and `DATA-CFG` conditions, the fact must **not** appear in rendered text or visual screenshots.
3. **Interactive Element Placement:** Because default DOM serializers drop non-interactive containers, all attribute treatments (`aria-label`, `data-*`) must be placed on **interactive elements** (e.g. `<button>`, `<input>`, `<a>`).
4. **Token Parity:** The exact string representation of the fact (e.g., `"LOT-9821"`) must be identical across all conditions where present.
