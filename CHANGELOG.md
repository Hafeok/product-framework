# Changelog

All notable changes to the Product Framework specification are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the specification aims to follow [Semantic Versioning](https://semver.org/)
adapted for a standard: the MAJOR version increments on a change that can
invalidate a previously-conformant instance.

## [1.5.0] — 2026-06-26

A minor release adding the framework's **execution boundary** and a practical
developer workflow. It adds new normative surface (a new seam contract and rule
clause) but does not invalidate a 1.4.0-conformant instance — it gives instances a
boundary they may now target, and a non-normative guide for day-to-day use.

### Added
- **§5.1 The Build seam — the work-unit emission contract.** Promotes the work
  unit from an internal concept to the framework's **third verified seam** (peer to
  application↔runtime §4.2 and screen↔UI-step §4.5): the boundary where
  specification ends and execution begins. The framework fixes the *contract* that
  crosses it — an emitted unit travelling **by value with a content-hash identity**,
  and a **self-describing verdict event** returning (the producer holding no
  knowledge of any consumer; the freeze is the decoupling) — and fixes **nothing**
  on the far side (scheduling, batching, how realisation is produced, event-stream
  transport are the executor's concern, out of scope). This makes the execution
  pillar **pluggable**: any executor honouring the seam can consume the framework's
  output, and either pillar is swappable. Anchored in §8 as the **Two Pillars
  seam** (the boundary between the specification pillar — this framework — and any
  execution pillar); rule §10.8 extended; the GUIDE's Build stage notes that Build
  runs *across* the seam. Catalog-agnostic: states the socket, never a particular
  executor.
- **`GUIDE.md` — a non-normative developer workflow.** Turns the authoring order
  (§2.1) into the everyday loop a developer runs when a feature arrives:
  **Intake → What → How → Build**, each stage with one guiding question, concrete
  steps, and an exit criterion, plus the feedback cycle (intent-reliance,
  state/Decider justification, data-divergence sending work upstream). Adds a
  lightweight **Intake** preamble for the "before the What" step — locating an
  informal request on the graph and extracting a one-sentence intent. Adds no
  conformance rules (practice stays out of the spec, §7.3); §2.1 gains a
  non-normative pointer to it, and the README lists it.

## [1.4.0] — 2026-06-24

A minor release: it **adds new normative surface** (it does not invalidate a
1.3.0-conformant instance, but a previously-passing instance may now surface new
findings — an unread aggregate field, a never-rejecting Decider — so it is a minor,
not a patch). Completes the What with the pieces authored after the 1.3.0 freeze:
a first-class **system** node, the **GUI/TUI interaction class** as the gating
context dimension, a normative **authoring order**, the **Decider** business gloss,
and the **aggregate-fields / state-justification / Decider-justification** trio that
makes the model self-auditing on the behavioural axis. Also corrects the spec
header (which lagged at 1.2 through the 1.3.0 freeze) and brings the README forward
to the full §§1–13 scope.

### Added
- **§3.2.0 Event-model building blocks and patterns** (adopting the Event Modeling
  vocabulary). Names the four **building blocks** — **Trigger** (new: the thing
  that issues a command, with source user / external / automated), Command, Event,
  **View** — and the four **patterns** as named, checkable event-graph shapes:
  **Command** (`Trigger→Command→Event(s)`), **View** (`Event(s)→View`),
  **Automation** (`Event(s)→View→automated Trigger→Command→Event(s)`), and
  **Translation** (cross-system). Patterns name the *topology*; the Decider (§3.3)
  and Projector (§3.4) supply the *executable semantics* inside the Command and
  View blocks (the Command pattern is a Decider invocation; the View pattern is the
  Projector's no-foreign-events discipline). **Automation is the normative way to
  model self-acting behaviour** — an automated Trigger watches a View (a to-do
  list) and issues Commands carrying no business logic. **Translation is the
  normative way sibling systems (§3.2.5) communicate** — read from exactly one
  source system, write side may fan out — making cross-system coupling an explicit
  directional edge, never a shared table. **Slicing** is identified with the
  framework's work unit (§5) and feature-as-flow-slice (§7.1). Adds the
  **pattern-conformance** verification kind (§6.3) and edges `triggers` /
  `triggered_by` / `watches` / `translates_from` (§9); §3.2's primitives bullet and
  rule §10.4 extended; the checkout example frames its commands/views as patterns
  and notes an Automation and a Translation.
- **§3.2.2 interaction class (GUI / TUI) as the gating context-of-use dimension.**
  A new context dimension *senior* to the others: the interaction class
  determines which sub-dimensions apply. **GUI** brings form factor
  (phone/tablet/desktop) and pointer/touch modality into scope; **TUI** brings
  terminal capabilities (grid size, colour depth, glyph set, key support) and
  rules form factor out. The AIO vocabulary is unchanged across classes — a
  `single-select` reifies to a touch control on a phone and an arrow-key list in a
  terminal — so one What realises over substrates as different as a phone screen
  and an SSH session. A system declares its target classes (§3.2.5); the design
  system (§11) reifies the same AIOs to visual or terminal widgets per class.
  Adds the `targets_class` edge (§9); §10.2 and §10.4 extended; the checkout
  example notes a possible `acme-cli` TUI sibling.
- **§4.5 unreifiable AIOs — honest substrate gaps.** A design system may declare a
  (AIO, class) pair **unreifiable** (e.g. an image `display-collection` in a TUI):
  a recorded, deliberate coverage gap with rationale, surfaced by the seam at
  authoring time, never a silent pass — the same honesty as a *manual* WCAG tag or
  the Polanyi floor. Adds the `unreifiable_in` edge (§9); the §11 manifest gains
  `interaction_class` in `contexts_supported` and an `unreifiable` block.
- **§2.1 Authoring order — the funnel as a process.** A normative description of
  the *order* in which artifacts must come into existence, derived from the
  dependency graph (§9) rather than invented as practice: system & domain
  structure → reference data → events & flows → Deciders & Projectors → UI &
  page graph → the How. **Verification is interleaved** (behavioural simulation
  before realisation, layout conformance first, data conformance continuous), not
  a final phase. The forward chain is a **cycle**: the *intent-reliance rate*
  (under-specification) and the *data-divergence rate* (over-confidence,
  post-deployment) send authoring back upstream — feedback re-enters the funnel
  as a fresh forward pass. The framework is normative about this **order** while
  staying silent about **practice** (cadence, ceremonies, who, when), preserving
  the §7.3 model/practice line. Adds rule §10.14 (closing rule renumbered to 15).
- **§3.2.5 The system** — what is being described. Adds a first-class What-side
  **system** node (name, kind — app/website/service/CLI — purpose, and target
  platform contexts) that owns its page graph and flows. A What may describe
  **several systems sharing one domain model** (e.g. a customer app and an admin
  website), each a distinct surface over the shared meaning with its own root,
  flows, and platforms. **Platform (iOS/Android/web) is folded into context of
  use** (§3.2.2) — "both" is two declared contexts the design system must reify
  into — reusing existing machinery. **System identity is What; deployment
  identity (domain name, bundle id, runtime) is How** (§4.2). §3.2.4's
  "application root" generalised to a per-system root. Adds links `system_of` /
  `targets_platform` / `roots_at` (§9); §8 mapping, §8.1 Level 1, and rule
  §10.2 updated; the checkout example gains a system declaration.
- **§3.3 Decider business gloss.** A business-facing gloss clarifying that a
  Decider is where the business rules live (the rules are its rejections) *and*
  says what results when a command is allowed (the emitted events) — capturing
  both "what is permitted" and "what then happens". The name is kept (precise:
  decide + reject + emit; established; fits the agent-noun pattern with Projector);
  no rename.
- **§3.4 the aggregate-fields principle.** An entity carries *exactly its
  invariant-bearing state* (what its Deciders must read at decision time);
  everything else a screen wants is a Projector's output, not a stored field. The
  same value may exist twice — as enforced aggregate state and as a projected
  field — for different reasons. §3.1's entities bullet gains the
  entity-vs-value-object test (identity-over-time vs. attribute-defined).
- **§3.4/§6.3 state justification — the reverse rule, as a checkable property.** A
  field belongs on an aggregate *iff* some Decider reads it; an unread aggregate
  field is a finding — **dead state**, or (more often) an **unmodelled invariant**,
  making orphaned state a **detector of where the behavioural model is incomplete**,
  the structural peer of the intent-reliance and data-divergence signals. The
  mirror holds on the read side (a projected field no consumer uses is a finding),
  making **state minimality a global property**. Adds the **state-justification**
  verification kind (§6.3) and the `reads` edge (§9); rule §10.5 extended.
- **§3.4 Decider justification — the mirror of state justification.** Every
  Decider must *decide*: at least one reachable rejection (enforce ≥1 invariant).
  A Decider that can never reject is a finding — trivial behaviour that should have
  *no* Decider, or a missing invariant. Explicitly **not** "a Decider must have
  fields": a creation Decider reads no prior state yet is valid because it rejects.
  Adds the `rejects` edge (§9); folded into the state-justification kind; rule
  §10.5 extended. State and Decider justification form a **pincer on unmodelled
  invariants** — found from the state side and the behaviour side.
- Checkout example: a system declaration (`acme-shop`), Order extended with
  `paid_total`/`refund_total` as invariant-bearing fields, a worked **"one
  invariant, many enforcement points"** passage (§3a) tracing `ORDER-REFUND-1` to
  a Decider rejection, a simulation, a data-conformance shape, and a UI constraint,
  and a worked state-justification note.

### Changed
- Spec header **Version 1.2 → 1.4.0**, correcting a version string that lagged the
  body (the 1.3.0 freeze shipped the data-side content under a 1.2 header).
- README brought forward to the full **§§1–13** scope: the What description now
  names the system and the data side; the contents table reflects §§11–13 (three
  Preview profiles) rather than §§11–12; a named maintainer added so the
  references in `LICENSE-docs`, `CODE_OF_CONDUCT.md`, and `SECURITY.md` resolve.

## [1.3.0] — 2026-06-21

Makes the domain model's **data side** first-class and introduces **data
conformance** — the framework's continuous, bidirectional, standalone-adoptable
capability — alongside reference data as part of the What. All changes are
additive; instances conformant to 1.2.0 remain conformant.

### Added
- **§3.1 the domain model's data side, and data conformance as a continuous,
  bidirectional capability.** §3.1 (retitled "structure and data") distinguishes
  **structure** (the SHACL-shape side, what developers mean by "domain model")
  from **data** (the RDF-instance side). **Reference data** is constitutive and
  part of the What; **production data** is the **oracle** the structure is
  validated against. Three principles are named: a data-conformance failure reads
  **both ways** (data wrong *or* spec stale — production data is a witness that
  can indict the spec); the shapes are **authored once but asserted continuously**
  in production (a standing monitor, not only a build gate); and the
  **data-divergence rate** is a first-class metric of spec staleness, the
  over-confidence counterpart to the intent-reliance rate. Adds the
  **data-conformance** verification kind (§6.3) and links `reference_data_for` /
  `conforms_to_shape` (§9). §8 mapping, §8.1 (Level 1 + an "adoptable alone"
  note), rule §10.3, and the checkout example updated.
- **§13 Data Conformance Profile** (**PREVIEW**, non-normative): packages data
  conformance as the framework's **minimal standalone adoption** — a system with
  only a domain structure and a production database declares shapes, asserts them
  continuously, triages failures bidirectionally, and surfaces the data-divergence
  trend, using none of the rest of the framework. Positioned as the lowest-
  commitment entry point (declaring a validatable structure is the hard part of
  Level 1, after which the rest is incremental).

## [1.2.0] — 2026-06-18

Adds a complete What→How chain for the user interface — from What-side screen
meaning down to swappable design-system and content providers — together with a
Preview render contract and a working generic renderer. Also closes a read-model
gap (the Projector) caught while dogfooding the reference implementation, and
names the irreducible-computation boundary (the Polanyi floor). All changes are
additive; instances conformant to 1.1.0 remain conformant.

### Added

*The UI axis (What side)*
- **§3.2.1 The UI step** — the What of a screen: a flow primitive carrying a
  buildable core derived from the model (the projection it `surfaces`, the
  commands it `offers`, its `transitions_to`) plus modelled meaning (emphasis,
  projection-state meanings, accessibility obligations, content references).
- **§3.2.2 Abstract Interaction Objects and the context of use** — the AUI layer
  of the Cameleon four-level model. UI interactions are **typed against AIOs** (a
  closed-core, extensible, context-independent vocabulary), converting the
  What/How UI split from a discipline into a **type boundary**: referencing a
  concrete control is a build-failing violation. Input AIOs derive their fields
  from the command payload (closing the form/data gap). Context of use (form
  factor, modality, …) is a declared What-side model.
- **§3.2.3 Accessibility as ingested criteria** — replaces prose "accessibility
  intent" with **WCAG 2.2 success criteria ingested as entities**, each tagged
  *machine* / *assisted* / *manual*; verdicts report a conformance level and its
  basis, never a bare pass. Obligations are inherited from a step's AIOs and
  extended per step.
- **§3.2.4 The page graph** — application navigation as **one page graph** (pages
  are nodes, `navigate` transitions are edges); a flow is a named connected
  subgraph; a declared application root's out-edges are the global destinations.
  "Top-level" is derived, not tagged. Reuses the `navigate` AIO at root scope.
- **§3.4 The Projector** — the executable form of a read model: the `evolve`/fold
  half of the Decider pair, fully symmetric (derived signature, authored logic,
  simulated sound and complete, serves as the projection's oracle). Closes the
  gap where `projects` named events without saying how they fold — the floor the
  whole UI stack stands on.
- **§3.5 Named-algorithm primitives (the Polanyi floor)** — a first-class
  category for irreducible computation, specified by reference + I/O contract +
  oracle, exempt from derivation, checked by **oracle conformance**. States the
  governing principle: a computation is mechanically derivable exactly to the
  degree its variability is declared data over a generic interpreter.

*The UI axis (How side)*
- **§4.5 The screen-composition contract** — screens as design-system
  compositions over the five normative Atomic Design levels, with a closed
  component vocabulary and tokens over literals; **reification rules**
  `reify(AIO, context) → CIO` (where phone→searchable-list / tablet→segmented
  lives), which must cover every (AIO, context) pair.
- **§4.6 Content resolution** — authored words live in a swappable **content
  store**, `resolve(key, locale) → string`, with locale as the context
  dimension. The fourth application of the framework's one UI move
  (widgets→AIOs, styles→tokens, components→CIOs, copy→content references).

*Verification*
- **§6.2 How a verification runs** — the anatomy of a check (frozen declared
  inputs; oracle derived from the model, not authored in the check; per-criterion
  findings; verdict as the conjunction; no override-by-assertion). Former §6.2
  (required kinds) is now **§6.3**, extended with Projector simulation/conformance
  and the **oracle-conformance** kind, and a seam check covering reification,
  state, content, and accessibility coverage.

*Preview profiles and tooling*
- **§11 Design System Conformance Profile** (PREVIEW) — the contract a design
  system meets to plug in as the Concrete UI layer, plus `design-system.manifest.yaml`.
- **§12 Content Store Conformance Profile** (PREVIEW) — the parallel contract for
  the content provider, plus `content-store.manifest.yaml`.
- **`preview/render-contract.schema.md`** (PREVIEW) — the **render contract**: the
  derived, design-system-agnostic projection of a What a renderer consumes
  (complement to the §11 manifest), with embedded simulated Projector output.
- **`preview/renderer.html`** (PREVIEW) — a working generic AIO renderer that
  consumes a render contract at wireframe fidelity, no design system coupled:
  a navigable, populated, localized checkout proving the contract is sufficient.

*New derivation links (§9)*: `surfaces` / `offers` / `transitions_to`,
`typed_as` / `reifies` / `in_context`, `must_satisfy` / `attests`, `has_state`,
`navigates_from_root` / `in_flow`, `projects_for` / `folds`,
`specified_by_reference` / `pinned_by_oracle`, `references_content` / `resolves`
/ `in_locale`, `realizes_step` / `composes` / `binds`.

### Changed
- **§7.1/§7.2**: a **feature** is now a reference to a slice of the event model;
  its domain concepts are *derived* as a `footprint(f)` traversal, not
  enumerated. `feature_done` ranges over the derived footprint; the release
  closed-cut is a transitive-closure check. (Rule §10.11.)
- **§3.2.1 intent reframed as specification debt**, not implementer autonomy —
  permitted but a measured liability, governed by a promotion rule and the
  *intent-reliance rate* metric. The Decider↔UI-step symmetry corrected: the
  authored peer of Decider logic is the *modelled* choices, with intent outside
  the symmetry as residue.
- **§3.2/§3.2.1/§4.5 projections declare a state space**; a UI step's state
  annotations are constrained-and-covering (the UI analogue of command coverage),
  catching the forgotten-state case. `failed` is What-side meaning, How-side
  mechanism.
- Rules §10.4, §10.5, §10.6, §10.9, §10.11; §8 mapping; §8.1 Levels 1–2; the §2
  diagram; and the README symmetry table updated across the above.

## [1.1.0] — 2026-06-16

### Added
- Initial open-source release of the specification.
- Repository scaffold: `README`, dual `LICENSE`/`LICENSE-docs`, `CONTRIBUTING`,
  and this changelog.

### Changed
- §8 Two Pillars mapping aligned to the parent foundation's vocabulary
  (SPMC named in full; verification described as criteria → judge → verdict; the
  derivation-contract row references §9 rather than restating a partial link set).
- License section replaced its placeholder with the committed dual scheme
  (CC BY 4.0 for text, Apache-2.0 for shapes/code).
- `CONTRIBUTING.md` and `CHANGELOG.md` references now resolve to real files.

---

## Planned

Not yet part of any cut; tracked here as the forward roadmap (not a pending release):

- Machine-readable RDF vocabulary for the typed nodes and links.
- SHACL shapes implementing the conformance rules of §10.
- Reference adoptions to graduate the three Preview profiles (§§11–13) to normative:
  a conforming design system (§11) and content store (§12) realising the worked
  example end to end, and a continuous data-conformance deployment (§13).
