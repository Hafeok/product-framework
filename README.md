# The Product Framework

**An open standard for specifying software as What, How, and Delivery.**

The Product Framework is a catalog-agnostic standard for describing a software
product as three connected, machine-readable models:

- **What** the system is and does — one or more **systems** (name, kind,
  platform reach), a **domain model** (structure *and* data, with reference data
  as part of the What), and an **event model** (behaviour), owned by product and
  design;
- **How** the code expresses the What — decisions, principles, patterns,
  contracts, and a repository layout model, owned by engineering;
- **Delivery** — features and releases as partitions of the What, with "done"
  expressed as a verifiable predicate.

It defines **shapes and rules, not any particular product.** You build your
domain models, your reusable How (archetypes), your verification libraries, and
your tooling *on top of* the framework — and adopting it never requires
disclosing them.

The full specification is in [`docs/product-framework.md`](docs/product-framework.md).

## Why it exists

Software is usually described in scattered, human-only artifacts — a wiki of
requirements, diagrams that drift from code, tickets that lose their rationale.
The Product Framework makes a product description **reproducible, verifiable,
and traceable**, so the description can drive generation, gate verification, and
explain itself. It rests on one chain: *reproducibility → measurement →
improvement.*

## The symmetry at its core

Two kinds of thing a system does — *decide* and *display* — are specified the
same way, and that symmetry is the framework's spine:

| | Behaviour | UI |
|---|---|---|
| **What-side artifact** | the Decider (§3.3) | the UI step (§3.2.1) |
| **Derived from the model** | the commands it handles, the events it emits | the projection it surfaces, the commands it offers, each typed by an Abstract Interaction Object |
| **Genuinely authored** | the decision *logic* | the modelled choices — AIO typing, emphasis/state/accessibility, reification rules |
| **Not part of the symmetry** | — | *intent* — unmodelled residue, treated as specification debt to be promoted into the modelled choices |
| **Constrains the How** | a pure, isolable core (§4.2) | the screen-composition contract (§4.5) |
| **Checked by** | behavioural conformance | the seam verification (§6.3) |

In both cases a What-side artifact derives its structure from the model, leaves
only meaning to be authored, imposes a constraint on the How, and is verified
rather than trusted. The Decider makes behaviour *executable from the model*;
the UI step makes a screen *buildable from the model*.

## Start small: data conformance

The framework's lowest-commitment entry point needs none of the above. A system
with only a **domain structure** (entities, relations, invariants as validatable
shapes) and a **production database** can declare what its data *should* satisfy
and assert it against real data — continuously, in production. A failure reads
both ways: the data is wrong, **or the spec has gone stale** — production data is
a witness that can indict the model. The resulting *data-divergence rate* is a
standing measure of how far the spec has fallen behind reality. Every system has
data and almost none can say whether it is valid against what they believe should
be true; this is where to start (see [§13](docs/product-framework.md#13-data-conformance-profile)).

## What's in this repository

| Path | Contents |
|---|---|
| [`docs/product-framework.md`](docs/product-framework.md) | The specification (normative §§1–10; Preview §§11–13). |
| [`examples/checkout/`](examples/checkout/) | A worked example — a complete What carried down the whole chain, doubling as the spec's conformance demonstration. |
| [`preview/`](preview/) | The render contract (Preview) and a working generic renderer that previews a What at wireframe fidelity. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to propose changes and file conformance reports. |
| [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | Contributor Covenant 2.1. |
| [`SECURITY.md`](SECURITY.md) | How to report a concern. |
| [`CHANGELOG.md`](CHANGELOG.md) | Versioned history of the specification. |
| [`LICENSE`](LICENSE) | Apache-2.0 — applies to shapes, schemas, and code. |
| [`LICENSE-docs`](LICENSE-docs) | CC BY 4.0 — applies to the specification text. |

> **Roadmap.** Machine-readable RDF vocabulary, SHACL shapes, and a worked
> example instance are planned but not yet part of this cut. See the
> [CHANGELOG](CHANGELOG.md) for the current scope.

## Relationship to the Two Pillars

The Product Framework is a conformant instantiation of the **Two Pillars
Specification Framework**: every construct maps to a named Two Pillars concept
(see [§8 of the spec](docs/product-framework.md#8-conformance-to-the-two-pillars)).
The Two Pillars foundation defines the standard; this framework is one
opinionated way to satisfy it for software.

## Conformance at a glance

Conformance is cumulative; an instance claims the highest level it satisfies:

1. **Described** — a machine-readable What exists (domain + event model, bounded
   contexts, mappings); interesting behaviour has a Decider, simulated sound and
   complete before any code.
2. **Realised** — a conformant How exists, including a repository layout model;
   work units reference the What and How by pointer.
3. **Verified** — verifications of all required kinds exist, meet the coherence
   bar, gate acceptance, and back the rationale trace.
4. **Delivered** — features and releases are graph partitions; "done" is a
   computed predicate.

## License

Dual-licensed by asset class:

- **Specification text** — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) ([`LICENSE-docs`](LICENSE-docs))
- **Shapes, schemas, code** — [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) ([`LICENSE`](LICENSE))

## Maintainer

Maintained by **Emil ([@Hafeok](https://github.com/Hafeok))**. For conduct or
security concerns, open an issue or contact the maintainer via GitHub.

> Replace this line with your preferred public name and contact if different —
> `CODE_OF_CONDUCT.md` and `SECURITY.md` point here for the maintainer reference.
