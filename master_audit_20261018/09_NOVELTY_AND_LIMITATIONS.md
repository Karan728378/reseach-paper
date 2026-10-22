# Novelty Assessment & Limitations
**Audit Date:** 2026-10-18

## Novelty Claim
**INFERRED (not yet independently verified against full literature):**

This study proposes the first controlled experiment measuring how the HTML information channel
(visible text, ARIA attributes, data-* attributes, JSON-LD metadata) independently affects
browser-based LLM agent task performance. Existing benchmarks (WebArena, Mind2Web, SeeAct)
measure task success but do not manipulate or isolate the markup channel through which
information is delivered.

## Related Work (Not Exhaustive)
| Work | Relevance | Gap |
|------|-----------|-----|
| WebArena (Zhou et al. 2023) | Realistic browser agent benchmark | Does not isolate HTML channel |
| Mind2Web (Deng et al. 2023) | Cross-website generalization | Offline; no channel manipulation |
| SeeAct (Zheng et al. 2024) | Vision-augmented web agents | Compares text+vision vs vision; not HTML channels |
| ScreenAgent / WebAgent | End-to-end web automation | No channel isolation |

## Internal Validity Threats

| Threat | Severity | Status |
|--------|----------|--------|
| v1-jsonld arm blocked by DISABLED_ELEMENTS | CRITICAL | Confirmed |
| v3-data-attrs stripped by DEFAULT_INCLUDE_ATTRIBUTES | CRITICAL | Confirmed |
| T3/T4/T5 verifier flaws | CRITICAL | Confirmed |
| Sequential blocking + quota truncation | CRITICAL | Confirmed |
| Vision confound (use_vision=True) | MODERATE | Confirmed risk |
| Single-agent generalizability | MODERATE | Inherent design limit |

## External Validity Limitations
1. **Single agent stack**: browser-use 0.13.10 + Gemini. Results may differ substantially
   with GPT-4, Claude, or other browser-agent frameworks.
2. **Single controlled website**: TechMart is purpose-built. Real sites have dynamic JS,
   shadow DOM, lazy-loaded content, and inconsistent ARIA implementation.
3. **Small product catalog**: 8 SKUs. Sites with hundreds of products may exhibit different
   search/navigation patterns.
4. **English only**: ARIA and visible-text channel effects may differ across languages.

## Ethical Considerations
- No real users or accounts involved.
- No real financial transactions (test card data).
- All LLM API calls use test/research API key.
- No PII collected or processed.
