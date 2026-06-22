# Contributing

Proposals, conformance reports, and reference tooling are welcome. This is a
specification project, so most contributions are changes to the normative text
in [`docs/product-framework.md`](docs/product-framework.md) or evidence about
how the spec behaves in practice.

## What you can contribute

- **Specification proposals** — clarifications, corrections, or additions to the
  spec. Open an issue describing the problem before a large pull request, so the
  shape of the change can be agreed first.
- **Conformance reports** — a description of a real instance and which
  conformance level ([§8.1](docs/product-framework.md#81-conformance-levels)) it
  reaches, including where the spec was ambiguous or hard to satisfy. These are
  the most valuable input to the standard's evolution.
- **Reference tooling** — RDF vocabulary, SHACL shapes, validators, scaffolders.
  These are licensed under Apache-2.0 (see below).

## Principles for spec changes

The framework defines **shapes and rules only**. Keep contributions on the right
side of the open/closed line ([§1](docs/product-framework.md#1-purpose-and-scope)):

- The framework is the *empty form and its rules*. Specific products,
  archetypes, patterns, Decider logic, and the content of verifications are built
  *on* the framework — they do not belong in the spec.
- A proposed rule should **earn its place**: it must be checkable, and it should
  protect a stated property. A rule no instance needs is documentation, not a
  conformance rule.
- Prefer reusing an existing standard (globs, OpenAPI, SHACL, …) over inventing a
  new mechanism — the same "use the standard" discipline the spec itself follows.

## Versioning and compatibility

The specification is versioned; see [`CHANGELOG.md`](CHANGELOG.md). Breaking
changes follow a documented deprecation policy so that existing conformant
instances are never silently invalidated. A change that would invalidate
previously-conformant instances must be called out explicitly and given a
deprecation path.

## Licensing of contributions

By contributing you agree that your contribution is licensed under the
repository's dual scheme: specification **text** under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), and **shapes, schemas,
and code** under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
