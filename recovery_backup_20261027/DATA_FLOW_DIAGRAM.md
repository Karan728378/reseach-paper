# BROWSER-USE 0.13.10 OBSERVATION PIPELINE DATA FLOW AND CIRCULARITY
**Generated (UTC):** 2026-10-26T19:34:48.313118+00:00  
**Package:** `browser-use==0.13.10` (SHA-256 verified)

---

## 1. Architectural Data Flow Diagram

```mermaid
flowchart TD
    HTML[Source HTML / Web Page] -->|CDP DOM.getDocument / Runtime.evaluate| DOM[Stage 1 & 2: Live Browser DOM]
    DOM -->|CDP Accessibility.getFullAXTree| AX[Stage 3: Blink Accessibility Tree]
    
    subgraph BrowserUse [browser-use Observation Engine]
        DOM -->|dom/service.py: get_clickable_elements| ENH[EnhancedDOMTreeNode Construction]
        AX -->|ax_node attached to tree nodes| ENH
        
        ENH -->|serializer/serializer.py: L480-482| DIS[Mechanism 1: DISABLED_ELEMENTS Pruning]
        note1[Prunes: script, meta, link, title, head, style unconditionally] -.-> DIS
        
        DIS -->|serializer/clickable_elements.py: L204-225| DET[Interactivity Detection Engine]
        DET -->|Rule A: Native tag / role attribute in interactive set| INT[is_interactive = True]
        DET -->|Rule B: ax_node.role in interactive set| INT
        DET -->|Rule C: 10px <= width, height <= 50px icon heuristic| INT
        DET -->|Rule D: cursor: pointer| INT
        
        INT --> SEL[Selector Map Registration]
        
        ENH -->|serializer.py: L1046-1051| GATE[Mechanism 2: Interactivity Gating]
        DET -.->|Determines node.is_interactive| GATE
        
        GATE -->|If non-interactive: strip tags and attributes, emit text only| TEXT_ONLY[Text-Only Node Stream]
        GATE -->|If interactive: enter attribute filtering| ATTR[Mechanism 3: Attribute Whitelist Filter]
        
        ATTR -->|views.py: DEFAULT_INCLUDE_ATTRIBUTES L18| WHITELIST[Attribute Whitelist Check L1214]
        note2[Retains: aria-label, role, title, id, name, placeholder, data-state<br>Drops: developer data-*, aria-describedby, aria-live] -.-> WHITELIST
        
        WHITELIST --> S4[Stage 4: Serialized DOM Tree llm_representation]
        TEXT_ONLY --> S4
    end
    
    S4 -->|Agent message_manager.create_state_messages| S5[Stage 5: Observation Message Buffer]
    S5 -->|LLM Client ainvoke / HTTP Request| S6[Stage 6: Provider Model Request Boundary]
```

---

## 2. Mathematical Formalization of the Serialization Gap

Let $\mathcal{C}$ represent the set of semantic metadata channels present in the document. For a given channel $c \in \mathcal{C}$, we define retention indicator functions across pipeline stages $s \in \{1, 2, 3, 4, 5\}$:
$$\mathbf{1}_s(c) \in \{0, 1\}$$

The **DOM Serialization Gap** $\mathcal{G}(c)$ is the information loss between the Live DOM ($s=2$) and the Agent Observation Buffer ($s=5$):
$$\mathcal{G}(c) = \mathbf{1}_2(c) - \mathbf{1}_5(c)$$

### Pruning Mechanism Classification:
1. **Mechanism 1 (Element-Level Pruning):**
   $$	ext{Tag}(e) \in 	exttt{DISABLED\_ELEMENTS} \implies e 
otin 	ext{Stage 4}$$
   Applies to: `<script>` (JSON-LD), `<meta>`, `<title>`, `<head>`, `<link>`.
   $\mathcal{G}(	ext{JSON-LD}) = 1 - 0 = 1$ (100% loss).

2. **Mechanism 2 (Interactivity-Gated Structural Dropping):**
   $$
eg 	ext{Interactive}(e) \land 
eg 	ext{Scrollable}(e) \implies 	ext{Attrs}(e) = \emptyset$$
   Applies to: `aria-label` on non-interactive `<span>`/`<div>`, `role="region"`, developer `data-*` on containers.
   $\mathcal{G}(	ext{Container ARIA}) = 1 - 0 = 1$ (100% loss).

3. **Mechanism 3 (Attribute Whitelist Filtering):**
   $$a 
otin 	exttt{DEFAULT\_INCLUDE\_ATTRIBUTES} \implies a 	ext{ omitted}$$
   Applies to: `data-action`, `data-product-id`, `aria-describedby`, `aria-labelledby`, `aria-live`.
   $\mathcal{G}(	ext{Developer } data	ext{-*}) = 1 - 0 = 1$ (100% loss).

---

## 3. Selector Map vs. Blink AXTree Circularity (C4 Audit Finding)

A central finding of this audit is that **the selector map's correspondence with the Blink AXTree is partially circular by construction**.
In `serializer/clickable_elements.py` (L204–225):
```python
if node.ax_node and node.ax_node.role in INTERACTIVE_ROLES:
    node.is_interactive = True
```
