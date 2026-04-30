# Clutter Control and Grouping Rules

The purpose of an architecture diagram is to preserve the overview. Do not sacrifice comprehension for completeness.

## Node limits
- Target: 5-9 primary nodes per overview diagram.
- Soft maximum: 12 primary nodes.
- Hard maximum: 15 nodes unless the user explicitly requests detail.
- If more are needed, split into multiple diagrams.

## Edge limits
- Target: one main relationship between major groups.
- Avoid drawing every call, import, table relation, or endpoint.
- Combine similar relationships into one labeled edge.

## Grouping heuristics
Group by deployable unit, bounded context, capability area, application layer, external system boundary, information ownership, or runtime responsibility.

Do not group only by folder structure if the folder structure hides the actual architecture. Use folders as evidence, not as the only truth.

## Progressive disclosure
Use this sequence:
1. One context/container overview.
2. One functional overview.
3. One information overview.
4. One deployment/runtime overview.
5. Detailed component diagrams only for selected areas.

## Split triggers
Split the diagram if it has more than 12 primary nodes, labels become long, edges cross conceptually, code knowledge is required to understand it, or one sub-area dominates.

## Replace diagram detail with tables
Use tables for endpoint lists, file/class lists, module evidence, scoring details, one-to-many mappings, and risk lists.

## Abstraction labels
Create useful names for groups even when source names are technical. Example: `Order workflow` instead of `OrderController + OrderService + OrderRepository`.

## Confidence warning
If grouping is inferred, state that it is inferred and list evidence.
