# endurance-rea.com

Static website for Endurance Real Estate Advisors (NYC commercial real estate brokerage).

- `site/` is the deployable folder. `wrangler.jsonc` tells Cloudflare Workers to serve it (build command: none, deploy command: `npx wrangler deploy`, root directory: `/`).
- `tools/build.py` generates every HTML page, `sitemap.xml` and `robots.txt`. Article text lives in `tools/articles.py`, FAQ content in `tools/faqs.py`, shared settings in `tools/common.py`. After editing, run `python3 tools/build.py`.
- `content-inventory.md` lists everything from the old site, `sitemap-plan.md` is the new structure, and `REPORT.md` covers placeholders, redirects and deployment.

Local preview: `cd site && python3 -m http.server 8080`, then open http://localhost:8080
