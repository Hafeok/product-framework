# AI Development Foundations & Contracts — Conformance Statement

> This statement asserts that **The Product Framework** conforms to (1) the
> [AI Development Foundations](https://github.com/Hafeok/ai-development-foundations)
> **Pillar One — Specification Framework**, and (2) the
> [AI Development Contracts](https://github.com/Hafeok/ai-development-contracts)
> **WorkUnit / VerdictEvent** seam contracts as a **producer**. Conformance is
> self-declared: every foundation claim cites the section of
> [`docs/product-framework.md`](docs/product-framework.md) that satisfies it, and
> anyone may verify it against the published
> [specification checklist](https://github.com/Hafeok/ai-development-foundations/blob/main/conformance/specification-conformance.md);
> the contracts claims cite the fields our emitted messages carry and are checked
> against the [producer checklist](https://github.com/Hafeok/ai-development-contracts/blob/main/conformance/producer-conformance.md).

## Framework

| Field | Value |
|-------|-------|
| **Name** | The Product Framework |
| **Version** | 1.7.0 |
| **Repository** | https://github.com/Hafeok/product-framework |
| **License** | Apache-2.0 (shapes, schemas, code) · CC BY 4.0 (specification text) |
| **Maintainer** | Emil ([@Hafeok](https://github.com/Hafeok)) |
| **Conforms to** | Specification Framework ☑ / Execution Contract ☐ / Contracts — Producer ☑ / Contracts — Consumer ☐ |
| **Foundation version targeted** | `ai-development-foundations` @ `13b0cb4` (2026-06-26) |
| **Contracts version targeted** | `ai-development-contracts` @ `0.1.0` (foundation_ref: `main`) |
| **Autonomy level** | n/a (specification framework; does not execute) |

## Statement

> We assert that any artifact produced under **The Product Framework**, following
> its defined process, satisfies every requirement checked below. Each checked
> item cites where in the framework the requirement is met. Requirements that are
> only partially met, or deliberately out of scope, are declared honestly in
> [Known gaps](#known-gaps) rather than overclaimed.

The Product Framework is a catalog-agnostic standard for describing software as
three connected, machine-readable models — **What**, **How**, and **Delivery** —
in one typed graph. It is, by construction, a Pillar One framework: it defines the
shape of a specification, the derivation contract that keeps it traceable, and the
seam at which a frozen work unit is handed to an executor. It stops at that seam
and specifies nothing on the far side of it (§5.1), so it makes **no** Pillar Two
claim.

## Pillar One — Specification

**Coverage:** What layer ☑ · How layer ☑ · SPMC ☑ (all four axes now pinned —
the Model axis was closed by adopting the contracts-tier WorkUnit; see §5 below
and [Contracts Layer — Producer Conformance](#contracts-layer--producer-conformance)).

### Summary

| Requirement | Met? | Where in the framework |
|-------------|------|------------------------|
| Premise (LLM input artifact, 5 properties) | ☑ | §1, §2, §9, §5, §6 |
| Layer separation (What / How / SPMC) | ☑ | §2, §8 (mapping table) |
| What completeness (9 sections) | ◐ | §3, §10 — 7 of 9 fully; 2 partial |
| How completeness (8 sections) | ◐ | §4, §9 — 7 of 8 fully; 1 partial |
| Derivation contract (5 rules) | ☑ | §9 (typed links), §4.1, §10 |
| SPMC (4 axes, frozen context) | ☑ | §5, §5.1, §6.2 — all four axes pinned; Model closed as a full binding via the contracts-tier WorkUnit |
| Scale discipline | ☑ | §10 (rules 1, 13–15), §8.1 |
| The seam (Section 7) | ☑ | §5.1 — defined, frozen, independently versioned, gated before emit |

### Section 0 — Premise (spec is an LLM input artifact)

| Property | Met? | Where |
|---|---|---|
| Unambiguous — every term defined, nothing left to inference | ☑ | One typed graph with defined node/link kinds (§9); "intent" (unmodelled residue) is explicitly marked as specification debt to be promoted, not left to the model (§3.2.1, rule 4) |
| Complete at the boundary | ☑ | Work unit carries a **frozen, fully-resolved input bundle**; freeze precedes emit; a unit needing a mid-execution callback must not be emitted (§5, §5.1) |
| Internally consistent — contradictions resolved in the spec | ☑ | The derivation contract and verification kinds (state/Decider justification, coherence bar) surface contradictions as findings (§6.2, §6.3, §9) |
| Machine-readable — structured, not prose | ☑ | A product is one machine-readable graph; reference encoding RDF + SHACL, any typed-node/typed-link/validatable-shape encoding conformant (§9, §10 rule 1) |
| Explicitly bounded — out-of-scope declared | ◐ | Framework-level open/closed line is explicit (§1); bounded contexts carry explicit cross-context mappings (§3.1). A required *per-What* non-empty out-of-scope list is not enforced — see Known gaps |

### Section 1 — Layer separation

| Requirement | Met? | Where |
|---|---|---|
| What / How / SPMC kept distinct, not collapsed | ☑ | §2 "the three models and the split"; §8 mapping table |
| What ownable/validatable by a non-technical product role | ☑ | What (systems, domain model, event model) owned by product and design; authored and agreed before the How (§2.1, §3, §10 rule 2) |
| How authored by the team and **derived** from the What, not restating it | ☑ | §4; "references, never re-derives" (§5); `derived_from` link (§9) |
| Each unit of work decomposes into an SPMC bundle before a model consumes it | ☑ | Work unit = one bounded transformation with frozen input (§5); §8 maps it to SPMC |

### Section 2 — What completeness

| Required element | Met? | Where |
|---|---|---|
| Identity — single unique name | ☑ | Each **system** is a first-class node with a name, used consistently downstream (§3.2.5, §10 rule 2) |
| Purpose — problem / who / why | ☑ | §1; each system carries a purpose (§3.2.5) |
| Actors — every person/role/system, what each may and may not do | ☑ | Triggers typed by source (user / external / automated) (§3.2.0); what an actor *may not* do is the Decider's reachable rejections (§3.3, Decider justification §6.3) |
| Behaviors — initiator, precondition, postcondition, **and unhappy path** | ☑ | Event model patterns (§3.2.0); the Decider derives commands/events/evolution and **must reject** ≥1 invariant — the unhappy path (§3.3) |
| Boundaries — in/out scope; out-of-scope **non-empty** | ◐ | In-scope is derived (feature footprints, allowlist); framework-level scope explicit (§1). A mandatory non-empty out-of-scope list per What is not enforced — see Known gaps |
| Data — every entity CRUD, with owner and lifecycle | ☑ | Domain model structure + data (§3.1); events `change` entities (§3.2, §9); reference vs production data distinguished (§10 rule 3) |
| Constraints — every non-derivable rule, with source and a way to verify | ☑ | Invariants in a constraint language (§3.1); constraints map to NFRs and are checked (§6, §9) |
| Acceptance Criteria — ≥1 testable criterion per behavior | ☑ | Versioned criteria per artifact kind; "done" is a predicate over behavioural conformance and acceptance criteria (§6.2, §7.2) |
| Open Questions — every known unknown, with owner and what it blocks | ◐ | Under-specification is a **measured signal** (intent-reliance rate, §3.2.1; data-divergence rate, §3.1) and undeclared decisions are surfaced (derivation Rule 5). A dedicated owner-tagged Open-Questions artifact is not a required construct — see Known gaps |

### Section 3 — How completeness

| Required element | Met? | Where |
|---|---|---|
| What Reference — identity and version derived from | ☑ | Work units reference the What/How by pointer; `derived_from` carries the upstream identity (§5, §9); Level 2 (§8.1) |
| Components — single-responsibility, dependencies directed and acyclic | ☑ | Contracts fix layering and isolation; decision logic kept in a pure isolable core (§4.2); structure enforced by the repository layout model (§4.3) |
| Data Model — a technical rep for every What entity, no orphans | ☑ | Derivation Rule "every data model entry maps to a What data entity"; domain conformance forbids structural drift (§6.3, §9) |
| Integrations — external system, direction, protocol, contract, **and failure** | ☑ | Interface contracts use industry standards generated from the domain model (§4.4); cross-system Translation pattern (§3.2.0); failure handled by error categories and `failed` read-model state (§3.2, §6.3) |
| Decisions — question, decision, rationale, rejected alternatives, driving What | ◐ | Decisions carry what/why/when-it-applies/when-it-does-not, by pointer (§4.1); driving What via `derived_from` (§9). "Rejected alternatives" is implied by "when it does not apply", not a mandated field — see Known gaps |
| Error Handling — a declared behavior per error category | ☑ | Decider rejections (§3.3); `failed` projection state (§3.2); error/seam verification kinds (§6.3) |
| Non-Functional Requirements — measurable threshold per What constraint | ☑ | Derivation Rule "every NFR maps to a What constraint"; verifications are deterministic gates (§6, §9) |
| Open Questions — propagated and structured as in the What | ◐ | Same mechanism and same gap as the What layer — see Known gaps |

### Section 4 — The derivation contract (5 rules)

| Rule | Met? | Where |
|---|---|---|
| Every component traces to ≥1 What behavior or data entity | ☑ | `derived_from` typed links (§9); rationale trace per work unit (§5) |
| Every data model entry maps to a What data entity | ☑ | §9; domain conformance verification (§6.3) |
| Every NFR maps to a What constraint | ☑ | §9; NFRs derive from constraints (§4, §6) |
| Every decision traces to a What element that required it | ☑ | Decisions linked to their driving What element (§4.1, §9) |
| Every How element with no What anchor is flagged as an undeclared product decision and escalated | ☑ | Surfaced, not silently blocked: the `escalate` verdict (§6.2) and the **earn-their-place rule** (§4.1) flag elements with no anchor; the intent-reliance rate measures the residue (§3.2.1) |

### Section 5 — SPMC

The work unit (§5) is the framework's SPMC bundle (§8 mapping), emitted as the
contracts-tier WorkUnit (§5.1). Coverage is now **full**: adopting that contract
closed the Model axis, which earlier cuts had left across the seam. Model and
Context are unit-level carriers; Schema and Prompt attach per cell.

| Axis / property | Met? | Where |
|---|---|---|
| **Schema** — output shape; non-conforming output rejected | ☑ | Each cell carries its output shape and versioned acceptance criteria; a failed verdict rejects it (§5, §6.2); the acceptance schema is dual-read like the layout model (§4.3) |
| Schema pins the shape language, recorded alongside | ☑ | Each cell's `schema` pins its **shape-language** with the shape document inline (§5, §5.1); encoding fixes the shape language in the graph (§9) |
| **Prompt** — derived from What behaviors/criteria, filtered through How responsibility | ☑ | The WorkUnit's `cell-graph` names **Prompt** as a per-cell axis, carried inline; each cell's prompt derives from What concepts and How principles referenced in the context-pool and re-derives nothing (§5, §5.1) |
| **Model** — selected by complexity remaining after the How | ☑ | The unit's `tier` is the single worker-role it runs at (homogeneity checked before emit); the producer selects it from the complexity the How leaves (§5, §5.1) |
| Model pinned as a binding (precision/quantization/params) | ☑ | `spmc-bundle.model.binding` pins provider, model-id, quantization, and invocation parameters — a full binding, not a label (§5, §5.1) |
| **Context** — assembled from the How, **frozen and bounded** at execution; no mid-execution retrieval | ☑ | A frozen, fully-inlined content-addressed `context-pool` travelling by value with a content-hash identity; nothing fetched mid-run; freeze precedes emit (§5, §5.1, §6.2) |
| Each axis pinned to the precision at which it affects output | ☑ | The frozen bundle's **content hash is its identity** over a declared canonical form, so any change to schema/prompt/context is a distinct unit; the Model binding pins served precision + invocation (§5.1) |
| Axes independently attributable (a quality failure points to which axis) | ☑ | Per-cell `cell-results` localize a failure to a cell (its S and P) and the unit-level M/C; per-criterion findings and the rationale trace retract exactly the failed claims (§5, §6.2) |

### Section 6 — Scale discipline

| Requirement | Met? | Where |
|---|---|---|
| Same floor for a one-page feature as for a large project (same structure, smaller content) | ☑ | The framework defines shapes and rules only and applies them uniformly; authoring follows the order the derivation contract forces regardless of size (§10 rules 1 & 14–15) |
| A spec missing a required section or holding placeholder content is a draft and does not proceed | ☑ | Conformance is cumulative and claimed at the highest level **satisfied**; an incomplete What does not reach the How (§8.1, §10 rule 13); verification is by construction, not assertion (§6.1) |

### Section 7 — The seam (framework hands work to an execution pillar)

The Product Framework emits frozen work units to an executor, so the seam section applies — and is a first-class part of the design (§5.1).

| Requirement | Met? | Where |
|---|---|---|
| The framework **defines** the handoff artifact's shape (contents, identity, return event) | ☑ | The Build seam fixes two schemas: an emitted work unit (by value, content-hash identity) and a self-describing verdict event (§5.1) |
| The unit is **frozen and self-contained** at emit; no callback to resolve | ☑ | "The freeze is the decoupling"; a unit needing a mid-execution callback is not frozen and must not be emitted (§5.1) |
| The interface **versions independently** of the framework (executor swap needs no framework change) | ☑ | A data contract with no live surface; either side can be rebuilt against the contract alone; by-value→by-reference is additive, not breaking (§5.1) |
| Any spec-side conformance gate the seam depends on runs **before emit** | ☑ | Layout conformance runs first and behavioural simulation runs before realisation; the freeze (and its gates) precede the emit (§6.3, §5.1) |

## Pillar Two — Execution

**Not claimed.** The Product Framework is a specification pillar with a published
socket (§5.1): it defines the Build seam and the verdict-event vocabulary, but it
deliberately specifies nothing about how a unit is scheduled, admitted, batched,
or run — that is the executor's concern, out of scope by the open/closed line
(§1, §5.1). It declares none of the eight Execution building blocks (workers,
capabilities, environment, tools, credentials, transition contract) and asserts no
closure contract. An execution framework conforming to Pillar Two can plug in
behind this seam without either side changing.

## Contracts Layer — Producer Conformance

> Asserts that every WorkUnit produced under this framework satisfies the
> [WorkUnit contract](https://github.com/Hafeok/ai-development-contracts/blob/main/contracts/work-unit.md)
> and that the framework reconciles
> [VerdictEvents](https://github.com/Hafeok/ai-development-contracts/blob/main/contracts/verdict-event.md)
> correctly — the **producer** (emitting/authoring) side of the seam. Checked
> against the [producer checklist](https://github.com/Hafeok/ai-development-contracts/blob/main/conformance/producer-conformance.md)
> @ contracts `0.1.0`. The framework defines the shape every conforming instance
> emits; the reference JSON projection lives at
> [`preview/build-seam/`](preview/build-seam/) (governed by the contract's
> normative [`schemas/`](https://github.com/Hafeok/ai-development-contracts/tree/main/schemas)).

### Emitting WorkUnits

| Requirement | Met? | Where |
|---|---|---|
| Every WorkUnit validates against the normative schema for its encoding + the cross-unit-edge structural check | ☑ | §5.1; local projection [`preview/build-seam/workunit.schema.json`](preview/build-seam/workunit.schema.json); `cell-graph` requires only intra-unit cell ids |
| Carries all schema fields with the declared types | ☑ | §5.1 (the full field set: `unit-ref`, `parent-deliverable`, `bundle-hash`, `tier`, `acceptance-class`, `ladder-position`, `artifact-delivery`, `spmc-bundle`, `cell-graph`) |
| `spmc-bundle` is **fully resolved** — no field requires a callback | ☑ | §5.1 "the freeze is the decoupling"; a unit needing a mid-execution callback is not frozen and must not be emitted |
| Every unit is **executable** — each cell carries prompt + shape inline, `context-refs` resolve, output declared | ☑ | §5, §5.1 (per-cell Schema + Prompt inline, context-pool fragments selected by id, per-cell `output`) |
| `artifact-delivery` declared per unit (`inline`/`workspace`), no undeclared store | ☑ | §5.1 (`artifact-delivery`; undeclared side channels forbidden) |
| Axis precision — Model pinned as a binding, Schema pinned with its shape language | ☑ | §5 (Model = full binding; per-cell Schema pins its shape-language) — the axis closed since the prior cut |
| **Homogeneity check runs before emit**, on the specification side | ☑ | §5.1 (`tier` is unit-wide; a heterogeneous unit is a decomposition defect that fails dispatch before emit) |
| `bundle-hash` is the content hash of `spmc-bundle` as emitted | ☑ | §5.1 (hash of the frozen bundle; identity and body agree at emit) |
| `bundle-hash` taken over a **declared canonical form** | ☑ | §5.1 + `context-pool.bundle-form-profile` names the canonical serialization |
| `cell-graph` contains **no cross-unit edges** — the interior is sealed | ☑ | §5.1 ("the interior is sealed"); schema structural check |
| `unit-ref` / `parent-deliverable` are opaque labels, not pointers | ☑ | §5.1 (opaque identity + lineage; the executor never dereferences them into the graph) |
| Emits by value; `bundle-hash` present regardless (by-reference migration additive) | ☑ | §5.1 (by-value-plus-hash discipline) |

### Consuming VerdictEvents (reconciliation)

| Requirement | Met? | Where |
|---|---|---|
| Reconciles by **observing the stream**, not blocking on a call to the executor | ☑ | §5.1 (verdict is an event; the producer holds no knowledge of any consumer; temporal decoupling) |
| Reconciliation matches on `unit-ref` / `bundle-hash`; no shared runtime state | ☑ | §5.1 (self-describing verdict echoes identity + lineage + bundle-hash) |
| On `rejected` / `escalate` with ladder remaining, **re-dispatches** — fresh unit, same `unit-ref`, same `bundle-hash` if unchanged, `ladder-position` advanced | ☑ | §5.1 (`ladder-position`); §6.2 `escalate` verdict; re-dispatch is a fresh emit |
| Honors `acceptance-class` (`auto-commit-if-green` vs `needs-verdict`) | ☑ | §5.1, §7.2 (the consumer, not the executor, decides to commit or surface) |
| Tolerates **temporal decoupling** — a verdict emitted while not listening reconciles on next read | ☑ | §5.1 ("temporal decoupling follows for free") |

### Ownership

| Requirement | Met? | Where |
|---|---|---|
| Treats the WorkUnit shape as **producer-authored** and published at the contracts tier; accepts no executor-specific override of the shape | ☑ | §5.1, §8 seam row (producer-owns per foundation RFC 0001; the shape lives on the contracts tier, this framework authors it and depends on it) |

## Known gaps

Honest partial conformance, with intent for each item.

| Gap | Status / plan |
|-----|---------------|
| **What/How Open Questions** — no dedicated owner-tagged "Open Questions" artifact with an explicit "what it blocks" field. | Functionally covered by measured under-specification signals (intent-reliance rate §3.2.1, data-divergence rate §3.1) and by Rule 5 / the `escalate` verdict surfacing undeclared decisions. Considering promoting an explicit Open-Question node kind in a future cut so each known unknown carries an owner and a blocked-set as graph data. |
| **Out-of-scope list per What** — the framework does not require every What instance to carry a non-empty explicit out-of-scope list (it declares scope at the framework level and derives in-scope footprints). | Under consideration as a What-side completeness rule; today the boundary is expressed structurally (bounded-context mappings, derived feature footprints, allowlist layout) rather than as a prose exclusion list. |
| **Decision "rejected alternatives"** — §4.1 mandates what/why/when-it-applies/when-it-does-not but not a discrete rejected-alternatives field. | "When it does not apply" carries the same information for traceability; a dedicated `rejected_alternatives` attribute is a candidate addition to the decision shape. |

> **Closed since 1.6.1.** The **SPMC Model axis** ("the framework does not
> select, pin, or bind the model") and **SPMC "Prompt" as a named axis** were
> previously declared out of scope. Adopting the contracts-tier WorkUnit
> (v1.7.0) closed both: the unit now pins the Model as a full binding and names
> Prompt as a per-cell axis (§5, §5.1). The framework's open/closed line still
> holds — *scheduling, admission, batching, and how the artifact is produced*
> remain the executor's concern — but *pinning the model binding* is now
> correctly the producer's job, because a verdict is only attributable to an
> immutable input if the model is itself immutable.

---

*Statement last verified: 2026-07-02 against ai-development-foundations `13b0cb4`
and ai-development-contracts `0.1.0`.*
