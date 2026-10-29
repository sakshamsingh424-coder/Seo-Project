# AI-Powered SEO Audit & Optimization Platform (Milestone 1)
Rule-based on-page and technical SEO analysis with a Streamlit dashboard.

## Run
    pip install -r requirements.txt
    streamlit run app.py

## Structure
- `auditor.py` – rules engine (title, meta, H1, headings, alt text, content length, links, keyword usage, HTTPS, speed, canonical, viewport, indexability, Open Graph, JSON-LD, robots.txt, sitemap.xml) and weighted 0-100 scoring
- `pages/1_Before_After_Case_Study.py` – before vs after SEO case study page (same demo site: score 29 -> 99, issues 17 -> 1)
- `sample_pages.py` – offline demo pages and case-study data
- `app.py` – dashboard: score cards, filterable issue table with fixes, keyword chart, JSON/CSV export

## Planned (Milestone 2)
LLM-generated fix suggestions, multi-page crawling, score history.
