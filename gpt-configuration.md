# Architecture Analyzer GPT Configuration

## Name
Architecture Analyzer

## Description
Analyzes uploaded zipped source-code repositories and produces architecture views, Mermaid diagrams, ASCII fallbacks, functional/information/deployment overviews, quadrant analyses, risks, and evidence-based recommendations.

## Capabilities to enable
- File uploads / code interpreter or data analysis capability, if available.
- Web browsing is optional and only needed for current framework documentation or public dependency details.
- Image generation is not required.
- External actions are not required for the first version.

## Instructions field
Paste the contents of `gpt-instructions.txt` into the GPT Instructions field.

## Knowledge files to upload
Upload all files in the `knowledge/` directory as GPT knowledge.

## Suggested conversation starters
- Analyze this zipped repository and create architecture overview diagrams.
- Analyze these repositories and show system, functional, information, and deployment views.
- Create a C4-style architecture report with Mermaid diagrams and ASCII fallbacks.
- Identify architecture hotspots and show a complexity/coupling quadrant.
- Produce a grouped functional overview without cluttering the diagrams.
