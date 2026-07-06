# Authoring Scopes

**Tools as bounded co-authors of the What.** A Product-Framework-tier contract:
each tool that authors into the specification (Figma, an Event Modeling board, a
legacy schema, a Jira board) declares which What-element kinds it may author; the
tool's adapter enforces that boundary; a completeness join across all connected
tools reports what is covered, coverable, or missing an author.

The principle: **specification has provenance** — things to be specified may exist
completely or partially in existing systems, and a scope declaration is how such a
system enters a given process in the funnel.

- The pattern and contract: [`docs/authoring-scopes.md`](docs/authoring-scopes.md)
- The schema: [`schema/authoring-scope.schema.json`](schema/authoring-scope.schema.json)
- The oracles (enforcement + completeness join): [`oracles/scope_check.py`](oracles/scope_check.py) — `--self-test`
- The reference instance: [`reference/figma.authoring-scope.json`](reference/figma.authoring-scope.json)

> Landed in the Product Framework as the **§14 Authoring Scope Conformance Profile**
> (Preview), framework **v1.9.0**.
