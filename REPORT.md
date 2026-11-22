# Launch Report: endurance-rea.com Rebuild

## What was delivered
| Item | Location |
|---|---|
| Deployable static site (14 pages, CSS, JS, images, sitemap.xml, robots.txt, 404.html, `_redirects`, `_headers`) | `site/` |
| Content inventory of the old site | `content-inventory.md` |
| New sitemap and conversion plan | `sitemap-plan.md` |
| Generator that rebuilds every page from one source file | `tools/build.py` (run `python3 tools/build.py`) |

**Quality checks (local, Lighthouse 12 mobile):** Home 98/100/100/100, Tenant Representation 100/100/100/100, FAQ 100/100/100/100, Contact 100/100/100/100, longest article 97/100/100/100 (Performance / Accessibility / Best Practices / SEO). Every page has exactly one H1, alt text and width/height on every image, valid JSON-LD, no broken internal links, no horizontal scroll at 390px, and no em dashes.

## 1. Placeholders that need real info
Every placeholder is shown on the page with a yellow highlight (`<mark class="ph">`), so you can find them visually or by searching the HTML for `class="ph"`. Edit the text in `tools/build.py` and re-run the build.

| Placeholder | Page(s) | Notes |
|---|---|---|
| [CONFIRM: office hours] | /contact/ | Also add `openingHoursSpecification` to the LocalBusiness schema in `build_home()` (a comment marks the spot). |
| [CONFIRM: fee structure for tenant and landlord assignments] | /faq/ | |
| [CONFIRM: landlord fee and commission structure] | /services/landlord-representation/ (also in that page's FAQ schema) | |
| [CONFIRM: typical timeline from first meeting to signed lease] | /faq/ | |
| [CONFIRM: other boroughs or markets served] | /faq/ | The site only says "across NYC". |
| [CONFIRM: New York State real estate broker license details] | /faq/ | No license info anywhere on the old site. |
| [ADD BIO: Gregory Gang] and [ADD BIO: Sergio Turaev] | /about/ | The old site has no bios. |
| [ADD HEADSHOT] x3 | /about/ | Mark Levy, Jim Torre, Steven Andersen have no photos. |
| [ADD TESTIMONIAL HERE] with [Client name] and [Title, Company] | /about/ | One open slot. All 9 real testimonials are already used. |
| [CONFIRM: author] x5 | Every article | Posts are written in the first person by a broker with 30+ years of experience (probably Gregory Gang). Once confirmed, also change the `author` in the Article schema. |
| [CONFIRM: original publish date] x5 | Every article | The old site shows November 20, 2026 on all five posts, which looks like a re-publish date. |

**Other items to confirm (no visible placeholder):**
- **Headshots.** Matched to names by card order on the old Team page (first card = Gregory Gang, second = Sergio Turaev).
- **LinkedIn URL.** The old link was a broken Proofpoint-wrapped *admin* URL. The new site uses `https://www.linkedin.com/company/1560494/`.
- **Contact form delivery.** With no service connected, the form opens the visitor's email app with the message filled in and addressed to greg.gang@endurance-rea.com. To get submissions sent straight to an inbox, set `data-endpoint` on the form in `build_contact()` to a form service (Formspree, a Cloudflare Pages Function, etc.).
- **Newsletter.** The old site had a Constant Contact signup pop-up. It was left out because it needs a list endpoint; it can be added back.
- **Stock photography.** The "thumbs up" group photo on About and the two Unsplash images on articles appear to be stock. Their alt text does not claim they show the Endurance team.

## 2. Old URL to new URL redirects (301)
These are already set up in `site/_redirects`, which Cloudflare Pages applies automatically.

| Old URL | New URL |
|---|---|
| /about | /about/ |
| /tenant-advocate | /services/tenant-representation/ |
| /landlord-representation | /services/landlord-representation/ |
| /contact-us (old Team page) | /about/ (team section) |
| /contact-us- | /contact/ |
| /join-us | /about/ (careers section) |
| /pulse-perspective | /insights/ |
| /blog | /insights/ |
| /blog/post/2358641/tribeca-prep-leases-116-nassau | /insights/tribeca-prep-leases-116-nassau-street/ |
| /blog/post/2332136/self-help-in-today-s-leasing-market | /insights/self-help-clause-commercial-lease-nyc/ |
| /blog/post/2270447/why-sndas-matter-to-tenants | /insights/why-sndas-matter-to-tenants/ |
| /blog/post/2337620/lessons-from-a-landlord-s-troubles | /insights/lessons-from-a-landlords-troubles/ |
| /blog/post/2272979/renewals-and-shrinking-ti-allowances | /insights/renewals-shrinking-ti-allowances/ |
| /blog/* (anything else) | /insights/ |

## 3. What could not be crawled
All 14 URLs loaded (HTTP 200). Notes:
- `/blog?page=2` shows the same three posts, loaded client-side. The blog sitemap confirms there are 5 posts in total, and all 5 were captured.
- The LinkedIn link (behind urldefense.com, pointing at an admin page) was not followed.

## Deploying to Cloudflare Pages
1. Create a Pages project connected to this repository.
2. Framework preset: **None**. Build command: *(leave empty)*. Build output directory: **`site`**.
3. Add the custom domain `endurance-rea.com`. The canonical tags and sitemap use `https://endurance-rea.com` without `www`, so redirect `www` to the apex.
4. After launch, submit `https://endurance-rea.com/sitemap.xml` in Google Search Console and Bing Webmaster Tools.
