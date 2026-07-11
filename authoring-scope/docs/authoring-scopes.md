# Authoring Scopes — tools as bounded co-authors of the What

*A Product-Framework-tier contract, landed as the §14 Authoring Scope Conformance Profile (Preview) in framework v1.9.0.*

> **Status: landed (Preview).** The contract, both oracles, and the Figma reference
> scope are specified and working, and this package landed in the Product Framework
> as the **§14 Authoring Scope Conformance Profile** (Preview) in **v1.9.0**. It
> is a contract about the What's write paths, and remains Preview until exercised as
> a live intake path feeding a conformant What end to end.

---

## 1. The principle: specification has provenance

The What does not materialise from nothing — it is *authored*, and its authors are
heterogeneous. A designer in Figma authors the interface slice. A domain expert's
Event Modeling board authors the event slice. A legacy system's schema already *is*
the de facto data contract. An existing Jira board partially authors the journey.

**Things to be specified may exist, completely or partially, in existing systems.**
The authoring-scope contract is how such a system enters a given process in the
funnel: as a **bounded co-author** of the What. Its contribution is first-class —
authored meaning, not "context to consult" — but only within a **declared,
enforced slice**, and a **completeness join** across all connected authors tells
you exactly what remains unauthored and who could author it.

This generalises a pattern that already runs through Decision-Driven Design:

- It is **axis-pinning applied to authorship**. As a work unit pins which SPMC axes
  it may vary, an authoring tool pins which What-slices it may write.
- It is the **discovery-record principle at the intake boundary**. Exploratory
  knowledge enters engineered mode only through a sanctioned channel; authored
  meaning enters the What only through a tool's sanctioned scope. A tool authoring
  outside its declared slice is disqualifying **regardless of content quality** —
  exactly as What/How fusion disqualifies a discovery record however complete it is.
- It re-characterises the **Polanyi floor** declaratively. A tool's `excluded` list
  is its Polanyi boundary written down: the What-elements this surface structurally
  cannot carry. And it is, precisely, a **channel floor**, not an intrinsic one —
  the knowledge is encodable, *this surface* just cannot carry it — which is
  exactly why the §4 gap split can route it to a sanctioned author instead of
  declaring it unencodable. The empirical annotation-needed list then splits along
  that boundary (§4).

## 2. The contract

Each tool that authors into the What carries an **authoring-scope declaration**
([`schema/authoring-scope.schema.json`](../schema/authoring-scope.schema.json)):

- **`authors`** — the What-element kinds this tool MAY author, each with a
  **completeness** (`sufficient` — the tool can author this kind fully; `partial` —
  it contributes, other authors expected) and a **channel** (how the meaning is
  carried in the tool: a native annotation, a component name, frame structure, a
  variable export). The adapter reads only declared channels.
- **`excluded`** — the kinds this tool MUST NOT author. Explicit, not inferred by
  omission: the exclusion list is a commitment, and inbound content authoring an
  excluded kind is rejected regardless of quality.
- **`process-slice`** — optionally, the funnel slice this authorship enters, so
  authored meaning arrives where the process expects it.

The **kind vocabulary is the Product Framework's own ontology** (verified against
the live 1.9.0 spec) — `domain-structure` (entities, relations, invariants, §3.1),
the event-model blocks `trigger` / `command` / `event` / `view` (§3.2.0), `decider`
and `projector` (§3.3–3.4), `ui-step` and `aio` (§3.2.1–3.2.2), `state-annotation`
(the authored per-state meanings and waivers, §3.2.1), `page-graph`,
`context-of-use`, `accessibility-criteria` (§3.2.3), `content-reference` (§3.2.1),
`journey` (§3.0.1), `quality-demand` (§3.6), `data-shape` (§13), … A scope is a
subset over kinds the framework already names; this contract introduces no ontology
of its own. Note one asymmetry the vocabulary carries: some kinds are **derived,
not authored** — a read model's `state-space` derives from the projection's shape
(§3.2) — and a derived kind belongs in *every* tool's excluded list, because no
tool is its author.

**Ownership.** The scope contract lives at the What's level (Product Framework /
product-cli). A tool's **adapter** (e.g. the Figma bridge) *enforces* a scope; it
never *owns* one. This is the same deflation applied to the Loom adapters: strip
the intermediary of independent meaning; let it only project onto — and police the
boundary of — an authoritative core.

## 3. Enforcement (per tool submission)

The adapter runs the enforcement oracle
([`oracles/scope_check.py`](../oracles/scope_check.py)) on everything the tool
submits:

- **In-scope authored content → accepted** into the What (subject to the What's own
  validity checks, which this contract does not replace).
- **Out-of-scope authored content → rejected**, with the basis stating the scope
  violation. A Decider authored in Figma is rejected *because Figma is not a
  sanctioned author of Deciders*, not because the Decider is wrong.

## 4. The gap split

Everything the adapter suspects needs authorship (the former "annotation-needed"
list) splits along the scope boundary into two findings demanding **different
actions from different people**:

| Finding | Meaning | Action |
|---|---|---|
| `unauthored-within-scope` | the tool *could* author this and didn't | author it **in the tool** (annotate the frame in Figma) |
| `outside-scope` | no work in this tool can author this | **route** to a sanctioned author (author the Decider in product-cli) |

This turns the Polanyi floor from a flat failure list into a routed work queue.

## 5. The completeness join (across all connected tools)

A What specification is **complete** when every required element kind is authored
by *some* sanctioned tool within its scope. The join reports, per required kind:

- **`covered`** — authored, and by whom (partial authors compose: Figma's visual
  criteria + product-cli's non-visual criteria jointly cover
  `criteria-attachment`);
- **`coverable-but-unauthored`** — a connected tool's scope includes it, but no one
  authored it yet;
- **`uncovered`** — no connected tool's scope includes it: **a sanctioned author is
  missing**, and connecting one (a Miro adapter for `journey`, say) is what
  completes the What.

This is the §3.5 view-contract discipline applied to authorship itself — nothing
required left unauthored, nothing authored out of sanction — one level up from
views: the bidirectional join over *who may say what*, rather than *what is shown
where*.

## 6. The reference instance: Figma

[`reference/figma.authoring-scope.json`](../reference/figma.authoring-scope.json):

- **Authors** (`sufficient`): `aio` via native annotation, `state-annotation`
  (the per-state meanings a designer is exactly the right author of — what *empty*
  looks like and means), `page-graph` via frame structure, `token-source` via
  variable export.
- **Authors** (`partial`): `ui-step` via frame structure (the buildable core's
  projection/command references come from the model, not the canvas), `aio` via
  component-name (the medium-confidence channel), `context-of-use`,
  `accessibility-criteria` (visual criteria only — contrast, target size;
  non-visual criteria are authored in product-cli), `content-reference`.
- **Excluded**: `domain-structure`, `trigger`, `command`, `event`, `view`,
  `decider`, `projector`, `journey`, `quality-demand`, `data-shape` — the
  What-elements a canvas tool structurally cannot carry — and `state-space`,
  which is excluded for a different reason: it is *derived* from the projection's
  shape (§3.2), so no tool authors it.

The Figma bridge, upgraded to a scope-enforcing adapter, thereby loses its last
piece of independent meaning: its AIO vocabulary comes from the framework ontology,
its composition rules from loom-spec's composition-graph contract (the intra-page
containment contract — distinct from the What's `page-graph`), and *what Figma may say
at all* from this scope declaration. The bridge becomes enforcement of contracts it
does not own — thin all the way through, exactly like a Loom adapter at the other
end of the stack.

## 7. The full symmetry

The ecosystem now has the same shape at both ends:

```
  AUTHORSHIP (top)                          REIFICATION (bottom)
  one What-of-truth                         one behavioural core (Loom)
    ← authored through tools                  → projected through modes
      (Figma, Miro, spreadsheets, …)            (loom-ios, loom-web, …)
    ← carried by thin adapters                → packaged by thin adapters
      whose SCOPE is checked                    whose FIDELITY is checked
    ← completeness = the authoring join      → completeness = the view join
```

Authorship flows in through scopes; reification flows down through seams; and the
gallery at the very bottom is the terminal reification of everything authored
above.

## Planned

- **Landed in the Product Framework (v1.9.0)** — the scope contract landed as the
  **§14 Authoring Scope Conformance Profile** (Preview). Still to do before normative
  status: express the kind vocabulary as references into the framework's own sections
  rather than the parallel list this package still carries, and add the **SHACL twin**
  per the dual-encoding discipline (this package is JSON-Schema-only).
- **Upgrade the Figma bridge** to consume the scope declaration and emit the
  §4 gap split (`unauthored-within-scope` / `outside-scope`) in place of the flat
  annotation-needed list.
- **`required-kinds` profiles** — per process-slice, the set of kinds a complete
  What needs (the join's left-hand side), authored as data rather than hard-coded.
- **Second reference scope** — an Event-Modeling-tool scope (`trigger`, `command`, `event`, `view`,
  `command`) to prove the join composes across genuinely different
  authoring surfaces.
