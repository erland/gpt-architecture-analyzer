# Architecture Analysis Method

## Goal
Turn uploaded source-code repositories into understandable architecture views. The result should explain what the system is, how it is structured, how users use it, what information it manages, how it runs, and where architecture risks exist.

## Standard analysis sequence

### 1. Repository inventory
Identify repositories, languages, frameworks, build/package files, runtime entry points, application layers, tests, infrastructure files, deployment descriptors, configuration files, and generated/vendor folders to ignore.

### 2. Architecture model extraction
Extract or infer systems, bounded contexts, frontend/backend/worker/database/queue/file/integration/infrastructure components, major modules, user-facing capabilities, domain concepts, runtime relationships, deployment relationships, and quality/risk signals.

### 3. Grouping before diagramming
Always group before drawing. Do not draw every file, class, endpoint, or table in overview diagrams.

Preferred grouping levels:
1. System / product
2. Container / deployable
3. Major capability or bounded context
4. Module / package cluster
5. Class/file/function detail only when requested

### 4. View generation
Generate the most useful subset of views: system context, container, functional overview, use case/user journey, information overview, runtime/sequence, deployment, integration, complexity/coupling quadrant, and risk/hotspot view.

### 5. Evidence and confidence
Every important claim should be tied to observable evidence, such as file paths, configuration files, package names, endpoint names, migration files, tests, or dependency declarations.

Confidence levels:
- High: directly supported by explicit source/config/test evidence.
- Medium: supported by several indirect signals.
- Low: plausible inference but incomplete evidence.

### 6. Recommendations
Recommendations should be scoped and practical: specific refactoring seams, diagrams to inspect next, tests to add before risky changes, architecture decisions to document, and follow-up analysis slices.
