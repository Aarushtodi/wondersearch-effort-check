"""WonderSearch proof run: 3 public blog posts, 5 reworded questions x Small/Medium/Large.
Scores where the right passage lands (gold = a sentence a reader needs), plus cost and time."""
import os, re, sys, json, time
from pathlib import Path
from wondersearch import WonderSearch

DOCS = Path(sys.argv[1])
QUESTIONS = [  # worded the way a user would ask, not the blog's words
    ("If nobody searches for a whole month, what am I still paying for?",
     ["Keep the collection but run no searches"]),
    ("How much does it cost to just keep a gigabyte of files sitting there?",
     ["$0.33 per GB per month"]),
    ("Should I check what the search pulled up before I trust the chatbot's reply?",
     ["read the retrieved material before reading the generated answer"]),
    ("Do I have to build and run my own vector pipeline?",
     ["you do not operate a separate embedding pipeline"]),
    ("What kinds of tricky test questions should I put in my test set?",
     ["Add near misses", "Include awkward wording, exact identifiers"]),
]
norm = lambda s: re.sub(r"\s+", " ", s).replace("’", "'").lower()

with WonderSearch(api_key=Path("~/.config/wondersearch/key").expanduser().read_text().strip()) as c:
    drive = c.drives.list()[0]["id"]
    if "--upload" in sys.argv:
        files = sorted(str(p) for p in DOCS.glob("*.md"))
        for f in files:
            b = c.upload(f, external_id=Path(f).stem, drive_id=drive)
            print("uploaded", Path(f).name, [r.status for r in b.files])
    rows = []
    for effort in ("small", "medium", "large"):
        for q, golds in QUESTIONS:
            t = time.time()
            r = c.search(q, effort=effort, drive_id=drive, group_by_document=False)
            secs = time.time() - t
            rank = next((i + 1 for i, p in enumerate(r.results)
                         if any(norm(g) in norm(p.text) for g in golds)), None)
            rows.append(dict(effort=effort, q=q, rank=rank, n=len(r.results), secs=round(secs, 2),
                             cost=r.usage.get("cost"), served=r.raw.get("effort_served"),
                             top=r.results[0].text[:160] if r.results else "", warnings=r.warnings))
            print(effort, rank, len(r.results), f"{secs:.1f}s", r.usage.get("cost"), r.raw.get("effort_served"), "|", q[:50])
    Path(sys.argv[2]).write_text(json.dumps(rows, indent=1))
