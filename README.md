# WonderSearch effort check

The [WonderSearch docs](https://docs.evokoa.com/wondersearch/search/effort-and-limits) say to try the same questions at Small, Medium and Large and compare the passages and charges. This script does that: it runs a question list at all three efforts and records where the right passage ranks, how long each search took, and what it cost.

## Test run (Oct 31, 2026)

Three WonderSearch blog posts as the collection, five questions worded the way a user would ask them:

- [A search bill that follows your questions](https://wondersearch.ai/blog/a-search-bill-that-follows-your-questions/)
- [Semantic search without the embedding project](https://wondersearch.ai/blog/semantic-search-without-the-embedding-project/)
- [Give your AI something worth reading](https://wondersearch.ai/blog/give-your-ai-something-worth-reading/)

| Effort | Right passage ranked first | Avg time | Cost per search |
|---|---|---|---|
| Small | 5 of 5 | 1.6 s | $0.001 |
| Medium | 5 of 5 | 2.8 s | $0.0025 |
| Large | 5 of 5 | 3.0 s | $0.01 |

Total cost of the run: $0.0675. Three short documents is an easy test, so this shows the method, not that Small wins on large collections. Full rows are in `results.json`.

## Run it

```
pip install wondersearch
# put your API key in ~/.config/wondersearch/key
python effort_check.py <folder of .md files> results.json --upload   # first run uploads the docs
python effort_check.py <folder of .md files> results.json            # later runs just search
```

Edit `QUESTIONS` in the script: each question comes with a short phrase that has to appear in the right passage.
