# Architecture Analyzer – OpenAI Plugin (GPT Builder 1.5.1)

OpenAI Plugin is added as a skills-first peer runtime.

- repository/file access is a required host capability for the primary source-analysis task
- if repository access is unavailable, repository analysis must block rather than simulate inspection
- only target files actually read may be used as source evidence
- plugin references, manifests and runtime files are never target-source evidence
- shell and code execution are optional host capabilities
- persistent cross-session state is not required
- no runtime scripts or custom tools are packaged
- no MCP wrapper is generated
- plugin ZIP participates in delivery manifest, checksums, runtime parity, release readiness, workflow parity and reproducibility
