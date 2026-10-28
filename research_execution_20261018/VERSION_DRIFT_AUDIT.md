# VERSION-DRIFT AUDIT: BROWSER-USE OBSERVATION PIPELINE
**Date (UTC):** 2026-10-27T13:43:19.236154+00:00  
**Methodology:** Forensic static code inspection of official PyPI binary distributions (`.whl`) across the development lifecycle of `browser-use` (v0.1.0 to v0.13.11).  
**Integrity:** Every downloaded binary verified byte-for-byte against PyPI cryptographic digests.  

---

## 1. Verified Binary Manifest

| Release Version | PyPI Wheel Filename | SHA-256 Digest (Verified) | Wheel Size | Digest Match |
|---|---|---|:---:|:---:|
| **`0.1.0`** | `browser_use-0.1.0-py3-none-any.whl` | `d9839f0e22cdb00cfdc0962b...` | 24,191 bytes | **PASS** |
| **`0.5.0`** | `browser_use-0.5.0-py3-none-any.whl` | `a42e72103dc425810c856e83...` | 280,060 bytes | **PASS** |
| **`0.13.0`** | `browser_use-0.13.0-py3-none-any.whl` | `afb80ceb2ef8f841b82f8c9d...` | 772,539 bytes | **PASS** |
| **`0.13.5`** | `browser_use-0.13.5-py3-none-any.whl` | `530ea9a89da22222c3576d4a...` | 714,245 bytes | **PASS** |
| **`0.13.10`** | `browser_use-0.13.10-py3-none-any.whl` | `66eb20153094f21728bc0110...` | 731,335 bytes | **PASS** |
| **`0.13.11`** | `browser_use-0.13.11-py3-none-any.whl` | `50b0d16efc44215f99ed1c91...` | 753,512 bytes | **PASS** |

---

## 2. Cross-Version Architectural Invariants

| Architectural Feature | v0.1.0 (Initial) | v0.5.0 | v0.13.0 | v0.13.5 | v0.13.10 (Pinned) | v0.13.11 (Latest) | Longitudinal Status |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **`DISABLED_ELEMENTS` Prunes `<script>` & `<meta>`** | **YES** | **YES** | **YES** | **YES** | **YES** | **YES** | **IMMUTABLE INVARIANT** |
| **JSON-LD Unconditionally Stripped at Stage 2** | **YES** | **YES** | **YES** | **YES** | **YES** | **YES** | **IMMUTABLE INVARIANT** |
| **Developer `data-*` Omitted from Default Whitelist** | **YES** | **YES** | **YES** | **YES** | **YES** | **YES** | **IMMUTABLE INVARIANT** |
| **Non-Interactive Container Tag Stripping (L1046)** | N/A | **YES** | **YES** | **YES** | **YES** | **YES** | **STABLE MECHANISM** |
| **Geometric Icon Heuristic ($10 \le w, h \le 50\text{px}$)** | NO | NO | **YES** | **YES** | **YES** | **YES** | **ESTABLISHED IN 0.13 SERIES** |
| **Circularity: ClickableElementDetector queries `ax_node.role`** | NO | NO | **YES** | **YES** | **YES** | **YES** | **ESTABLISHED IN 0.13 SERIES** |

---

## 3. Analysis of Architectural Stability vs. Version Drift

### A. The Core Invariants: JSON-LD, Meta, and Developer Attributes
Across all audited versions spanning the entire repository history from v0.1.0 to v0.13.11:
1. `DISABLED_ELEMENTS` has consistently contained `{'style', 'script', 'head', 'meta', 'link', 'title'}`.
   - **Conclusion:** The elimination of Schema.org JSON-LD and OpenGraph `<meta>` tags is **not** an incidental quirk of v0.13.10, but an immutable architectural design decision across the entire `browser-use` framework family.
2. `DEFAULT_INCLUDE_ATTRIBUTES` has never included developer `data-*` attributes (`data-product-id`, `data-sku`, `data-amount`).
   - **Conclusion:** The pruning of custom attributes is an architectural invariant. Benchmarks attempting to evaluate `data-*` enrichment without explicitly expanding `DEFAULT_INCLUDE_ATTRIBUTES` test unmanipulated baselines across *all* versions.

### B. Architectural Evolution in the v0.13 Series
1. **Introduction of Geometric Icon Detection:**
   - Early versions (v0.1.x–v0.5.x) relied solely on native HTML interactive tags (`<a>`, `<button>`, `<input>`).
   - The v0.13 series introduced bounding-box heuristics ($10 \le w, h \le 50\text{px}$) to identify unsemantic icon buttons. As demonstrated in our geometry boundary audit, this heuristic introduces systematic false-positive action targets on small text spans and badges (e.g. 48.6px in-stock badges).
2. **Chromium AXTree Integration & Circularity:**
   - The v0.13 series coupled `ClickableElementDetector` to `node.ax_node.role` from the CDP accessibility tree.
   - This coupling creates circularity: any correspondence between the framework's selector map and Blink's AXTree is structurally guaranteed by the framework's reliance on AX roles for interactivity classification.

---
**Audit Status:** Fully verified against PyPI binaries. No model calls or live execution required.  