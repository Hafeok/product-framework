# The Render Contract (PREVIEW)

**A derived, design-system-agnostic projection of the What that a renderer consumes to put a screen on a surface.**

> 🅿 **PREVIEW.** Companion to §11 of the specification. The render contract is the *missing half* of the design-system coupling: §11's manifest says **what a design system can render**; the render contract says **what there is to render**. They meet at the renderer: `render(render_contract, manifest?) → surface`. With a manifest, rendering is concrete; without one, a generic AIO renderer falls back to wireframe fidelity — which is the proof the contract is sufficient on its own.

## What it is, and is not

- It is a **pure projection of the What-graph** — derived, read-only, regenerated on every change. It is never hand-authored and cannot drift (the same discipline as "diagrams are derived projections of the live graph").
- It is the **serialized Abstract UI** (the AUI level of §3.2.2) made consumable: the abstract interactions, their data bindings, states, transitions, and accessibility obligations — and nothing design-system-specific.
- It is **not** the §11 manifest (that is the design system's self-description), and **not** the What-graph itself (which carries invariants, rationale, and provenance a renderer does not consume).

## Structure

A render contract is a **page graph** — an application root plus screens (one per UI step) and the `navigate` edges between them — plus the **scenario** whose simulated Projector output populates the screens with real data.

```jsonc
{
  "contract_version": "preview-0",
  "title": "Checkout",
  "context": { "form_factor": "phone", "modality": "touch" },
  "locale": "en",

  "content_store": {                         // resolve(key, locale) -> string (§4.6)
    "checkout.review.heading": { "role": "heading",       "en": "Review your order" },
    "cart.empty.message":      { "role": "empty-message", "en": "Nothing to check out yet — add something." }
  },

  "root": {                                  // the application root (§3.2.4)
    "destinations": [                        // its out-edges = the global nav
      { "to": "ui-browse",   "label": "Browse" },
      { "to": "ui-orders",   "label": "Orders" },
      { "to": "ui-review-cart", "label": "Cart" }
    ],
    "global_actions": [                       // trigger-actions valid app-wide
      { "issues": "cmd-sign-out", "label": "Sign out" }
    ]
  },

  "flows": [                                  // named subgraphs of the page graph
    { "id": "flow-checkout", "entry": "ui-review-cart",
      "pages": ["ui-review-cart","ui-choose-payment","ui-confirmation"] }
  ],

  "screens": [ /* … UI steps as before … */ ],
  "scenario": { /* … given/then with embedded projected output … */ }
}
```

Each screen is as documented below; the new top-level pieces are `root` (the global navigation a renderer draws as chrome) and `flows` (the named subgraphs, so a renderer can show where in a task the user is).

```jsonc
{
  "contract_version": "preview-0",
  "title": "Checkout",
  "context": { "form_factor": "phone", "modality": "touch" },  // the context of use (§3.2.2)

  "screens": [
    {
      "id": "ui-review-cart",
      "intent": "Confirm what you're buying before paying",   // residue only; not rendered as a control (§3.2.1)
      "projection": "rm-cart-summary",                        // the read model surfaced (§3.2)
      "state_space": ["present", "empty", "loading", "failed"],// declared states (§3.2)
      "state_meanings": {
        "empty":   "Nothing to check out — go add something",
        "loading": "Fetching your cart",
        "failed":  "Couldn't load your cart — retry"
      },
      "elements": [
        {
          "aio": "display-collection",      // the abstract interaction (§3.2.2)
          "role": "the line items",
          "binds": "rm-cart-summary.items", // data binding -> projection field
          "item_shape": [                   // each field + its DOMAIN TYPE (§3.1)
            { "field": "name",  "type": "string" },
            { "field": "qty",   "type": "integer" },
            { "field": "price", "type": "money" }
          ],
          "wcag": ["1.3.1"]                 // obligations inherited from the AIO (§3.2.3)
        },
        {
          "aio": "display-value",
          "role": "the total owed",
          "binds": "rm-cart-summary.total",
          "value_type": "money",
          "emphasis": "primary",            // what to stress (§3.2.1) — meaning, not style
          "wcag": ["1.3.1"]
        },
        {
          "aio": "trigger-action",
          "role": "proceed to payment",
          "issues": "cmd-begin-payment",    // the command this offers (§3.2.1)
          "emphasis": "primary",
          "transitions_to": "ui-payment",   // makes it clickable (§3.2.1)
          "wcag": ["2.5.8", "2.4.7"]
        }
      ]
    }
  ],

  "scenario": {                              // the given/when/then that feeds the preview (§3.4)
    "given": [
      { "event": "ev-item-added", "data": { "name": "Coffee beans", "qty": 2, "price": 1800 } },
      { "event": "ev-item-added", "data": { "name": "Filter papers", "qty": 1, "price": 600 } }
    ],
    "projected": {                           // simulated Projector OUTPUT, embedded — real data, not lorem ipsum
      "rm-cart-summary": {
        "state": "present",
        "items": [
          { "name": "Coffee beans", "qty": 2, "price": 1800 },
          { "name": "Filter papers", "qty": 1, "price": 600 }
        ],
        "total": 4200
      }
    }
  }
}
```

## Field reference

| Field | From | Why a renderer needs it |
|---|---|---|
| `context` | §3.2.2 context of use | selects which reification a manifest applies; generic renderer notes it |
| `screens[].projection` | §3.2 `projects` | which read model backs the screen |
| `screens[].state_space` + `state_meanings` | §3.2 / §3.2.1 | which empty/loading/failed states exist and what they mean |
| `elements[].aio` | §3.2.2 AIO | the abstract control to render (generic default, or reified via manifest) |
| `elements[].binds` / `item_shape` / `value_type` | §3.1 domain types | what data to show and how to draw each typed field |
| `elements[].issues` / `transitions_to` | §3.2.1 | the command fired and the next screen — makes it clickable |
| `elements[].emphasis` | §3.2.1 | what to stress (a renderer may honour or ignore) |
| `elements[].wcag` | §3.2.3 | obligations the rendered control must carry |
| `screens[].content` / `state_content` | §3.2.1 / §4.6 | content keys (heading, state prose) resolved against the content store, never literals |
| `content_store` + `locale` | §4.6 | resolves each content key to a string for the locale |
| `scenario.projected` | §3.4 Projector simulation | the real data the preview displays |

## The generic-renderer contract

A renderer that consumes this with **no manifest** must map each AIO to a canonical default control (`single-select` → a generic picker, `display-collection` → a generic list, `trigger-action` → a generic button, …) and draw each `item_shape` field by its domain type. If the screen renders and is walkable from the render contract *alone*, the contract is complete — that is the test. Plugging a §11 manifest in then swaps the generic defaults for real components without changing the contract.
