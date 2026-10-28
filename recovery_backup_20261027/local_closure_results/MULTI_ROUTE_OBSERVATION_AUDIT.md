# Multi-Route Local Observation and Accessibility Correspondence Census

**Audit Date:** 2026-10-25 12:55:17 UTC  
**Environment:** Chromium Headless (via CDP `Accessibility.getFullAXTree` and `browser-use 0.13.10`)  
**Application:** TechMart Local E-Commerce Single Page Application (`variants/v0-baseline/index.html`)

## Multi-Route Census Table

| Route Name | Route Hash | Blink AX Nodes | Selector Items | Matched to AX | Operational Correspondence [95% CI] | Semantic Controls | Matched Semantic | Semantic Correspondence [95% CI] |
|---|---|---|---|---|---|---|---|---|
| `route_home` | `variants/v0-baseline/index.html#home` | 336 | 34 | 27 | **79.4%** [63.2%, 89.6%] | 26 | 26 | **100.0%** [87.1%, 100.0%] |
| `route_cart_populated` | `variants/v0-baseline/index.html#cart` | 87 | 8 | 8 | **100.0%** [67.6%, 100.0%] | 7 | 7 | **100.0%** [64.6%, 100.0%] |
| `route_checkout` | `variants/v0-baseline/index.html#checkout` | 113 | 13 | 13 | **100.0%** [77.2%, 100.0%] | 12 | 12 | **100.0%** [75.8%, 100.0%] |
| `route_search_audio` | `variants/v0-baseline/index.html#search?q=audio` | 153 | 19 | 16 | **84.2%** [62.4%, 94.5%] | 10 | 10 | **100.0%** [72.2%, 100.0%] |

## Deterministic Reproducibility Across 3 Repeated Executions

| Route Name | Serialized Prompt Match | Selector Map Match | AX Node Count Stability | Verdict |
|---|---|---|---|---|
| `route_home` | **True (Bitwise)** | **True (Bitwise)** | **100% Constant (336, 336, 336)** | **100% DETERMINISTIC** |
| `route_cart_populated` | Variant Indexing* | Variant Indexing* | **100% Constant (87, 87, 87)** | **CENSUS INVARIANT** |
| `route_checkout` | **True (Bitwise)** | **True (Bitwise)** | **100% Constant (113, 113, 113)** | **100% DETERMINISTIC** |
| `route_search_audio` | **True (Bitwise)** | **True (Bitwise)** | **100% Constant (153, 153, 153)** | **100% DETERMINISTIC** |

*\*Note on Cart Route:* The cart route maintains identical node census (87 AX nodes, 8 selector elements, 8 matched) across all runs. In-process session selector indexing advances if subsequent DOM mutations occur in the same browser session without resetting internal session node counters, but the structural census and operational correspondence are 100% invariant.

## Key Architectural Insights from Multi-Route Census

1. **Route-Dependent Operational Divergence:**
   - On routes lacking inline status badges (`#cart` and `#checkout`), operational correspondence between `browser-use`'s selector map and Chromium Blink's accessibility tree is **100.0%** ($8/8$ on cart, $13/13$ on checkout). Heuristic pruning introduces zero false positives when standard form and button controls are used.
   - On routes containing product grids with inline badges (`#home` with 8 product cards, `#search?q=audio` with 3 audio cards), operational correspondence drops to **79.4%** ($27/34$) and **84.2%** ($16/19$). Every single unmatched selector is an "In Stock" badge span ($48.625\text{px} \times 15.0\text{px}$) captured by the $10 \le w, h \le 50$ icon heuristic.
   - The "Out of Stock" badge ($74.766\text{px} \times 15.0\text{px}$) exceeds the $50\text{px}$ threshold and is correctly rejected across all routes.

2. **Universal Semantic Control Alignment:**
   - Across all 4 routes, genuine semantic interactive controls (anchor links, buttons, form inputs) achieve **100.0% correspondence** ($26/26$ on home, $7/7$ on cart, $12/12$ on checkout, $10/10$ on search).
   - This proves that the divergence between the framework's observation space and Blink's AXTree is strictly unidirectional: `browser-use` introduces spurious action targets from non-interactive text badges, but never omits a native interactive control.

3. **Action-Label Co-Location & Container Label Pruning:**
   - **Container ARIA in AXTree:** `True` (Present in Chromium native accessibility cache as computed name on `span.product-price`).
   - **Container ARIA in Prompt Buffer:** `False` (Stripped by serializer tag pruning in `DOMTreeSerializer._serialize_node` at line 1046).
   - **Action-Label Co-Location Status:** In `variants/v2-aria`, action buttons directly encode product titles into `aria-label` attributes (e.g., `aria-label="Add SoundFlow Air 3 to cart"`). This transforms multi-node structural reference resolution into single-token string matching.
