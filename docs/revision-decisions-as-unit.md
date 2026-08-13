# Product Framework — Revision: decisions as the unit across all phases

> # ⛔ DRAFT — NOT CANON. NOT PREVIEW. NOT NORMATIVE.
>
> **This document is a revision proposal awaiting the principal's ruling. It is not part of the
> specification and nothing in it may be cited, implemented, or conformed to.**
>
> | | |
> |---|---|
> | **Status** | Draft for the principal's ruling — **unruled** |
> | **Filed** | 2026-08-13 |
> | **Author** | Draft authored outside this repo; filed here unaltered in §§1–6 and §9 |
> | **Applies to** | The Product Framework specification, currently **1.10.0** |
> | **Spec version this would produce** | None assigned. A version is assigned *if and when* it is ruled on and folded in. |
> | **Ruling** | *(unruled — see [§8](#8-open-decisions-for-the-principal))* |
>
> **What it proposes to change.** That **the decision becomes the unit of account across all three
> phases** — What enumerates decisions, How allocates them, Build discharges them. Today the phases
> have different units: What and How produce documents, Build produces files. Under this proposal
> the contracts, validators, and repo layout keep their roles but stop being the *measure* of a
> phase's completion and become evidence within it.
>
> **Where this sits in this repo's status ladder.** This repo publishes material at two
> established statuses: the **normative body** (`docs/product-framework.md` §§1–10) and
> **🅿 Preview** (§§11–14 — published, coherent with the body, not yet normative, *already accepted
> into the specification document*). This document is **below both**: it is not in the
> specification document at all, has not been accepted, and may be rejected in whole. Where this
> document and `docs/product-framework.md` appear to differ, **`docs/product-framework.md` governs,
> normative body and Preview sections alike.**
>
> **If you are an agent or a tool surveying `docs/`:** the only authoritative document in this
> directory is [`product-framework.md`](product-framework.md). Do not treat this file as spec, do
> not derive from it, do not implement against it, and do not answer questions about the framework
> from it. Its §§1–6 and §9 are one person's argument, not an agreed position.

**Status:** draft for the principal's ruling. Not canon until accepted and filed in the framework
repo. Two reframes, deliberately in one revision because they are one change seen from two ends.

**What it changes.** Today the framework's phases have different units: What and How produce
documents, Build produces files. This revision makes **the decision the unit throughout** — What
enumerates decisions, How allocates them, Build discharges them. Everything else in the
framework is unchanged; the contracts, validators, and repo layout keep their roles, but they
stop being the *measure* of a phase's completion and become evidence within it.

---

## 1. Why

Two diagnoses, both from the framework's own instruments.

**Build measures the wrong store.** A build phase organised around file creation measures
transcription — the cheap store. Two builds can produce identical file trees where one encodes
the Decider's invariants in the type system and the other leaves them in comments; a
file-shaped completion predicate cannot tell them apart. That is a maximal proxy gap at exactly
the point where the What's demand is supposed to become machine-checkable.

**Elicitation is ungoverned.** When a model helps author What and How, nothing verifies that the
output is complete, honest, or grounded. The specification is a document the model wrote, and
its quality is assessed by reading it. Meanwhile the decision machinery — allocation, coverage,
readiness, acceptance — sits one phase downstream, unused where it would do the most good.

Both are the same defect: demand is being handled in a store nobody is counting.

## 2. What: enumeration

**The What phase produces an enumerated decision set, not a document.**

Its product is the set of decisions the product must settle, each with a statement, at a
declared tolerance floor. The prose document remains — as a **projection** of the set for human
readers, generated or maintained alongside, never the source of truth.

- The set is a ledger `DecisionSet` with a tolerance floor (§4.2.1 floor semantics: up-only
  overrides, effective tier hashed).
- Enumeration may be model-assisted (§5).
- Completion is not "the document reads well". It is **the readiness gate**: no unallocated
  decisions before produce.

**Instrument:** late-discovery rate — decisions added to the set after its readiness gate, by
stage. This is the direct measure of enumeration quality and should fall with practice on a task
type. A model-assisted What that leaks decisions during build is a *measured* elicitation
failure, not a vague one.

## 3. How: allocation

**The How phase allocates each enumerated decision to a store.**

The vocabulary already exists in the ledger's `Allocation` sum type and needs no new invention:
**constraint** (encoded — type system, schema, analyzer, IaC policy), **criterion** (a test or
acceptance predicate, with its stage), **judgment** (a named human at a named stage), or
**escaped** (priced: exposure, acceptor, review date).

- Repo layout, contracts, and interfaces remain How content — but as **decomposition claims**,
  not target trees: each declared boundary must encode something about the verdict, and the
  contract at that boundary is the seam declaration. Validation is seam-shaped (the ddd
  interceptor and CI diff), not tree-matching.
- Allocation may be model-proposed and **must be human-accepted** (§5).
- Where the predicate catalog holds a closure claim for a decision's shape, the allocation cites
  it — this is where accumulated findings from prior engagements pay out to a new project
  instead of being re-derived.

**Completion:** every enumerated decision has an allocation. That is the readiness gate, and it
is mechanical.

## 4. Build: discharge

**The Build phase discharges allocated decisions. Files are the medium, not the deliverable.**

The unit of build work is not "create file X" but **"discharge decision D into store S, verified
by discharge ref R"** — where R is the ledger's typed `DischargeRef`: a type signature, a test
id, an analyzer rule, a contract clause, a `what-if` assertion, an OTel metric-plus-expectation,
a named actor, or the CI contract check.

- **Completion predicate: coverage.** Every enumerated decision has a discharge ref or a priced
  escape. Not "all files generated".
- `product decider derive` is the existing precedent — What in, executable signature out, no
  file framing anywhere in its contract. This revision generalises that shape to the phase.
- Files, layout, and structure are validated as before; they are evidence that a discharge
  landed, not the measure of whether the phase is done.

**Instrument:** encoded-demand coverage by store — a real progress measure where file counts
never were.

> **Folded in 2026-08-13, after drafting — finding F9.** Source: `product-cli`,
> [`docs/demo-runbook.md`](https://github.com/Hafeok/product-cli/blob/main/docs/demo-runbook.md),
> finding **F9**, from the demo rehearsal. Cited, not reproduced; the runbook governs its own text.
>
> **The defect.** `product build` renders **`no How contract loaded`** for every product. The cause
> is in the loader, not the contract: `load_how()` probes three legacy paths and resolves the
> product through `default_product_name()` rather than the `--product` argument it was given. The
> How contract itself is intact — `how show` reads the same contract correctly. This is a
> straightforward loader bug and is filed as such; it is not evidence of anything wrong with the
> How contract, the How phase, or the artefact kinds §6 leaves unchanged.
>
> **Why it is also a datapoint for §4.** Under a file-shaped completion predicate, `build` passed
> its own measure while unable to read the How at all. Nothing in the phase's notion of "done"
> depended on the How having been loaded, so nothing surfaced the failure — it took a demo
> rehearsal, watching output a human read, to find it. That is consistent with §1's claim that the
> build phase's completion measure is not load-bearing: a coverage predicate (every enumerated
> decision carries a discharge ref) would have had nothing to compute and would have failed closed.
>
> **What this is not.** One loader bug in one CLI is not proof of the reframe. It is a single
> observation, found by a method (human rehearsal) that this revision does not propose to replace,
> and a file-shaped predicate is not the only thing that could have caught it — an ordinary
> assertion that the loader returns a contract would also have. It is admitted here as an instance
> of the failure mode §1 describes, at the weight of one instance, and it is a **defect to fix in
> `product-cli` regardless of how this revision is ruled on**. Fixing it is not in this revision's
> scope, and this revision must not be treated as the reason to fix it.

## 5. The model's boundary — propose, ground, check

Model assistance is admitted at every phase under one boundary, stated once and applying
throughout.

**The model may:**
- **propose** — enumerate candidate decisions, draft statements, suggest allocations, surface
  decisions the set is missing;
- **ground** — cite upstream claims through the basis cone (company canon, framework claims,
  catalog closure claims), pinned by SHA;
- **check** — run gates, compute coverage, flag decisions with no discharge, surface
  contradictions between allocations.

**The model may not:** accept; set or raise a tolerance floor; price an escape; ratify a status;
sign anything. `accepted-by` never resolves to a model identity — enforced mechanically (L006),
not by convention.

**Working shape:** an elicitation session's product is a **batch awaiting the principal's
ruling** — the curation discipline, applied to product specification. Proposals land as
allocated-awaiting-acceptance; the human rules per entry; the accepted set is the What/How.

**Consequence worth stating plainly:** this makes specification *authorship* delegable and
specification *authority* non-delegable. The model does the enumeration labour; the human
carries the answerability. That is the framework's own accountability-completeness result
applied to its own process.

> **Folded in 2026-08-13, after drafting — the seam's actual state.** Source: the same `product-cli`
> demo rehearsal, [`docs/demo-runbook.md`](https://github.com/Hafeok/product-cli/blob/main/docs/demo-runbook.md).
> Recorded there as an observation of the seam rather than under a numbered finding, so it is cited
> by document only; there is no finding id to quote. Cited, not reproduced.
>
> **The check half of §5 is partly built, not wholly planned.** `ddd what --product acme` already
> classifies the product store's What boundaries **against the same policy table the code path
> uses** — one table, two callers, not two implementations that happen to agree. On the rehearsal's
> product it reported **8 surface elements, 0 declared, in roughly 25 ms**. So the §5 verb *check*
> — run gates, compute coverage, flag decisions with no discharge — is not a capability this
> revision must first invent at the What boundary; a working instance of it exists, is fast enough
> to run inline, and shares its policy with the code path rather than restating it. §5 should be
> read as **extending a built seam**, and the §7 sequencing below is amended to match.
>
> **What remains untrue today, stated plainly.** Two things, and neither is softened by the above:
>
> 1. **`product build` never consults `.decisions/`.** Not partially, not by a different name — the
>    build path does not read the decision store at all. Everything §4 proposes about discharge
>    refs and coverage-as-completion is unbuilt on the build side.
> 2. **The two "done" definitions are computed by different code over different stores.** The
>    What-side classification above and whatever `product build` calls complete are separate
>    computations over separate stores, with no shared predicate and nothing that would detect them
>    disagreeing. The single unit this revision argues for does not exist yet; what exists is one
>    end of it.
>
> Together these bound the claim: the classifier is a real precedent for §5's *check*, and it is
> **not** evidence that the §2–§4 reframe is underway. The seam is built on the What side and
> absent on the Build side, which is precisely the asymmetry §7 has to sequence around.

## 6. What does not change

- The four artefact kinds, the contracts, and the validators keep their current roles.
- The repo layout stays in How and stays validated — its meaning changes (decomposition claim,
  not target tree), its presence does not.
- Prose documents remain, as projections. Nothing here forbids writing well; it forbids the
  document being the unit of account.
- No new stores, no new vocabulary: allocation, discharge, coverage, and tolerance all come from
  the ledger spec as it stands.

## 7. Dependencies and sequencing

*Dependency states verified 2026-08-13. This list is the answer to "what could actually be built
today?" — it is meant to be readable without asking anyone.*

| Dependency | Needed for | State as of 2026-08-13 |
|---|---|---|
| **M8** — discharge-ref kinds, content-hash pins | §4 (Build: discharge) | **Shipped and merged.** Available now. |
| **L4** — federation / upstreams resolution | the *ground* verb in §5 | **Not started.** No work underway. |
| **Cross-repo basis-ref amendment** | citing upstream claims across repo boundaries | **Not landed.** |
| **Predicate catalog seeding** | §3's closure-claim payoff | Ongoing; value scales with seeding, arrives with the catalog. |
| **What-boundary classifier** (`ddd what --product`) | the *check* verb in §5 | **Built** — see the §5 addendum. Shares the code path's policy table. |
| **Build-side `.decisions/` read** | §4, and a single "done" | **Does not exist.** See the §5 addendum. |

**What this means for sequencing.**

- **Available today:** everything §4 needs from **M8** — the discharge-ref kinds and the
  content-hash pins the build phase leans on are shipped and merged, so the build side is not
  blocked on a dependency; it is blocked only on being built.
- **Available today, partly:** §5's *check*. A working What-boundary classifier already runs
  against the code path's own policy table (§5 addendum). The Build-side half of *check* — coverage
  over discharge refs — has nothing to run against, because `product build` does not read
  `.decisions/`.
- **Not available:** §5's *ground*. **L4 (federation) has not started**, and the **cross-repo
  basis-ref amendment has not landed**. Without upstreams resolution, product decisions cite
  framework and company claims **by convention only** — which is to say the citation is unpinned
  and unverified. *Propose* and *check* work without L4; *ground* does not, and no partial
  workaround should be read into the classifier's existence: it classifies within one store and
  resolves nothing upstream.
- **Arrives later regardless:** the predicate catalog's usefulness to §3 scales with its seeding.
  The payoff is real but arrives with the catalog, not with this revision.

**Consequence for any implementation sequenced off this list:** the only §5 verb fully unavailable
today is *ground*, and it is unavailable for two independent reasons (L4, the amendment), either of
which alone would block it. An implementation that needs grounding is blocked on work that has not
begun; an implementation of *propose* and *check* is not blocked on anything external.

## 8. Open decisions for the principal

> **This repo has no decision store, and none was invented for this document.** The Product
> Framework repo carries canon as **plain versioned documents** — the normative spec
> (`docs/product-framework.md`), `CHANGELOG.md`, `CONFORMANCE.md` — with no `.ddd/`, no
> `.decisions/`, and no issue-backed or file-backed register of open decisions. The absence is not
> an oversight this document should route around: the repo **records it as a known gap in its own
> conformance statement** — [`CONFORMANCE.md` § Known gaps](../CONFORMANCE.md#known-gaps), the
> *What/How Open Questions* row: "no dedicated owner-tagged 'Open Questions' artifact with an
> explicit 'what it blocks' field", with an explicit note that promoting an Open-Question node kind
> is under consideration for a future cut.
>
> So the four questions below are filed as **clearly marked open decisions in this document**, not
> as entries in a store. Each carries the two fields that conformance row names as missing —
> **owner** and **what it blocks** — plus a blank **ruling** line, so a verdict can be written in
> place. That shape is borrowed from the repo's own description of the artifact it does not yet
> have; it does not constitute such an artifact, and creating one is a spec change outside this
> revision's scope. **Every entry below is unruled.**

---

### OD-1 — Set granularity in a product context

**Question.** One decision set per feature, per epic, or per release?

**Why it is a decision and not a detail.** The tolerance floor is per-set and up-only, so **set
boundaries are consequence boundaries**. Drawing them is a real design act, not a bookkeeping
choice, and it cannot be deferred to implementation without the implementation making it.

**Options.** Per feature · per epic · per release · something else the principal names.

**Instrument.** Override-rate per set — a floor drawn wrong shows up as a high override rate on
that set.

**Blocks.** §2 (What: enumeration) cannot specify what a `DecisionSet` scopes to; the readiness
gate has no defined subject.
**Does not block.** §4, §5's *check*, or the F9 fix.

**Owner.** The principal.
**Ruling.** *(unruled)*

---

### OD-2 — Generated or maintained What projection

**Question.** Does the What prose document get **generated** from the decision set, or
**maintained alongside** it?

**Why it is a decision and not a detail.** §2 makes the set the source of truth and the document a
projection either way; this decides whether the projection can drift from its source at all. The
trade is stated in the draft and not resolved by it: generated is consistent by construction and
reads worse; maintained reads better and can drift.

**Options.** Generated from the set · maintained alongside · generated with a maintained overlay,
if the principal wants a third.

**Blocks.** §2's projection clause; any tooling that would render or lint the What document.
**Does not block.** Enumeration itself, or §3's allocation.

**Owner.** The principal.
**Ruling.** *(unruled)*

---

### OD-3 — Where a product decision set lives

**Question.** Does a product's decision set live **in the product repo**, or **in a Context&
engagement repo that pins the product's**?

**Why it is a decision and not a detail.** It is the same publish-and-pin question the corpus
already answered for canon, asked now for product decisions. It determines who can write a set,
what a pin refers to, and whether a set outlives an engagement.

**Options.** Product repo · engagement repo pinning the product's · both, with a stated direction
of pinning.

**Blocks.** Any storage or addressing work; and it interacts with the **cross-repo basis-ref
amendment**, which has not landed (§7) — an engagement-repo answer needs that amendment, a
product-repo answer does not.
**Does not block.** §2/§3/§4's content, which are storage-agnostic as drafted.

**Owner.** The principal.
**Ruling.** *(unruled)*

---

### OD-4 — Elicitation session shape

**Question.** Does the model enumerate from a brief **in one pass**, presenting batches for
ruling, or **interview iteratively**?

**Why it is a decision and not a detail.** §5 fixes the model's boundary (propose / ground / check;
never accept) under either shape, so this is not a boundary question — it is a question about what
the principal's time is spent on. The draft's own statement of the trade: the iterative shape
produces better sets and costs more principal time, which is the scarce resource by construction.

**Options.** One-pass batch · iterative interview · one-pass with an iterative escalation path for
flagged entries.

**Blocks.** Any elicitation tooling; and it sets what the late-discovery-rate instrument (§2) is
measuring across, since the two shapes are not comparable on that instrument without a stated
baseline.
**Does not block.** §5's boundary rules, which hold under either.

**Owner.** The principal.
**Ruling.** *(unruled)*

## 9. Falsifiers

- **Late-discovery rate does not fall with practice** on a repeated task type → model-assisted
  enumeration is not learning, and the What phase's new unit buys nothing over the document.
- **Coverage-complete builds ship the same defect classes** as file-complete builds → discharge
  refs are ceremony over the same work, and the build reframe is wrong.
- **Allocation proposals are accepted almost unchanged** → either the model is very good or the
  human is rubber-stamping; the second is the failure mode, and the tell is that accepted
  allocations later prove wrong at the same rate as unreviewed ones.
- **Set-boundary design proves undecidable in practice** — override rates high everywhere → the
  per-set floor does not fit product work, and tolerance needs a different granularity here than
  it has in the tooling corpus.

---

## 10. Filing record

*Not part of the proposal. A record of what this document is and how it got here, so that a reader
can tell the principal's argument from the filing around it.*

**Filed** 2026-08-13, in `product-framework` — the repo the revision governs. It is a Product
Framework spec change; filing it in a downstream consumer would invert provenance.

**Unaltered from the draft as received:** §§1–6 and §9. The argument is the principal's and stands
as written until ruled on. Two addenda were *appended* to §4 and §5 — clearly marked, dated, and
separable — rather than woven into the draft's prose, so that nothing in §§1–6 has been restated or
rewritten.

**Added in filing:**

| Change | Where |
|---|---|
| Draft-status block | Top of document |
| Finding **F9** folded in as defect + datapoint, with its limits stated | §4 addendum |
| The seam's actual state folded in; what remains untrue stated plainly | §5 addendum |
| Dependency list rebuilt against reality as of 2026-08-13 | §7 |
| Four open questions restructured as unruled, owner-tagged, blocking-scoped entries | §8 |
| This record | §10 |

**Citations, not imports.** Both folded findings come from the `product-cli` demo rehearsal
recorded in that repo's [`docs/demo-runbook.md`](https://github.com/Hafeok/product-cli/blob/main/docs/demo-runbook.md).
Its text is not reproduced here; where this document's summary and that runbook differ, **the
runbook governs its own findings**. F9 carries a finding id; the seam-state observation does not,
and is cited by document only rather than given an id it does not have.

**Not done, deliberately.** No implementation of anything the revision proposes. No phase changes,
no tooling, no metamodel edits, no `product-cli` changes (including the F9 loader fix, which is
that repo's to make and is not contingent on this ruling). No L4 or basis-ref-amendment work. The
four open decisions are unanswered. This document is not registered in `CHANGELOG.md`, which
records **accepted** changes to the specification at an assigned version — an unruled proposal has
neither, and listing it there would be the promotion this filing is designed to prevent.

**On a ruling.** If accepted, the change lands in `docs/product-framework.md` under the repo's
normal versioning discipline (`CONTRIBUTING.md`, `CHANGELOG.md`), at a version assigned then, and
this file is removed or reduced to a pointer. If rejected, this file is deleted or archived with
the verdict recorded. Until one of those happens it stays exactly what its header says it is.
