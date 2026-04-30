# Quadrant Scoring Rubric

Quadrant views help prioritize attention. They are not exact measurements unless source metrics are computed. Treat them as an evidence-based heuristic.

## Common quadrant pairs

### Complexity vs business importance
- High complexity + high importance = critical hotspot
- High complexity + low importance = simplification candidate
- Low complexity + high importance = strategic stable area
- Low complexity + low importance = low-risk support area

### Coupling vs cohesion
- High coupling + low cohesion = refactoring candidate
- High coupling + high cohesion = central integration point
- Low coupling + high cohesion = healthy module
- Low coupling + low cohesion = possible miscellaneous utility area

### Volatility vs test coverage
- High volatility + low tests = change risk
- High volatility + high tests = active but protected
- Low volatility + low tests = latent risk
- Low volatility + high tests = stable protected area

## Suggested scoring scale
Score each dimension 1-5.

Complexity signals: file/module size, branching/nesting, number of responsibilities, public APIs, dependencies, configuration logic.
Coupling signals: incoming/outgoing dependencies, cross-layer references, circular references, shared mutable state, infrastructure dependency leakage.
Volatility signals: duplicated concepts, feature-specific conditionals, many TODO/FIXME comments, change markers if available.
Importance signals: user-facing workflow, central domain model, external API contract, data ownership, deployment/runtime criticality.
Test confidence signals: unit, integration, smoke, contract, and end-to-end tests.

## Output format
Always include score table, quadrant assignment, evidence, confidence, and recommended action.

## ASCII quadrant template

```text
                         Higher Y dimension
                               ^
                               |
        Quadrant A             |          Quadrant B
        - item                 |          - item
                               |
Low X dimension ---------------+--------------- High X dimension
                               |
        Quadrant C             |          Quadrant D
        - item                 |          - item
                               v
                         Lower Y dimension
```
