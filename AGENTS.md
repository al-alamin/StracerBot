# AGENTS.md

Read the shared rules first: agents/AGENTS.md of https://github.com/DE-Knowledge-Base/agents.md (on Alamin's MacBooks at ~/agents.md), plus the applicable harness supplement. This file adds this repository's guidance.

## Purpose, current state and planned work

A course research project for searching Stack Overflow stack traces, with data-processing scripts and a demonstration web application.

Maintenance and runtime/deployment status are not established by this top-level audit, so `repo.yaml` uses `state: unknown`. Capabilities below describe documentation and tracked material, not newly tested application behavior.

Current documented capabilities:

- readme.md documents XML-to-CSV processing, code-segment extraction, TF-IDF preparation and metadata extraction; Scripts and batch_jobs directories are tracked.
- The root tree includes a web_application/ demonstration and research report/presentation material; runtime and research results were not evaluated.

Documented planned work (completion not established by this audit):

- The historical README task list describes ongoing search research, summarization and possible distributed-processing extensions; present completion is unverified.

## Working here

- Read readme.md and relevant component instructions before changing research scripts or the demonstration.
- Preserve source-data provenance and licensing; do not treat historical task status or performance estimates as verified current results.
- Cluster jobs and large dataset operations require their own approved scope; a metadata update does not launch them.
