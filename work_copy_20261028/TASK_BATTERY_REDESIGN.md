# Task Battery Redesign & DOM Serialization Gap Investigation

**Project:** The DOM Serialization Gap: Architectural Pruning, Information Loss, and Experimental Confounds in Autonomous Browser Agents  
**Timestamp:** 2026-10-24T23:26:00  
**Workspace:** `C:\testing\research_execution_20261018\`  

---

## 1. Forensic Audit of the Current Task Battery & Ceiling Effect

Across the 41 completed confirmatory runs, all trials achieved a score of **1.0 (100% success rate)** across all three treatment arms:
- `ABS` (Pruned Baseline DOM): 13 / 13 completed runs successful.
- `ARIA` (Accessibility Tree Markup): 13 / 13 completed runs successful.
- `DATA-CFG` (Extended Semantic Attributes): 15 / 15 completed runs successful.

### Root Cause: The Information Redundancy Confound
In the current website mockups (`v0-baseline`, `v2-aria`, `v3-data-attrs`), the information necessary to complete tasks T1–T6 was **redundantly duplicated in visible text nodes**:

| Task ID | Task Description | Intended Semantic Carrier | Confounding Visible DOM Text | Why Baseline Succeeded |
|---|---|---|---|---|
| **T1** | Search for 'wireless headphones' and add least expensive. | `data-amount` vs `aria-label` | `<span class="price">$49.99</span>` | Baseline serializer preserves text nodes; model reads "$49.99" directly from visible text. |
| **T2** | Find 'Mechanical Keyboard Pro' and add to cart. | `data-product-id` | `<h3>Mechanical Keyboard Pro</h3>` | Product name is in visible text; button has visible text "Add to Cart". |
| **T3** | Compare customer ratings in Audio; add second-highest. | `data-rating="4.5"` | `<span class="rating">4.5 (85 reviews)</span>` | Numerical ratings were rendered as visible text; model sorted 4.8, 4.5, 4.2 in prompt context. |
| **T4** | Search 'ErgoGlide Mouse' and complete checkout. | Form schema / `aria-*` | Standard `<input>` fields with visible labels | Standard form inputs with standard text labels are easily handled by baseline DOM serializers. |
| **T5** | Seeded cart item removal. | `data-action="remove"` | `<button class="btn">Remove</button>` | The button contained explicit visible text "Remove", making semantic attributes unneeded. |
| **T6** | Retrieve manufacturer warranty duration (Unstated). | `data-warranty` absence | Explicit lack of text on page | Agent searched page text, found no warranty mention, and generated grounded refusal. |

**Methodological Conclusion:** The original study intended to test whether pruning DOM metadata degrades agent performance. However, because the web mockups contained visible text duplicates for every piece of information, the baseline model (`ABS`) never suffered an information deficit. This created an artificial ceiling effect where no differential effect could be detected.

---

## 2. Theoretical Grounding: Where Does DOM Serialization Pruning Actually Cause Information Loss?

To evaluate the DOM serialization gap scientifically, experimental tasks must be situated where DOM pruning causes **irrecoverable information loss** in text-only autonomous browser agents (`use_vision=False`).

In modern web development, critical task information is frequently detached from visible text nodes in four distinct architectural patterns:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   GENUINE DOM SERIALIZATION FAILURE ARCHETYPES                   │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 1. Icon-Only Action Affordances (No visible text in button)                      │
│    - Baseline (ABS):  <button class="icon-btn"><svg ...></svg></button>         │
│    - ARIA:            <button class="icon-btn" aria-label="Remove item">...      │
│    - DATA-CFG:        <button class="icon-btn" data-action="remove-item">...     │
│    -> Loss in ABS: Model sees empty/opaque button; cannot distinguish action.    │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 2. Visual-Only Glyphs & State Indicators (Color/Icon indicators)                 │
│    - Baseline (ABS):  <span class="stock-badge in-stock"><svg></svg></span>      │
│    - ARIA:            <span class="stock-badge" aria-label="In Stock">...        │
│    - DATA-CFG:        <span class="stock-badge" data-stock="in-stock">...        │
│    -> Loss in ABS: Model cannot observe stock status without text or attributes. │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 3. Non-Standard Custom Widgets (Accessible Role & State Asymmetry)               │
│    - Baseline (ABS):  <div class="custom-radio selected"><span>Express</span>    │
│    - ARIA:            <div role="radio" aria-checked="true"><span>Express</span> │
│    - DATA-CFG:        <div class="custom-radio" data-selected="true">...         │
│    -> Loss in ABS: Model cannot determine selection state of custom controls.    │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 4. Pruned Complex Metadata (Microdata / Technical Attributes)                    │
│    - Baseline (ABS):  Pruned custom technical specs (voltage, warranty SKU)      │
│    - ARIA:            aria-description / aria-details reference                  │
│    - DATA-CFG:        Extended data attributes preserved                         │
│    -> Loss in ABS: Pruned attributes are absent from serialized prompt tree.     │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Redesigned Task Battery (Hypotheses & Specifications)

> [!NOTE]
> All proposed tasks, difficulty levels, and failure modes are **theoretical hypotheses**. In accordance with scientific integrity guidelines, no empirical failure rates are fabricated or assumed prior to live execution.

### Task Archetype 1: Icon-Only Affordance Discrimination (Action Loss)
- **Proposed Task T1-REV:** *"Navigate to your cart. There are two items. Click the button to remove the 'SoundFlow Air 3' without clearing or modifying other items."*
- **DOM Implementation:**
  - Cart row contains three icon buttons side-by-side: Save for Later (bookmark icon), Remove (trash icon), and Quantity (chevron icon).
  - In `ABS`: Buttons contain only SVG glyphs (`<button class="action-btn"><svg>...</svg></button>`).
  - In `ARIA`: Buttons have standard accessible names (`aria-label="Remove item"`, `aria-label="Save for later"`).
  - In `DATA-CFG`: Buttons have extended attributes (`data-action="remove"`, `data-action="save"`).
- **Hypothesis H1:** In the `ABS` arm, text-only browser agents will exhibit action disorientation (clicking incorrect icons or guessing), causing a measurable drop in task success compared to `ARIA` and `DATA-CFG`.

### Task Archetype 2: Visual Glyph State Discrimination (State Loss)
- **Proposed Task T2-REV:** *"Search for 'mechanical keyboard'. Two models appear. Add the keyboard that is currently In Stock to your cart."*
- **DOM Implementation:**
  - Both keyboards list identical prices. Stock availability is indicated solely by a visual badge: green checkmark icon for In Stock, red exclamation icon for Backordered / Out of Stock (no visible text "In Stock").
  - In `ABS`: Visual SVGs are stripped of semantics; no text indicates availability.
  - In `ARIA`: Badge carries `role="status"` and `aria-label="In Stock"` / `aria-label="Out of Stock"`.
  - In `DATA-CFG`: Badge carries `data-stock-status="in-stock"` / `data-stock-status="out-of-stock"`.
- **Hypothesis H2:** In the `ABS` arm, text-only agents cannot differentiate stock availability, leading to a 50% random guessing rate or grounded refusal, whereas `ARIA` and `DATA-CFG` will maintain high task completion.

### Task Archetype 3: Custom Widget State Discrimination (Affordance Loss)
- **Proposed Task T3-REV:** *"Proceed to checkout. In the Shipping Method section, select the 'Overnight Express' shipping option and verify its selection before placing the order."*
- **DOM Implementation:**
  - Shipping options are implemented as styled `div` card elements (custom radio buttons).
  - In `ABS`: `<div>` elements contain visible text ("Standard $4.99", "Overnight $14.99"), but selected state is communicated purely via CSS classes (`.is-active`, `.selected`).
  - In `ARIA`: Elements have standard WAI-ARIA pattern: `role="radio"`, `aria-checked="true"` / `aria-checked="false"`.
  - In `DATA-CFG`: Elements have `data-selected="true"`.
- **Hypothesis H3:** In `ABS`, agents will struggle to verify whether a click registered or which option is currently active, resulting in higher step counts or incorrect order placement.

### Task Archetype 4: Ranked Attribute Comparison Without Visible Text
- **Proposed Task T4-REV:** *"Navigate to the Audio category. Three products are displayed with star rating glyphs (no visible numbers). Add the product with the highest customer rating to your cart."*
- **DOM Implementation:**
  - Product cards display 5 SVG star icons (filled vs empty), without visible numerical text.
  - In `ABS`: SVGs are serialized as generic graphics without star counts.
  - In `ARIA`: Rating container carries `role="img" aria-label="4.8 out of 5 stars"`.
  - In `DATA-CFG`: Rating container carries `data-rating="4.8"`.
- **Hypothesis H4:** In `ABS`, agents will be blind to the quantitative rating value, forcing random selection or exploration failure, while `ARIA` and `DATA-CFG` supply the necessary scalar rating.

---

## 4. Objective, Non-Exploitative Measurement Framework

To prevent creating tasks that merely "trick" the verifier or rely on contrived puzzles:
1. **Real-World Ecological Validity:** All proposed DOM patterns (icon buttons, visual stock badges, star glyphs, custom selectable cards) represent standard design patterns observed in production web applications (e.g., Amazon, Shopify, Airbnb).
2. **Multidimensional Measurement Matrix:**
   - **Primary Metric:** Binary ground-truth completion ($Y \in \{0, 1\}$), verified independently via browser state (cart contents, order confirmation ID).
   - **Efficiency Metrics:** Total action steps, navigation trajectory length, cumulative token consumption.
   - **Cognitive Failure Taxonomy:**
     - *Disorientation Error:* Clicking an incorrect action button when options are indistinguishable.
     - *Hallucination Error:* Generating confident assertions about visual states that were pruned from the observation.
     - *Thrashing / Stagnation:* Repeated scrolling or navigating in search of lost information.
