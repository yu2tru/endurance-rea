# Launch Report: endurance-rea.com Rebuild

## What was delivered
| Item | Location |
|---|---|
| Deployable static site (14 pages, CSS, JS, images, sitemap.xml, robots.txt, 404.html, `_redirects`, `_headers`) | `site/` |
| Content inventory of the old site | `content-inventory.md` |
| New sitemap and conversion plan | `sitemap-plan.md` |
| Generator that rebuilds every page | `tools/build.py` (layout and pages), `tools/articles.py`, `tools/faqs.py`, `tools/common.py`. Run `python3 tools/build.py` |

**Quality checks (local, Lighthouse 12 mobile):** Home 98/100/100/100, Tenant Representation 100/100/100/100, FAQ 100/100/100/100, Contact 100/100/100/100, longest article 97/100/100/100 (Performance / Accessibility / Best Practices / SEO). Every page has exactly one H1, alt text and width/height on every image, valid JSON-LD, no broken internal links, no horizontal scroll at 390px, and no em dashes.

## Revision 2: design and content pass

### Content recovered and where it went
| Recovered from the official site | Where it is now |
|---|---|
| Headshots for Mark Levy, Jim Torre and Steven Andersen | About, team section (all five members now have photos) |
| Personal LinkedIn profiles for Gregory Gang, Sergio Turaev, Mark Levy, Jim Torre | About, team cards ("LinkedIn profile"), plus `sameAs` in the Person schema |
| Steven Andersen's card link (company page) | About, team card ("Company LinkedIn") |
| Correct company LinkedIn URL | Footer, Contact page, LocalBusiness `sameAs` |
| Atlas at Rockefeller Center photo (old homepage) | About hero |
| Meeting photo (old homepage) | Home "Every assignment starts with your goals" section, Contact hero |
| Handshake photo (old About) | FAQ hero |
| Note-taking and handshake photos (old Tenant Advocate) | Tenant Representation page |
| Stacked-hands photo (old Team page) | About, Careers section |

### Placeholders removed
- [ADD HEADSHOT] x3: filled with the real headshots.
- [ADD BIO] for Gregory Gang and Sergio Turaev: no bios exist on the site (see below). The visible placeholders were removed and each card links to the person's LinkedIn profile instead.
- [ADD TESTIMONIAL HERE]: removed. All 9 real testimonials are published, and an empty slot made the page look unfinished.
- [CONFIRM: author] and [CONFIRM: original publish date] on articles: removed from view. Articles now show "Endurance Real Estate Advisors" and the date the site itself shows (November 20, 2026).

## 1. Placeholders remaining (and why)
I checked every page, every blog post and the builder's embedded page data. None of these facts appear anywhere on endurance-rea.com.

| Placeholder | Page | Why it remains |
|---|---|---|
| [CONFIRM: office hours] | /contact/ | Hours are not listed anywhere. Add `openingHoursSpecification` to the schema in `build_home()` once confirmed. |
| [CONFIRM: fee structure for tenant and landlord assignments] | /faq/ | No pricing or fee information on the site. |
| [CONFIRM: landlord fee and commission structure] | /services/landlord-representation/ | Same. |
| [CONFIRM: typical timeline from first meeting to signed lease] | /faq/ | Only one data point exists (75 spaces over 9 months), which is quoted in the answer. |
| [CONFIRM: other boroughs or markets served] | /faq/ | The site only says "across NYC". |
| [CONFIRM: New York State real estate broker license details] | /faq/ | No license information on the site. |

**Not placeholders, but worth adding if the client has them:** short bios for each team member (none exist on the site), the real author and original publish date of each article, and a personal LinkedIn URL for Steven Andersen.

**Still to set up:**
- **Contact form delivery.** With no service connected, the form opens the visitor's email app with the message filled in and addressed to greg.gang@endurance-rea.com. To get submissions sent straight to an inbox, set `data-endpoint` on the form in `build_contact()` to a form service.
- **Newsletter.** The old Constant Contact signup pop-up was left out because it needs a list endpoint.

### Fonts chosen
- **Headings:** Barlow Condensed (500, 600, 700). It's semi-condensed with a tall x-height and a confident, architectural feel.
- **Body:** Barlow (400, 500, 600, italic 400), the companion family, so the type reads as one system. Body text is 18px with a 1.6 line height.
- Loaded from Google Fonts with `display=swap`, preconnect hints and a non-blocking stylesheet load.

### Design changes
- Removed every eyebrow label, including the dash-prefixed ones.
- Replaced card grids with editorial layouts: alternating photo and text splits, rows separated by thin dividers, and a large pull quote followed by a two-column list of testimonials. Cards remain only for team members and articles, with no borders, shadows or icons.
- Replaced the numbered process cards with a short narrative ("Every assignment starts with your goals") beside a meeting photo.
- Heroes are now 85vh on the home page and 62vh on inner pages. The dark gradient sits only behind the text (left side on desktop, bottom on mobile), and each photo has its own desktop and mobile focal point.
- The palette is restrained: charcoal, warm neutrals, and the logo red as the single accent. Section spacing is larger.

### Unchanged SEO and AEO work
All titles, meta descriptions, canonical tags, Open Graph and Twitter tags, JSON-LD (LocalBusiness, Service, FAQPage, Article, BreadcrumbList, AboutPage, Blog), FAQ content, alt text, internal links, sitemap.xml, robots.txt and redirects are unchanged or expanded. Lighthouse (mobile, local): Home 97/100/100/100, About 96/100/100/100, Tenant Representation 100/100/100/100, FAQ 100/100/100/100, longest article 93/100/100/100.

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

## Deploying to Cloudflare (Workers)
The repo includes `wrangler.jsonc`, which serves the `site/` folder as static assets (with `_redirects`, `_headers` and the custom 404 page).
1. In the Worker's **Settings > Builds**: Build command *empty*, Deploy command `npx wrangler deploy`, Root directory `/`, Production branch `main`.
2. The `name` in `wrangler.jsonc` (`endurance-rea`) must match the Worker's name in the dashboard. If the build reports a name mismatch, change it there.
3. Add the custom domain `endurance-rea.com` under the Worker's **Settings > Domains & Routes**. Canonical tags and the sitemap use `https://endurance-rea.com` without `www`, so redirect `www` to the apex.
4. After launch, submit `https://endurance-rea.com/sitemap.xml` in Google Search Console and Bing Webmaster Tools.
