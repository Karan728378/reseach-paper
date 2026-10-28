# Geometry Heuristic Boundary Audit: ClickableElementDetector

**Audit Date:** 2026-10-25 12:55:17 UTC  
**Target:** `browser_use.dom.serializer.clickable_elements.ClickableElementDetector.is_interactive`  
**Core Rule:** An element is classified interactive as an icon if $10 \le \text{width} \le 50$ and $10 \le \text{height} \le 50$ with an attribute in `{'class', 'role', 'onclick', 'data-action', 'aria-label'}`.

## Boundary Test Results

| Case ID | Rendered Width | Rendered Height | Within Bounds ($10 \le w, h \le 50$) | Detected Interactive | Match Expectation |
|---|---|---|---|---|---|
| `case-w9-h30` | 9px | 30px | False | **False** | MATCH (PASS) |
| `case-w10-h10` | 10px | 10px | True | **True** | MATCH (PASS) |
| `case-w30-h30` | 30px | 30px | True | **True** | MATCH (PASS) |
| `case-w50-h50` | 50px | 50px | True | **True** | MATCH (PASS) |
| `case-w51-h30` | 51px | 30px | False | **False** | MATCH (PASS) |
| `case-w30-h9` | 30px | 9px | False | **False** | MATCH (PASS) |
| `case-w30-h51` | 30px | 51px | False | **False** | MATCH (PASS) |
| `case-instock-empirical` | 48.625px | 15px | True | **True** | MATCH (PASS) |
| `case-outofstock-empirical` | 74.766px | 15px | False | **False** | MATCH (PASS) |

## Key Findings

1. **Exact Corner Inclusions:**
   - Both exact corner bounds ($10\text{px} \times 10\text{px}$ and $50\text{px} \times 50\text{px}$) are classified as **interactive**.
   - Sub-boundary elements ($9\text{px}$ width or height) and supra-boundary elements ($51\text{px}$ width or height) are classified as **non-interactive**.

2. **Empirical Stock Badge Reconciliation:**
   - The ``In Stock'' badge (`case-instock-empirical`) renders at $48.625\text{px} \times 15.0\text{px}$, which satisfies $10 \le 48.625 \le 50$ and $10 \le 15.0 \le 50$. It carries `class="product-stock in-stock"`, causing it to be assigned an interactive selector index.
   - The ``Out of Stock'' badge (`case-outofstock-empirical`) renders at $74.766\text{px} \times 15.0\text{px}$, which exceeds the $50\text{px}$ ceiling ($74.766 > 50$). Consequently, it is classified as non-interactive.
   - This boundary explains why exactly 7 of 8 product cards on `#home` produce false-positive interactive elements.
