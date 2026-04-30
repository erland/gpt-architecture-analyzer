# Architecture Model Schema

Use this internal schema as a thinking and reporting aid. The model can be emitted as YAML when useful.

```yaml
system:
  name: string
  purpose: string
  confidence: high|medium|low

repositories:
  - name: string
    role: string
    languages: []
    frameworks: []
    evidence: []

actors:
  - id: string
    name: string
    type: person|system|organization
    evidence: []

containers:
  - id: string
    name: string
    type: web_app|api|worker|database|queue|cache|storage|external|library|other
    responsibilities: []
    technologies: []
    evidence: []

components:
  - id: string
    container: string
    name: string
    responsibility: string
    kind: controller|service|repository|domain|ui|state|adapter|config|other
    evidence: []

information_concepts:
  - id: string
    name: string
    owner: string
    lifecycle: string
    evidence: []

relationships:
  - from: string
    to: string
    type: calls|reads_writes|publishes|subscribes|contains|depends_on|configured_by|deploys_to
    label: string
    confidence: high|medium|low
    evidence: []

risks:
  - area: string
    risk: string
    severity: low|medium|high
    evidence: []
    recommendation: string
```

Do not force the user to see this model unless it helps. Use it to keep diagrams consistent.
