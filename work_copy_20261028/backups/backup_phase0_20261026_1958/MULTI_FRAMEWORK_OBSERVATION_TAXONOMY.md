# Multi-Framework Observation Pipeline Systems Audit

## 1. Overview and Scope
This audit evaluates how modern autonomous browser-agent frameworks and underlying browser APIs process and serialize semantically enriched HTML documents. Testing is conducted using a shared, deterministic local fixture (`fixtures/multi_framework_observation_fixture.html`) containing 7 distinct semantic layers:
1. Schema.org JSON-LD in a `<script type="application/ld+json">` element
2. Interactive control (`<button>`) with an explicit `aria-label`
3. Non-interactive container (`<span>`) with an `aria-label`
4. Custom developer attribute (`data-product-id="target-sku-101"`) on an interactive button
5. Visible rendered typography
6. Nested interactive control (`<a><button>...</button></a>`)
7. Hidden control (`style="display: none;" aria-hidden="true"`)

## 2. Comparative Systems Taxonomy

| Framework/version | Observation method | JSON-LD retained? | Interactive aria-label retained? | Non-interactive span aria-label retained? | data-* retained? | Visible text retained? | Test method | Evidence | Limitations |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :--- |
| Static DOM Parser (bs4/lxml) | Full DOM AST parse (tree walk, zero layout engine) | **YES** | **YES** | **YES** | **YES** | **YES** | Local execution on multi_framework_observation_fixture.html | `Observed in local execution` | No dynamic JS execution, no computed CSS styling/visibility, lacks actionability mapping. |
| Chromium Blink AXTree (CDP Accessibility.getFullAXTree) | Native accessibility tree compiled by browser engine (roles, accessible names, states) | NO | **YES** | **YES** | NO | **YES** | Local execution via CDP session on multi_framework_observation_fixture.html | `Observed in local execution` | Excludes non-standard attributes (data-*), strips script tags; non-interactive nodes may require explicit accessible roles to avoid generic pruning. |
| browser-use 0.13.10 (Default) | Interactive DOM serialization with DEFAULT_INCLUDE_ATTRIBUTES whitelist | NO | **YES** | NO | NO | **YES** | Local execution on multi_framework_observation_fixture.html | `Observed in local execution` | Prunes script/style/meta tags via DISABLED_ELEMENTS; filters out non-whitelisted attributes; strips tags of non-interactive elements. |
| browser-use 0.13.10 (Extended Whitelist) | Interactive DOM serialization with EXTENDED_ATTRIBUTES whitelist (runner patch) | NO | **YES** | NO | **YES** | **YES** | Local execution on multi_framework_observation_fixture.html | `Observed in local execution` | Retains data-* on interactive nodes only; still prunes script/meta and strips non-interactive container tags. |
| Playwright (page.accessibility.snapshot / aria_snapshot) | W3C Accessibility Tree snapshot / YAML aria_snapshot locator abstraction | NO | **YES** | **YES** | NO | **YES** | Source code and API specification inspection (playwright.dev/python/docs/api/class-accessibility) | `Unsupported in current environment` | Package playwright is not installed in .venv311. Cannot serialize non-standard DOM attributes. |
| BrowserGym (browsergym.core 0.3.x) | Hybrid AXTree extraction ('axtree_txt') or pruned HTML extraction via Playwright harness | NO | **YES** | **YES** | NO | **YES** | Source code inspection of browsergym/core/observation.py | `Unsupported in current environment` | Package browsergym is not installed in .venv311. Requires Playwright backend. |

## 3. Strict Evidence Label Definitions
- `Observed in local execution`: Empirical observation extracted directly from executing code in the local Python `.venv311` environment on `fixtures/multi_framework_observation_fixture.html`.
- `Verified by source inspection only`: Architectural capability or behavior verified through static inspection of upstream framework source code and official API specifications without local execution.
- `Not tested`: Potential configuration or framework variant not evaluated in this audit.
- `Unsupported in current environment`: Framework is not installed or available in the local execution environment (`.venv311`), precluding dynamic execution.

## 4. Key Systems Findings
1. **The JSON-LD Universal Blindspot:**
   - Neither `browser-use 0.13.10` nor the Chromium Blink AXTree retains `<script type="application/ld+json">` structured data.
   - Browser-use prunes `<script>` tags via `DISABLED_ELEMENTS` in `build_dom_tree.js`.
   - Blink AXTree ignores `<script>` elements because they do not participate in layout or accessibility trees.
   - Consequently, autonomous web agents cannot observe Schema.org microdata unless static scraping or custom DOM injection is explicitly executed.

2. **Custom Developer Attributes (`data-*`):**
   - Stripped by default in `browser-use 0.13.10` (`DEFAULT_INCLUDE_ATTRIBUTES` whitelist).
   - Retained only when an extended whitelist (`EXTENDED_ATTRIBUTES`) is injected at the runner level.
   - Completely absent in Chromium Blink AXTree and Playwright accessibility snapshots, as `data-*` attributes are not part of the W3C Accessible Rich Internet Applications (WAI-ARIA) specification.

3. **Non-Interactive Container ARIA:**
   - In Chromium Blink AXTree, an `aria-label` on a non-interactive `<span>` forces the layout engine to construct an accessible generic/group node.
   - In `browser-use 0.13.10`, non-interactive tags are stripped of element wrappers and emitted purely as text; their `aria-label` is discarded unless promoted or configured.

4. **Hidden Control Pruning:**
   - Both Chromium AXTree and `browser-use` prune `display: none` / `aria-hidden="true"` elements from the agent's observation space, preventing false-positive actions on non-actionable elements.
   - Static parsers (e.g. BeautifulSoup) retain hidden elements because they lack CSS layout evaluation.

## 5. Architectural Implications for Web Agent Benchmarking
Benchmarks evaluating agent performance across semantic treatments must distinguish between **behavioral agent failure** and **observation-pipeline reachability failure**.
If a benchmark modifies `data-*` or JSON-LD without verifying observation-channel reachability in the target framework, the agent is tested under an unmanipulated baseline, rendering treatment conclusions invalid.