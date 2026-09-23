# Architecture Analyzer

Repository för **Architecture Analyzer** med jämbördiga distributioner för ChatGPT Chat, Custom GPT, Claude Projects och OpenCode, byggda från samma canonical instruktion och Knowledge-lager.

## Aktuell Custom GPT-konfiguration

- Instructions: `gpt-instructions.txt`
- Conversation starters och installationsbeskrivning: `gpt-configuration.md`
- Maskinläsbar konfiguration: `gpt-config.json`
- Knowledge: samtliga 10 filer i `knowledge/`
- Setup: `docs/setup-steps.md`

De beteendestyrande källfilerna används oförändrade i Custom GPT-distributionen.

## Bygg distributioner lokalt

```bash
python3 scripts/build_distributions.py
python3 scripts/validate_distributions.py
```

Det skapar:

```text
dist/
  architecture-analyzer-project-vX.Y.Z.zip
  architecture-analyzer-chat-vX.Y.Z.zip
  architecture-analyzer-custom-gpt-vX.Y.Z.zip
  architecture-analyzer-claude-vX.Y.Z.zip
  architecture-analyzer-opencode-vX.Y.Z.zip
  SHA256SUMS.txt
  DELIVERY-MANIFEST.json
```

Vanliga byggen använder versionen i `VERSION`.

## Portable Chat

Bifoga `architecture-analyzer-chat-vX.Y.Z.zip` i en vanlig ChatGPT-konversation och skriv exempelvis:

> Använd Architecture Analyzer i den bifogade ZIP-filen under den här konversationen. Läs START-HERE.md först.

Bifoga därefter repository-ZIP:en eller repository-ZIP:arna som ska analyseras.

## GitHub Release

Vid en publicerad GitHub Release används release-taggen som versionskälla. Taggen ska följa SemVer med inledande `v`, exempelvis:

```text
v1.0.0
v1.1.0
```

En release `v1.1.0` bygger och bifogar automatiskt:

```text
architecture-analyzer-project-v1.1.0.zip
architecture-analyzer-chat-v1.1.0.zip
architecture-analyzer-custom-gpt-v1.1.0.zip
architecture-analyzer-claude-v1.1.0.zip
architecture-analyzer-opencode-v1.1.0.zip
SHA256SUMS.txt
DELIVERY-MANIFEST.json
```

Taggversionen skrivs även in i `VERSION` inne i respektive distributionspaket och i portable-paketets `MANIFEST.json`.
