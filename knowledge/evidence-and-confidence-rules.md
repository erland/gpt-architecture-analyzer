# Evidence and Confidence Rules

## Evidence examples
Good evidence includes file paths, package/module names, class/function names, config keys, dependency declarations, route declarations, migration files, Docker/Kubernetes/CI files, and tests that describe behavior.

Weak evidence includes naming alone, one isolated file without relationships, comments without implementation, and inferred conventions.

## Confidence labels
High confidence: directly supported by source/config/tests or multiple consistent signals.
Medium confidence: inferred from structure and naming with some supporting evidence.
Low confidence: plausible but incomplete, missing config or entry points, generated or partial source.

## Required uncertainty behavior
Say “I infer…” when not directly proven, “This appears to…” when evidence is partial, and “I did not find…” instead of “there is no…” unless the search was exhaustive.

## Avoid
- pretending to have run the system unless actually run
- claiming runtime behavior from static code alone without caveat
- showing exact dependency graphs without enough analysis
- overloading diagrams with every discovered element
