"""Report drift between the three surfaces that describe the same work.

The same facts are hand-written in three places, deliberately -- each renders for a
different medium and GitHub sanitises profile READMEs, so no single source can produce
all three:

  index.html                  the site
  llms.txt                    plain-text mirror for LLM crawlers
  ../pleiadian53-profile/     profile README, rendered at github.com/pleiadian53

Only a narrow set overlaps: the project roster, identity strings, and spelling. Everything
else (publications, JSON-LD, the schematic, sitemap, CSS) lives on the site alone. This
checks the overlap and stays out of the rest.

Usage:
    python3 scripts/check_sync.py [--profile PATH]

Exits 1 if anything has drifted, so it works as a pre-push or pre-commit hook.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROFILE = ROOT.parent / "pleiadian53-profile" / "README.md"

# Identity strings that must agree everywhere. Drift here is the expensive kind: it
# splits the search entity that ties the two names to one person.
IDENTITY = {
    "name (goes by)": "Barnett Chiu",
    "name (publishes as)": "Po-Hsiang Chiu",
    "ORCID iD": "0000-0001-8816-9799",
    "Zenodo DOI": "zenodo.21696681",
}

# The site settled on US spelling. These are the forms that keep creeping back.
UK_FORMS = ["tumour", "labelled", "labelling", "factorisation", "modelling", "behaviour"]

# Em dashes are kept to one or two per document at most. Used heavily they make prose
# read as over-edited, and they are a common tell of machine-written text.
EM_DASH_BUDGET = 2


def strip_markup(html: str) -> str:
    """Drop tags and JSON-LD so prose checks never match attribute names.

    Without this, searching for "labelled" hits every aria-labelledby attribute -- a
    blanket substitution on that basis once silently broke ten of them.
    """
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    return re.sub(r"<[^>]+>", " ", html)


def site_projects(html: str) -> list[str]:
    """Canonical roster: the first token of each project card's <h3>.

    Handles both linked cards (<h3><a ...>ssl-lab</a></h3>) and private ones
    (<h3>nmdiff <span class="tag">private</span></h3>).
    """
    names = []
    for card in re.findall(r'<article class="proj.*?</article>', html, re.S):
        h3 = re.search(r"<h3>(.*?)</h3>", card, re.S)
        if h3:
            text = strip_markup(h3.group(1)).split()
            if text:
                names.append(text[0])
    return names


def dois(text: str) -> set[str]:
    found = re.findall(r"10\.\d{4,9}/[^\s\"'<>)\]]+", text)
    return {d.rstrip(".,;").lower() for d in found}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--profile", type=Path, default=DEFAULT_PROFILE,
                    help=f"path to the profile README (default: {DEFAULT_PROFILE})")
    args = ap.parse_args()

    html = (ROOT / "index.html").read_text()
    llms = (ROOT / "llms.txt").read_text()
    prose = strip_markup(html)

    surfaces = {"index.html": html, "llms.txt": llms}
    if args.profile.is_file():
        surfaces["profile README"] = args.profile.read_text()
    else:
        print(f"note: profile README not found at {args.profile} -- skipping its checks\n")

    problems = []

    print("PROJECT ROSTER")
    roster = site_projects(html)
    print(f"  {len(roster)} projects on the site")
    for name in roster:
        missing = [s for s, t in surfaces.items() if name not in t]
        if missing:
            problems.append(f"project '{name}' missing from: {', '.join(missing)}")
            print(f"  DRIFT  {name} -- absent from {', '.join(missing)}")
    if not any(p.startswith("project") for p in problems):
        print("  ok     present on every surface")

    print("\nIDENTITY STRINGS")
    for label, needle in IDENTITY.items():
        missing = [s for s, t in surfaces.items() if needle not in t]
        if missing:
            problems.append(f"{label} ('{needle}') missing from: {', '.join(missing)}")
            print(f"  DRIFT  {label}: absent from {', '.join(missing)}")
        else:
            print(f"  ok     {label}")

    print("\nDISPLAY NAME")
    # The title is "<name><separator><tagline>". Accept any separator the page may use,
    # so changing it is a style decision rather than a reason for this check to fail.
    title = re.search(r"<title>([^<]*?)\s*(?:&middot;|&mdash;|·|—|\|)", html)
    h1 = re.search(r"<h1>(.*?)</h1>", html)
    heads = {"<title>": title.group(1).strip() if title else "?",
             "<h1>": strip_markup(h1.group(1)).strip() if h1 else "?"}
    if "profile README" in surfaces:
        m = re.search(r"^#\s+(.+)$", surfaces["profile README"], re.M)
        heads["profile README heading"] = m.group(1).strip() if m else "?"
    for where, value in heads.items():
        print(f"  {where}: {value}")
    if len(set(heads.values())) > 1:
        problems.append(f"display name differs across surfaces: {heads}")
        print("  DRIFT  these should all match")
    else:
        print("  ok     consistent")

    print("\nSPELLING (US forms expected)")
    for form in UK_FORMS:
        hits = [s for s, t in surfaces.items()
                if form in (prose if s == "index.html" else t).lower()]
        if hits:
            problems.append(f"UK spelling '{form}' in: {', '.join(hits)}")
            print(f"  DRIFT  '{form}' in {', '.join(hits)}")
    if not any(p.startswith("UK spelling") for p in problems):
        print("  ok     no UK forms found")

    print(f"\nEM DASHES (budget: {EM_DASH_BUDGET} per document)")
    for name, text in surfaces.items():
        n = (prose if name == "index.html" else text).count("—")
        if n > EM_DASH_BUDGET:
            problems.append(f"{name} has {n} em dashes (budget {EM_DASH_BUDGET})")
            print(f"  DRIFT  {name}: {n}")
        else:
            print(f"  ok     {name}: {n}")
    readme = ROOT / "README.md"
    n = readme.read_text().count("—")
    if n > EM_DASH_BUDGET:
        problems.append(f"README.md has {n} em dashes (budget {EM_DASH_BUDGET})")
        print(f"  DRIFT  README.md: {n}")
    else:
        print(f"  ok     README.md: {n}")

    print("\nPUBLICATION DOIs (site vs llms.txt)")
    only_site = dois(html) - dois(llms)
    only_llms = dois(llms) - dois(html)
    for d in sorted(only_site):
        problems.append(f"DOI on site but not in llms.txt: {d}")
        print(f"  DRIFT  only on the site: {d}")
    for d in sorted(only_llms):
        problems.append(f"DOI in llms.txt but not on site: {d}")
        print(f"  DRIFT  only in llms.txt: {d}")
    if not only_site and not only_llms:
        print(f"  ok     {len(dois(html))} DOIs agree")

    print()
    if problems:
        print(f"{len(problems)} drift(s) found:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("All surfaces in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
