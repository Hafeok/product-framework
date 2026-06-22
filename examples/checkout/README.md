# Worked example — Checkout

**A small but complete What, carried down the whole chain: domain → events → Decider → Projector → UI steps → AIOs → page graph → reification + content → verification.**

> This example is the specification's own conformance demonstration. It is written to exercise the parts that are easy to *claim* and hard to *do*: a **derived** read model with a real Projector (not just CRUD), a **named-algorithm primitive** (the Polanyi floor), the **page graph**, **content references**, and both **Preview provider profiles** (§11 design system, §12 content store). If the chain composes here, the spec earns its claims; where it fights back, that is a finding.

It targets the four conformance levels (§8.1): **Described → Realised → Verified → Delivered**. Files in this folder:

| File | What it is |
|---|---|
| `README.md` | this walkthrough — the full What (§§1–6) and its verification & delivery story |
| `design-system.manifest.yaml` | a conforming design system (§11) |
| `content-store.manifest.yaml` | a conforming content store (§12) |

---

## 1. The What — domain (§3.1)

One bounded context, **Ordering**. Ubiquitous language: *Cart*, *Line Item*, *Order*, *Payment Method*.

```
Cart (aggregate)
  has many   LineItem { product: Product, qty: Integer≥1, unit_price: Money }
  invariant  CART-1: a Cart in `checking-out` has at least one LineItem
  invariant  CART-2: qty ≥ 1 for every LineItem

Order (aggregate)
  created-from  a Cart at payment authorization
  has           order_no: OrderNo (value object), total: Money, placed_at: Instant
```

`Money` is a value object (minor units, integer); `OrderNo` is a value object with a checksum (relevant in §4).

**Reference data (What, §3.1)** — constitutive instance data the behaviour depends on:

```
shipping-methods:  [ standard, express, pickup ]      -- a single-select draws options from here
tax-categories:    [ standard, reduced, zero ]
currencies:        [ EUR ]
```

These are in the What because behaviour references them: "tax category must be one
of the declared set" is checkable only because the set is modelled, and the
payment-method `single-select` (§6) draws its options from declared reference data,
not thin air.

**Production data (oracle, not What)** — the live catalog (4,200 products), real
orders. Not specification; instead the **data-conformance** oracle (§6.3): the
declared shapes are validated against real data. If the catalog holds a product
with `unit_price` of 0, or a `tax-category` outside the declared three, that is a
finding — either the data is wrong or the model is. This is the data practitioner's
check, and it catches what the structure side alone never sees.

## 2. The What — events & commands (§3.2)

```
commands → events                                    changes / targets
─────────────────────────────────────────────────────────────────────
cmd-add-item        → ev-item-added                  targets Cart, changes Cart
cmd-begin-payment   → ev-payment-begun               targets Cart  (guards CART-1)
cmd-authorize-pay   → ev-payment-authorized          targets Cart
                    | ev-payment-declined
cmd-place-order     → ev-order-placed                targets Order, changes Order
```

Read models (`projects`), **with declared state spaces** (§3.2):

```
rm-cart-summary        projects Cart        states: present, empty, loading, failed
rm-payment-options     projects (config)    states: present, loading, failed
rm-order-confirmation  projects Order       states: present, loading
```

`rm-cart-summary` is the interesting one: it is **not** a CRUD view — its `total`
is a fold over the line items, so it needs a real Projector (§4).

## 3. The What — the Decider (§3.3)

The Cart aggregate's behaviour, derived signature + authored logic:

```
decide(cart, cmd-begin-payment):
    reject CART-1  if cart.items is empty            -- invariant, executable
    else accept [ ev-payment-begun ]

decide(cart, cmd-authorize-pay { method }):
    accept [ ev-payment-authorized { method } ]      -- (gateway result modelled below as a primitive)

evolve(cart, ev-item-added e):  cart.items += LineItem(e)      -- aggregate state fold
```

Simulated **before realisation** against a flow scenario:

```
given  [ ]                                   (empty cart)
when   cmd-begin-payment
then   Rejected(CART-1)                       ✓ sound: empty cart cannot check out

given  [ ev-item-added{Coffee,2,1800} ]
when   cmd-begin-payment
then   Accepted[ ev-payment-begun ]           ✓ complete: valid cart proceeds
```

Command coverage holds: every command targeting Cart is handled. ✓

## 4. The What — the Projector (§3.4) — the part that matters

`rm-cart-summary` folds events into a view whose `total` is **computed**, so the
`projects` pointer alone derives nothing — it needs a Projector.

```
project(state, ev-item-added e):
    state.items += { name: e.name, qty: e.qty, price: e.qty * e.unit_price }
    state.total  = sum(item.price for item in state.items)
    state.state  = "present"          -- present once any item exists; empty before

-- conformance (mirrors the Decider):
--   no foreign events:   folds only ev-item-added (the events rm-cart-summary projects) ✓
--   event coverage:      every event changing Cart that the view shows is folded        ✓
--   output containment:  produces only { items, total, state } — the declared fields     ✓
```

Simulated before realisation:

```
given  [ ev-item-added{Coffee,2,1800}, ev-item-added{Filter,1,600} ]
then   { items:[{Coffee,×2,€36.00},{Filter,×1,€6.00}], total:€42.00, state:"present" } ✓
given  [ ]
then   { items:[], total:€0.00, state:"empty" }                                          ✓
```

The fold is **mechanical**: its only variability (sum, line subtotal) is declared
arithmetic over a generic fold engine — so it rejoins the mechanical region (§3.5).
Contrast the next item.

## 5. A named-algorithm primitive (§3.5 — the Polanyi floor)

`OrderNo` carries a checksum so a mistyped order number is detectable. The checksum
is **not** derivable from declared rules — it is the **Damm algorithm**. So it is a
named-algorithm primitive, specified by reference, not folded:

```
primitive  ordernumber-checksum
  reference   "Damm algorithm (H. M. Damm, 2004), decimal check digit"
  io          (digits: String) -> check_digit: Digit
  oracle      [ ("3192", 4), ("0088", 6), ("4200", 0) ]      -- reference I/O pairs
  verified-by oracle-conformance     -- NOT behavioural simulation; there is no fold
```

This is the honest boundary: the framework does **not** pretend the checksum
regenerates from a rule-set. It is named, pinned by an oracle, and bounded. Everything
*else* in the example is mechanical; this one primitive is the irreducible kernel.

## 6. The What — UI steps & the page graph (§3.2.1, §3.2.4)

Three pages in the **checkout flow** (a named subgraph), reachable from an
application root that also exposes Browse and Orders.

```
[root] ──navigate──▶ Browse        (flow-browse)
       ──navigate──▶ Orders        (flow-orders)
       ──navigate──▶ Review cart ─▶ Choose payment ─▶ Order placed   (flow-checkout)
                         ▲                                   │
                         └───────────── navigate ◀───────────┘  (keep shopping)
```

UI step **Review cart** (`ui-review-cart`), specified as pure meaning:

```
intent:        "Confirm what you're buying before paying"   (debt — drive toward 0)
content:       heading → checkout.review.heading             (a content key, §4.6)
surfaces:      rm-cart-summary  as  display-collection (items) + display-value (total)
offers:        cmd-begin-payment  as  trigger-action (emphasis: primary)
transitions:   on ev-payment-begun → ui-choose-payment       (a navigate edge)
state space:   present | empty | loading | failed            (covering, §3.2)
  empty   → content cart.empty.message
  failed  → content cart.failed.message    (meaning is What; mechanism is How)
  loading → (waived: sub-perceptual on cached carts — reason recorded)
a11y:          inherited from AIOs — 1.3.1 (collection), 2.5.8 + 2.4.7 (action)
```

Note what is **not** here: no dropdown, no colour, no layout, no literal copy. Every
realisation term is absent by *type* (§3.2.2), not by discipline.

## 7. The How — reification & content (§4.5, §4.6)

The What above reifies through the design system manifest for `context = {phone, touch}`:

```
single-select × {phone, many}   → searchable-list      (from design-system.manifest)
trigger-action × {primary}      → primary-button
display-collection              → list
navigate × root                 → drawer                (the burger menu)
```

…and resolves content through the content store manifest for `locale = en`:

```
checkout.review.heading → "Review your order"
cart.empty.message      → "Nothing to check out yet — add something to get started."
cart.failed.message     → "Couldn't load your cart. Check your connection and retry."
```

Swapping `context` to `{tablet, pointer}` reifies `single-select` to a
`segmented-control` instead — **same What, different surface**. Swapping `locale` to
`es` resolves the same content keys to Spanish — **same What, different words**. That
is the pluggability the AUI layer and the two provider profiles exist to deliver.

## 8. Verification (§6) — what gates this example

| Check (§6.3) | On this example |
|---|---|
| Layout conformance | the repo tree matches the archetype's layout model |
| Behavioural simulation | the Decider §3 and Projector §4 are sound & complete *before* code |
| Oracle conformance | `ordernumber-checksum` matches Damm across its oracle pairs |
| Domain conformance | realised Cart/Order match §1; no structural drift |
| Data conformance | the live catalog validates against the declared shapes; reference data (shipping/tax/currency) is the closed set behaviour references |
| Behavioural conformance | realised behaviour & projection produce identical output to §3/§4 |
| Seam | every datum projected, every control a valid command, reification covers {phone,tablet}, every state covered or waived, every content key resolves for {en,es}, a11y machine criteria pass + attestations recorded |

Only when all pass is any artifact accepted (§6.1), and the rationale trace (§5)
retains only the principles those passing checks enforce.

## 9. Delivery (§7)

The checkout flow is one **feature** — a reference to its flow slice. Its domain
**footprint** is *derived*: `{Cart, LineItem, Order, Money, OrderNo}` — the concepts
its events change and its projections read, not a hand-listed set. `feature_done`
ranges over that footprint; the release cut is closed iff nothing in it depends on an
excluded element.

---

## What this example demonstrates about the spec

- **The mechanical/irreducible boundary is real and small.** Everything folded
  mechanically (the Projector) except one named primitive (the checksum). The spec's
  §3.5 claim — push everything into declared data, name-and-bound only what cannot —
  held when written out.
- **No realisation term appears in the What.** Section 6 is design-system-free *by
  type*, and Section 7 is where every concrete choice lives — the split survived a
  concrete instance.
- **One What, many surfaces.** phone/tablet and en/es are coupling choices, not forks.
- **The render contract** (`preview/render-contract.schema.md`) is exactly the
  projection of Sections 6–7 a renderer consumes; `preview/renderer.html` shows this
  flow running at wireframe fidelity.

> **Status.** The What and its verification story are expressed against the normative
> body (§§1–10). The two manifests exercise the Preview profiles (§§11–12); coupling
> them to a running renderer is the open experiment that would graduate those profiles
> to normative.
