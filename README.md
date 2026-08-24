# Colorado Construction Intelligence

Sales-focused public building-permit intelligence for **new single-family, multifamily, and commercial construction**.

## v0.1

- Aurora public Building Permits ArcGIS collector
- permit normalization, qualification, scoring and persistent history
- source health: technical status, freshness, record-volume anomalies and cached-data reporting
- sortable/filterable browser dashboard
- builder/GC rollups
- RSS feeds: all new construction, single-family, multifamily, commercial and top opportunities
- GitHub Actions every six hours and automatically after code changes on `main`
- GitHub Pages deployment

The initial automated source is Aurora because its official open-data layer is queryable and exposes permit number, issue date, permit/building type, project description, valuation and address. See `docs/SOURCE_DIRECTORY.md` for the broader Colorado rep-prospecting directory and next collectors.

## GitHub Pages

Set **Settings → Pages → Source → GitHub Actions**. The launch commit triggers the workflow automatically; you can also run it manually from Actions.

## Local run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m colorado_permits.main
python -m http.server 8000 -d public
```
