# endurance-rea.com

Static website for Endurance Real Estate Advisors (NYC commercial real estate brokerage).

- `site/` is the deployable folder (Cloudflare Pages build output directory: `site`, no build command).
- `tools/build.py` generates every HTML page, `sitemap.xml` and `robots.txt`. Edit content there, then run `python3 tools/build.py`.
- `content-inventory.md` lists everything from the old site, `sitemap-plan.md` is the new structure, and `REPORT.md` covers placeholders, redirects and deployment.

Local preview: `cd site && python3 -m http.server 8080`, then open http://localhost:8080
