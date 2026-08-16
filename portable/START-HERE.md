# Architecture Analyzer – Portable Chat Package

Detta paket gör samma Architecture Analyzer-underlag tillgängligt i en vanlig ChatGPT-konversation.

## Start

1. Läs `assistant/instructions.txt` först och använd den som arbetsinstruktion under resten av konversationen.
2. Använd filerna i `knowledge/` som permanent referensmaterial för arkitekturanalys.
3. `assistant/conversation-starters.md` innehåller exempel på lämpliga startfrågor, men användarens aktuella instruktion har alltid företräde.
4. När ett eller flera repository-ZIP:ar bifogas: följ arbetsflödet i instruktionen, inventera först och skilj tydligt mellan evidens, inferens och osäkerhet.
5. För stora kodbaser: gruppera aggressivt och undvik diagram som försöker visa allt samtidigt.

## Prioritet

Vid konflikt gäller i praktiken:

1. användarens aktuella instruktion,
2. `assistant/instructions.txt`,
3. relevanta filer i `knowledge/`.

Paketet är byggt från samma instruktion och Knowledge-filer som Custom GPT-distributionen.
