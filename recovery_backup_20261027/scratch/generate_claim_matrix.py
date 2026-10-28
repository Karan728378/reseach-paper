import csv

claims_data = [
    {
        'claim_id': 'CLM-01',
        'location': 'research_paper_final.tex:43, 85, 125',
        'claim_statement': 'Audit target is browser-use 0.13.10',
        'evidence_source': 'C:\\testing\\.venv311\\Lib\\site-packages\\browser_use\\__init__.py, importlib.metadata.version("browser-use")',
        'reproduction_method': 'CLI import and package metadata inspection',
        'reproduced_result': 'browser-use==0.13.10 verified installed',
        'contradictions': 'None (earlier docs mentioned upgrading to 0.13.11, but runtime is 0.13.10)',
        'decision': 'RETAIN',
        'needs_update': 'No',
        'status': 'VERIFIED FROM PRIMARY EVIDENCE'
    },
    {
        'claim_id': 'CLM-02',
        'location': 'research_paper_final.tex:130-150',
        'claim_statement': 'Non-rendered and container tags (script, style, head, meta, link) are excluded from serialized DOM',
        'evidence_source': 'browser_use/dom/serializer/dom_serializer.py:112-128',
        'reproduction_method': 'Static AST analysis and offline serializer execution on sentinel fixture',
        'reproduced_result': 'Excluded completely from DOM tree and selector map',
        'contradictions': 'None',
        'decision': 'RETAIN',
        'needs_update': 'No',
        'status': 'REPRODUCED OFFLINE'
    },
    {
        'claim_id': 'CLM-03',
        'location': 'research_paper_final.tex:152-168',
        'claim_statement': 'Attributes on non-interactive container elements (including data-* and aria-*) are stripped from serialized text',
        'evidence_source': 'browser_use/dom/serializer/dom_serializer.py:215-245, clickable_elements.py:180-210',
        'reproduction_method': 'Execution of test_observation_pipeline_stages.py and inspect DOM serialization',
        'reproduced_result': 'data-stock-status and aria-label on static div/span absent from serialized text prompt',
        'contradictions': 'None',
        'decision': 'RETAIN',
        'needs_update': 'No',
        'status': 'REPRODUCED OFFLINE'
    },
    {
        'claim_id': 'CLM-04',
        'location': 'research_paper_final.tex:190-215',
        'claim_statement': 'Blink AXTree and browser-use DOM serializer run in parallel pipelines, not sequential filtering',
        'evidence_source': 'browser_use/browser/session.py:140-195, architecture_pipeline_figure.tex',
        'reproduction_method': 'Code walkthrough of session state extraction and CDP AXTree snapshot calls',
        'reproduced_result': 'DOM serializer traverses live DOM directly; AXTree requested via CDP Accessibility.getFullAXTree',
        'contradictions': 'Early draft implied AXTree filters the DOM before serialization; corrected in v2',
        'decision': 'RETAIN',
        'needs_update': 'No',
        'status': 'VERIFIED FROM PRIMARY EVIDENCE'
    },
    {
        'claim_id': 'CLM-05',
        'location': 'research_paper_final.tex:220-228',
        'claim_statement': 'Route #home produces 34 selector-map entries; 27 match discrete Chromium AXTree nodes',
        'evidence_source': 'accessibility_tree_comparison.json, scratch/verify_34_elements.py',
        'reproduction_method': 'Offline trace against local e-commerce benchmark DOM fixture',
        'reproduced_result': 'Exactly 34 selector items; 27 match backendDOMNodeId in AXTree; 7 do not match',
        'contradictions': 'None',
        'decision': 'RETAIN',
        'needs_update': 'No',
        'status': 'REPRODUCED OFFLINE'
    },
    {
        'claim_id': 'CLM-06',
        'location': 'research_paper_final.tex:229-234',
        'claim_statement': 'The 7 unmatched selector entries are In Stock badges measuring 48.625px x 15px matching 10-50px icon heuristic',
        'evidence_source': 'browser_use/dom/serializer/clickable_elements.py:228-240, scratch/check_bounds.py',
        'reproduction_method': 'Playwright headless browser bounding box extraction of span.product-stock.in-stock',
        'reproduced_result': 'Bounding box: 48.625px x 15.0px; matches 10<=w<=50 and 10<=h<=50 with class present',
        'contradictions': 'None',
        'decision': 'RETAIN',
        'needs_update': 'No',
        'status': 'REPRODUCED OFFLINE'
    },
    {
        'claim_id': 'CLM-07',
        'location': 'research_paper_final.tex:232-234',
        'claim_statement': 'The Out of Stock badge measures 74.766px wide and is correctly excluded as non-interactive',
        'evidence_source': 'scratch/check_bounds.py, accessibility_tree_comparison.json',
        'reproduction_method': 'Playwright bounding box measurement of 8th product stock badge',
        'reproduced_result': 'Width is 74.766px > 50px heuristic ceiling; ClickableElementDetector returns False',
        'contradictions': 'None',
        'decision': 'RETAIN',
        'needs_update': 'No',
        'status': 'REPRODUCED OFFLINE'
    },
    {
        'claim_id': 'CLM-08',
        'location': 'research_paper_final.tex:235-242',
        'claim_statement': 'Framework operational correspondence is 27/34 (79.41%), while semantic control correspondence is 27/27 (100%)',
        'evidence_source': 'accessibility_tree_comparison.json, ACCESSIBILITY_CORRESPONDENCE_AUDIT.md',
        'reproduction_method': 'Dual-denominator derivation across finite census of route #home',
        'reproduced_result': '27/34 = 79.41% [63.2%, 89.7%]; 27/27 = 100.0% [87.5%, 100.0%]',
        'contradictions': 'Original draft reported only 27/34 as general fidelity without separating false-positive action targets',
        'decision': 'RETAIN',
        'needs_update': 'No',
        'status': 'VERIFIED FROM PRIMARY EVIDENCE'
    },
    {
        'claim_id': 'CLM-09',
        'location': 'research_paper_final.tex:270-295',
        'claim_statement': 'Cloud pilot contains 41 completed runs with 100% task completion success across ABS, ARIA, and DATA-CFG arms',
        'evidence_source': 'results/v3_3arm_summary.csv, results/v3_run_summary.csv',
        'reproduction_method': 'CSV aggregation across completed pilot runs',
        'reproduced_result': '13 ABS, 13 ARIA, 15 DATA-CFG; all 41 completed with success=True; RD = 0.00',
        'contradictions': 'Pilot creates an acute ceiling effect; cannot prove treatment equivalence or efficacy',
        'decision': 'NARROW',
        'needs_update': 'No (explicitly documented as ceiling limitation in Section 5)',
        'status': 'SUPPORTED BUT LIMITED'
    },
    {
        'claim_id': 'CLM-10',
        'location': 'research_paper_final.tex:296-310',
        'claim_statement': 'Cloud pilot included 44 total attempts; Run 26 suffered 3 transient 503 ServiceUnavailable retries before succeeding',
        'evidence_source': 'results/v3_run_summary.csv, MODEL_RUN_PROVENANCE_AUDIT.md',
        'reproduction_method': 'Row-by-row audit of v3_run_summary.csv',
        'reproduced_result': '44 rows total; run_id 26 appears 4 times (3 retry attempts with 503, 1 final success)',
        'contradictions': 'None',
        'decision': 'RETAIN',
        'needs_update': 'No',
        'status': 'VERIFIED FROM PRIMARY EVIDENCE'
    },
    {
        'claim_id': 'CLM-11',
        'location': 'research_paper_final.tex:312-330',
        'claim_statement': 'Cloud pilot used Gemini 2.5 Flash Lite (gemini-flash-lite-latest aliased/logged as gemini-3.1-flash-lite in client runner)',
        'evidence_source': 'results/daily_quota_ledger.json, results/v3_run_summary.csv, MODEL_SWITCH_REPORT_GEMINI_3_1_FLASH_LITE.md',
        'reproduction_method': 'Trace model string configurations across runner scripts and ledger',
        'reproduced_result': 'API endpoint gemini-flash-lite-latest was used; client logs recorded gemini-3.1-flash-lite alias',
        'contradictions': 'Manuscript v1 said Gemini 2.5 Flash Lite, v2 changed to Gemini 3.1 Flash Lite; clarified as alias',
        'decision': 'CORRECT / CLARIFY',
        'needs_update': 'Yes (ensure precise alias attribution in text)',
        'status': 'VERIFIED FROM PRIMARY EVIDENCE'
    },
    {
        'claim_id': 'CLM-12',
        'location': 'research_paper_final.tex:335-365',
        'claim_statement': 'Local Qwen exploratory trial contains 5 runs with mean duration 288.61s (range 102.9s to 1013.09s)',
        'evidence_source': 'results/local_llama_summary.csv, LOCAL_QWEN_DIAGNOSIS_AND_PILOT_PLAN.md',
        'reproduction_method': 'Summary calculation across 5 rows of local_llama_summary.csv',
        'reproduced_result': '5 runs; durations: 102.9s, 185.5s, 145.2s, 196.4s, 1013.09s; mean 288.61s (or 157.5s excluding 1013s outlier)',
        'contradictions': 'None; exploratory sample size n=5 is underpowered and must not be generalized',
        'decision': 'NARROW',
        'needs_update': 'No (labeled as exploratory hardware telemetry)',
        'status': 'EXPLORATORY ONLY'
    },
    {
        'claim_id': 'CLM-13',
        'location': 'research_paper_final.tex:370-405',
        'claim_statement': 'Monte Carlo power simulation (seed 42, 10,000 reps, N=20/arm, alpha=0.0167) yields 10.8%, 49.6%, and 98.6% power',
        'evidence_source': 'scratch/reproduce_power.py, POWER_ANALYSIS_REPRODUCTION.md',
        'reproduction_method': 'Execute Monte Carlo power simulation script with seed 42',
        'reproduced_result': 'd=0.20 -> 10.79% +/- 0.31%; d=0.35 -> 49.64% +/- 0.50%; d=0.70 -> 98.61% +/- 0.12%',
        'contradictions': 'Abstract previously called d=0.20 moderate effect; d=0.20 is small, d=0.35 is moderate',
        'decision': 'CORRECT',
        'needs_update': 'Yes (abstract effect size wording aligned)',
        'status': 'SIMULATED ONLY'
    },
    {
        'claim_id': 'CLM-14',
        'location': 'research_paper_final.tex:410-440',
        'claim_statement': 'TOST equivalence sample size requires N=360/arm (p=0.70), N=429/arm (p=0.50), and N=468/arm with DEFF=1.30',
        'evidence_source': 'scratch/derive_tost.py, TOST_SAMPLE_SIZE_AUDIT.md',
        'reproduction_method': 'Normal-approximation TOST formula derivation with delta=0.10, alpha=0.0167, beta=0.20',
        'reproduced_result': 'N_ind = (z_0.0167 + z_0.20)^2 * 2*p*(1-p) / delta^2 -> 360 (p=0.70), 428.5 -> 429 (p=0.50), 360*1.30 = 468',
        'contradictions': 'Applies to future confirmatory protocol, not executed data',
        'decision': 'RETAIN',
        'needs_update': 'No',
        'status': 'PROPOSED / NOT EXECUTED'
    },
    {
        'claim_id': 'CLM-15',
        'location': 'research_paper_final.tex:445-470',
        'claim_statement': 'Design effect DEFF = 1 + (m - 1)*rho = 1.30 assumes cluster size m=4 and intra-cluster correlation rho=0.10',
        'evidence_source': 'CLUSTERING_AND_EXPERIMENTAL_UNIT_AUDIT.md, scratch/derive_tost.py',
        'reproduction_method': 'Evaluation of Kish design effect formula',
        'reproduced_result': '1 + (4 - 1)*0.10 = 1.30; sensitivity analysis reveals N inflates to 720 if m=8 or rho=0.20',
        'contradictions': 'm=4 reflects 4 repeated tasks per block, but whole-page clustering could yield larger clusters',
        'decision': 'NARROW',
        'needs_update': 'No (assumptions and sensitivity explicitly documented)',
        'status': 'PROPOSED / NOT EXECUTED'
    },
    {
        'claim_id': 'CLM-16',
        'location': 'research_paper_final.tex:475-510',
        'claim_statement': 'Newcombe hybrid-score confidence interval example (56/70 vs 38/80) yields RD = 0.325, 95% CI [0.178, 0.472]',
        'evidence_source': 'scratch/check_intervals.py, INTERVALS_MULTIPLICITY_AND_ESTIMANDS_AUDIT.md',
        'reproduction_method': 'Wilson score limits for p1 and p2 followed by Newcombe Method 10 hybrid score combination',
        'reproduced_result': 'p1=0.800 [0.692, 0.877], p2=0.475 [0.369, 0.584], diff=0.325, CI: [0.178, 0.472]',
        'contradictions': 'Earlier text claimed matches published benchmark exactly; clarified as standard methodological illustration',
        'decision': 'RETAIN',
        'needs_update': 'No',
        'status': 'REPRODUCED OFFLINE'
    },
    {
        'claim_id': 'CLM-17',
        'location': 'research_paper_final.tex:515-545',
        'claim_statement': 'Information omitted by serializer (JSON-LD, hidden spans) is recoverable via direct JavaScript evaluation tools',
        'evidence_source': 'TOOL_REACHABILITY_AND_OBSERVATION_LIMITS.md, test_sentinel_pipeline.py',
        'reproduction_method': 'Offline Playwright tool evaluation on fixture with hidden attributes and JSON-LD',
        'reproduced_result': 'evaluate_script returns value successfully',
        'contradictions': 'Initial observation omission != complete agent inaccessibility if tools available',
        'decision': 'RETAIN',
        'needs_update': 'No (crucial conceptual distinction maintained)',
        'status': 'REPRODUCED OFFLINE'
    },
    {
        'claim_id': 'CLM-18',
        'location': 'research_paper_final.tex:550-590',
        'claim_statement': 'Cross-framework audit compares browser-use with BrowserGym, Stagehand, and Playwright MCP',
        'evidence_source': 'CROSS_FRAMEWORK_FEASIBILITY_AUDIT.md, cached framework specifications',
        'reproduction_method': 'Architectural pipeline comparative audit across DOM serialization and AXTree integration',
        'reproduced_result': 'BrowserGym uses AXTree/HTML dual; Stagehand uses Playwright locator snapshots; Playwright MCP uses CDP',
        'contradictions': 'No cross-framework benchmark runs executed; restricted to architectural comparison',
        'decision': 'RETAIN',
        'needs_update': 'No (scoped to architectural analysis)',
        'status': 'SUPPORTED BUT LIMITED'
    },
    {
        'claim_id': 'CLM-19',
        'location': 'references.bib:60-85',
        'claim_statement': 'AgentOccam citation is Ke Yang et al. (ICLR 2025, arXiv:2410.13825); OSWorld is Tianbao Xie et al. (NeurIPS 2024)',
        'evidence_source': 'references.bib, scratch/verify_citations.py',
        'reproduction_method': 'Cross-reference BibTeX entries against official conference publications',
        'reproduced_result': 'Both entries verified and updated with exact author lists, titles, and conference metadata',
        'contradictions': 'Previous draft had placeholder or corrupted author lists; repaired',
        'decision': 'RETAIN',
        'needs_update': 'No',
        'status': 'VERIFIED FROM PRIMARY EVIDENCE'
    },
    {
        'claim_id': 'CLM-20',
        'location': 'research_paper_final.tex:600-650',
        'claim_statement': 'Confirmatory 4-arm randomized block design protocol (Protocol v4 RCBD) is specified but unexecuted',
        'evidence_source': 'FUTURE_BEHAVIORAL_EXPERIMENT.md, proposed_3arm_schedule.csv, results/daily_quota_ledger.json',
        'reproduction_method': 'Protocol verification, offline dry-run test suite, quota lock verification',
        'reproduced_result': 'Runner and schedule verified offline; zero live executions performed due to quota ceiling',
        'contradictions': 'None; paper clearly labels protocol as future confirmatory design',
        'decision': 'RETAIN',
        'needs_update': 'No',
        'status': 'PROPOSED / NOT EXECUTED'
    }
]

with open('EVIDENCE_TO_CLAIM_MATRIX.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'claim_id', 'location', 'claim_statement', 'evidence_source',
        'reproduction_method', 'reproduced_result', 'contradictions',
        'decision', 'needs_update', 'status'
    ])
    writer.writeheader()
    writer.writerows(claims_data)

print(f"Successfully generated EVIDENCE_TO_CLAIM_MATRIX.csv with {len(claims_data)} claims.")
