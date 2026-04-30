# Example Prompts for Architecture Analyzer

## General repository analysis
Analyze this zipped repository. Produce a grouped architecture overview with Mermaid diagrams and ASCII fallbacks. Keep diagrams uncluttered and include evidence/confidence.

## Multiple repositories
Analyze these zipped repositories as one system. Identify system boundaries, integration points, deployment relationships, and duplicated domain concepts. Produce context, container, functional, information, and deployment views.

## Functional overview
Analyze the user-facing functionality in this source code. Show a grouped functional overview diagram and explain the main workflows. Avoid implementation-level clutter.

## Information overview
Analyze the information managed by this source code. Show key domain concepts, ownership, lifecycle, and relationships. Use Mermaid only if it remains readable; otherwise use tables plus an ASCII overview.

## Deployment overview
Analyze the deployment/runtime model from Docker, Compose, Kubernetes, CI, config, and application entry points. Produce a deployment overview diagram with evidence and uncertainty.

## Quadrant analysis
Analyze major modules/components and create a complexity vs coupling quadrant. Include scoring rationale, evidence, confidence, and recommended action for each hotspot.

## Deep slice
Focus only on the backend application layer. Produce a component view, key responsibilities, dependencies, risks, and recommended refactoring seams.
