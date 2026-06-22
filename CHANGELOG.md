# Changelog

All notable changes to the Product Framework specification are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the specification aims to follow [Semantic Versioning](https://semver.org/)
adapted for a standard: the MAJOR version increments on a change that can
invalidate a previously-conformant instance.

## [1.3.0] — 2026-06-22

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

### Planned
- Machine-readable RDF vocabulary for the typed nodes and links.
- SHACL shapes implementing the conformance rules of §10.
- Coupling experiment: a conforming design system (§11) and content store (§12)
  realising the worked example end to end, to graduate both Preview profiles.

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
