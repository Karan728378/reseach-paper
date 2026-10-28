# CROSS-FRAMEWORK ARCHITECTURAL AUDIT & FEASIBILITY ANALYSIS

**Target:** Comparative Systems Audit across Autonomous Browser Observation Pipelines  
**Frameworks Evaluated:** `browser-use 0.13.10`, `BrowserGym`, `Stagehand`, `Playwright MCP`  
**Host Workspace:** `C:\testing\research_execution_20261018`  
**Audit Date:** 2026-10-25  

---

## 1. Architectural Scope & Ground Rules

To ensure strict scientific credibility:
1. **Zero Fabricated Benchmarks:** We do **not** report cross-framework task success rates, win-rates, or execution latencies unless the identical task suite has been executed live under identical network and model conditions.
2. **Architectural Code Audit:** Comparisons are restricted to documented observation pipelines, tree serialization algorithms, action space mappings, and tool reachability.
3. **Environment Isolation:** No unvetted external packages were installed into `.venv311` to prevent dependency contamination.

---

## 2. Comparative Observation Pipeline Matrix

| Architectural Dimension | `browser-use 0.13.10` | `BrowserGym` (v0.3+) | `Stagehand` (v1.0+) | `Playwright MCP` |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Observation Source** | Live DOM recursive traversal via Playwright JS | Dual: Chromium AXTree snapshot + raw/pruned HTML | Playwright locator snapshots (`page.locator`) | Chrome DevTools Protocol (CDP) Page/DOM snapshot |
| **AXTree Integration** | Parallel query (`getFullAXTree`) used for role lookup; does not prune DOM | Primary modality; serialized as indented accessibility hierarchy | Secondary; relies primarily on visible accessibility roles | Direct CDP access via `Accessibility.getFullAXTree` |
| **Interactive Element Identification** | Geometric heuristic ($10 \le w, h \le 50$px + class) and tag whitelist | Accessibility tree clickable roles and explicit `bid` assignment | Hybrid LLM locator extraction and Playwright visibility filters | CDP node resolution via `backendNodeId` |
| **Action Space Mapping** | Numeric selector index (`[index]`) mapped to pixel center | `bid` (browser-gym identifier) or coordinate click/type | Natural language intent translated to Playwright locators | Tool-call functions (`click`, `fill`, `navigate`) |
| **Dynamic Tool Execution** | `evaluate_script`, `click_element`, `extract_content` | Python Gym environment actions (`step(action)`) | Autonomous `act()`, `extract()`, `observe()` primitives | Granular MCP tool server calls |
| **Offline Reproducibility in Current Setup** | **Fully Verified & Installed** (`browser-use 0.13.10`) | Architectural specification verified via cached documentation | Architectural specification verified via cached documentation | Architectural specification verified via CDP protocol spec |
| **Requires Live Infrastructure?** | No for offline tests; Yes for live model agent runs | Yes (requires separate package installation and live API) | Yes (requires Node.js / Playwright / Browserbase service) | Yes (requires running MCP server process and client) |

---

## 3. Key Architectural Divergences

### A. The Action-Target Identification Strategy
- **`browser-use`:** Employs an aggressive client-side geometric heuristic ($10 \le w, h \le 50\text{px}$ with class attributes) to detect icon buttons. As demonstrated in Section 4.2 of the manuscript, this heuristic introduces false-positive interactive targets for static text badges ($27/34$ correspondence on route `#home`).
- **`BrowserGym`:** Bypasses DOM geometric bounding box heuristics by constructing its observation hierarchy directly from the Chromium AXTree (`bid` system). This eliminates false positives from non-interactive text spans, but risks omitting custom un-annotated controls that lack standard ARIA roles.
- **`Stagehand`:** Offloads target element identification to Playwright's smart locators and an initial LLM `observe()` pass, shifting the computational burden from deterministic rules to model inference.

### B. Omission vs. Tool Reachability Across Frameworks
All four frameworks prune non-rendered elements (`<script>`, `<style>`) from the initial observation to minimize prompt token overhead. However, all four frameworks provide execution channels (e.g., `evaluate_script` in browser-use, CDP evaluation in Playwright MCP) allowing an agent to query hidden metadata if explicitly instructed.

---

## 4. Feasibility of Follow-Up Cross-Framework Empirical Study

To execute an apples-to-apples empirical benchmark in a future funded study:
1. **Standardized Task Harness:** Adapt the 4-arm randomized block design (Protocol v4 RCBD) to expose identical synthetic e-commerce and web benchmark routes to all four framework agents.
2. **Fixed Model Provider:** Lock the reasoning model across all frameworks (e.g., Gemini 2.5 Flash Lite or Claude 3.5 Sonnet) at identical temperature ($0.0$) and context limits.
3. **Execution Guardrails:** Require identical local request budgeting and cost ceilings ($0.00 spend on free tiers).
4. **Current Status:** Proposed for future confirmatory research; unexecuted in current repository state.
