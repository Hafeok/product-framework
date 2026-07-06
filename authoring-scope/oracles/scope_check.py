#!/usr/bin/env python3
"""
scope_check — the two authoring-scope oracles.

1. ENFORCEMENT (per tool submission):
   Everything a tool authors must be within its declared scope. Authorship of an
   excluded kind is rejected regardless of content quality — a tool cannot say
   what it is not sanctioned to say. Gaps split into two distinct findings that
   demand different actions from different people:
     - unauthored-within-scope : the tool COULD have authored this and didn't
                                 (fix in the tool — e.g. annotate the frame in Figma)
     - outside-scope           : no amount of work in this tool can author this
                                 (route to a sanctioned author — e.g. product-cli)

2. COMPLETENESS JOIN (across all connected tools):
   A What specification is complete when every required element kind is authored
   by SOME sanctioned tool within its scope. The join reports, per required kind:
   covered (and by whom), coverable-but-unauthored (a connected tool could author
   it), or uncovered (no connected tool's scope includes it — a new author is
   needed). This is the §3.5-style bidirectional discipline applied to authorship:
   nothing required left unauthored, nothing authored out of sanction.

Run:  python3 scope_check.py --self-test
"""
import json, sys, pathlib


def load(p): return json.load(open(p))


def authored_kinds(scope):
    return {a["kind"] for a in scope["authors"]}


# ---------------------------------------------------------------- 1. enforcement
def enforce(scope, submission):
    """
    submission: {"authored": [{"kind": ..., "element": ...}, ...],
                 "unauthored-candidates": [{"kind": ..., "element": ...}, ...]}
    'authored' is what the adapter extracted as authored meaning.
    'unauthored-candidates' is what the adapter suspects needs authorship
    (the annotation-needed list, pre-split).
    """
    ok_kinds = authored_kinds(scope)
    excluded = set(scope["excluded"])
    findings = {"accepted": [], "rejected-out-of-scope": [],
                "unauthored-within-scope": [], "outside-scope": []}

    for item in submission.get("authored", []):
        k = item["kind"]
        if k in excluded:
            findings["rejected-out-of-scope"].append(
                {**item, "basis": f"'{scope['tool']}' is excluded from authoring '{k}' — rejected regardless of content"})
        elif k in ok_kinds:
            findings["accepted"].append(item)
        else:
            findings["rejected-out-of-scope"].append(
                {**item, "basis": f"'{k}' is not in '{scope['tool']}''s declared authors list"})

    for item in submission.get("unauthored-candidates", []):
        k = item["kind"]
        if k in ok_kinds:
            findings["unauthored-within-scope"].append(
                {**item, "action": f"authorable in {scope['tool']} — author it there (e.g. annotate)"})
        else:
            findings["outside-scope"].append(
                {**item, "action": "not authorable in this tool — route to a sanctioned author"})

    valid = not findings["rejected-out-of-scope"]
    return valid, findings


# ---------------------------------------------------------------- 2. completeness join
def completeness_join(required_kinds, scopes, authored_by_tool):
    """
    required_kinds : the What-element kinds a complete specification needs
    scopes         : list of scope declarations (all connected tools)
    authored_by_tool: {tool-name: set of kinds actually authored (accepted)}
    """
    report = {}
    for kind in required_kinds:
        authors = [s["tool"] for s in scopes if kind in authored_kinds(s)]
        did = [t for t in authors if kind in authored_by_tool.get(t, set())]
        if did:
            report[kind] = {"status": "covered", "by": did}
        elif authors:
            report[kind] = {"status": "coverable-but-unauthored", "candidates": authors}
        else:
            report[kind] = {"status": "uncovered",
                            "detail": "no connected tool's scope includes this kind — a sanctioned author is needed"}
    complete = all(v["status"] == "covered" for v in report.values())
    return complete, report


# ---------------------------------------------------------------- self-test
def _self_test():
    here = pathlib.Path(__file__).parent
    figma = load(here / "../reference/figma.authoring-scope.json")
    passed = total = 0

    def case(name, cond):
        nonlocal passed, total
        total += 1
        passed += bool(cond)
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")

    # --- enforcement
    sub = {
        "authored": [
            {"kind": "aio", "element": "tz-field"},
            {"kind": "page-graph", "element": "settings-screen"},
            {"kind": "decider", "element": "no-overlap-rule"},          # excluded!
        ],
        "unauthored-candidates": [
            {"kind": "aio", "element": "mystery-dropdown"},  # within scope, unauthored
            {"kind": "event", "element": "booking-events"},       # outside scope
        ],
    }
    valid, f = enforce(figma, sub)
    case("out-of-scope authorship rejected (decider via Figma)", not valid and len(f["rejected-out-of-scope"]) == 1)
    case("in-scope authorship accepted (aio, composition)", len(f["accepted"]) == 2)
    case("gap split: mystery-dropdown -> within-scope (fix in Figma)",
         len(f["unauthored-within-scope"]) == 1 and f["unauthored-within-scope"][0]["element"] == "mystery-dropdown")
    case("gap split: event -> outside-scope (route elsewhere)",
         len(f["outside-scope"]) == 1 and f["outside-scope"][0]["element"] == "booking-events")

    # --- completeness join
    pcli = {"tool": "product-cli", "adapter": "native", "excluded": [],
            "authors": [{"kind": k} for k in
                        ["domain-structure", "trigger", "command", "event", "view",
                         "decider", "projector", "accessibility-criteria"]]}
    required = ["aio", "page-graph", "accessibility-criteria",
                "domain-structure", "event", "decider", "journey"]
    authored = {"figma": {"aio", "page-graph", "accessibility-criteria"},
                "product-cli": {"domain-structure", "event", "decider"}}
    complete, rep = completeness_join(required, [figma, pcli], authored)
    case("join: aio covered by figma", rep["aio"]["status"] == "covered" and rep["aio"]["by"] == ["figma"])
    case("join: decider covered by product-cli", rep["decider"]["status"] == "covered")
    case("join: criteria covered (partial authors compose)", rep["accessibility-criteria"]["status"] == "covered")
    case("join: journey UNCOVERED (no connected author)", rep["journey"]["status"] == "uncovered")
    case("join: overall incomplete because journey uncovered", not complete)

    # now connect a journey author and re-join
    miro = {"tool": "miro", "adapter": "miro-bridge", "excluded": [],
            "authors": [{"kind": "journey"}]}
    authored["miro"] = {"journey"}
    complete2, rep2 = completeness_join(required, [figma, pcli, miro], authored)
    case("join: connecting a journey author completes the What", complete2)

    print(f"\n{passed}/{total} self-test cases passed")
    return passed == total


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        sys.exit(0 if _self_test() else 1)
    print(__doc__)
