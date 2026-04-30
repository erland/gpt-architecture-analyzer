# Setup Steps for the Architecture Analyzer GPT

1. Create a new custom GPT named **Architecture Analyzer**.
2. Paste `gpt-instructions.txt` into the GPT Instructions field.
3. Upload every file in the `knowledge/` directory as GPT Knowledge.
4. Enable file uploads / data analysis if available.
5. Add the conversation starters from `gpt-configuration.md`.
6. Test with a small zipped repository first.
7. Ask it to produce one compact system overview, one functional overview, one information overview, and one hotspot quadrant.

## Recommended first test prompt

```text
Analyze this zipped repository. Produce:
1. repository inventory
2. grouped system overview with Mermaid and ASCII fallback
3. functional overview
4. information overview
5. deployment/runtime overview if detectable
6. complexity/coupling quadrant
7. top architecture risks and next recommended analysis slices

Keep diagrams grouped and avoid clutter.
```
