# Output Templates

## Standard architecture analysis response

```markdown
# Architecture Analysis

## 1. Scope and limits
- Repositories analyzed:
- Analysis limits:

## 2. Repository inventory
| Area | Findings | Evidence | Confidence |
|---|---|---|---|

## 3. Grouped system overview
Short explanation.

Mermaid diagram plus ASCII fallback.

## 4. Functional overview
- Capability groups
- Main workflows

## 5. Information overview
| Concept | Owner | Lifecycle | Evidence |
|---|---|---|---|

## 6. Runtime/deployment overview
Only include if enough evidence exists.

## 7. Quadrant analysis
| Area | X score | Y score | Quadrant | Evidence | Confidence |
|---|---:|---:|---|---|---|

ASCII quadrant.

## 8. Architecture risks and hotspots
| Priority | Area | Why it matters | Recommendation |
|---:|---|---|---|

## 9. What to inspect next
- Suggested next slice 1
- Suggested next slice 2
```

## Compact response for large repositories
If the repository is large, first return inventory, top-level grouped view, analysis plan for deeper slices, and first-pass hotspots. Do not attempt to exhaustively analyze every file in one response.
