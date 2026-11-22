# Sitemap Plan: New endurance-rea.com

## Who the business serves
Endurance Real Estate Advisors is a NYC commercial real estate brokerage with two lines of business:

1. **Tenant representation ("Tenant Advocate")**: companies leasing, renewing, expanding or relocating office space. Their problem: landlords hold the information and the leverage. Endurance's answer is the proprietary Tenant Advantage Analysis (TAA).
2. **Landlord representation**: building owners, investors, and condo and coop boards leasing office and retail space. Their problem: vacancy, slow lease-up, the wrong tenants. Endurance's answer is positioning, targeted marketing and negotiation.

Tenant work is clearly the lead offer (most testimonials, all 5 articles, the proprietary TAA), so the new site leads with tenants and gives landlords a clear second path.

## Conversion strategy
- **Hero on every page** states the customer's problem plus a single primary CTA ("Schedule a Consultation" goes to /contact/; phone always one tap away).
- **Proof early:** the stats bar (1,850+ transactions, 30+ years, $3B volume) sits directly under the home hero; testimonials appear on Home, both service pages and About.
- **Sticky header** with click-to-call phone and "Contact" button on every screen; on mobile the phone and CTA stay visible in the header bar.
- **Two-path chooser** on Home ("I'm a tenant" / "I'm a landlord") so each visitor self-selects into the right service page.
- **One CTA per page**, repeated in a closing CTA band.
- **Merged thin/duplicate pages:** Team + Join Us folded into About; Blog + Pulse & Perspective merged into Insights; two confusing contact slugs merged into one /contact/.

## Page structure

| # | New URL | Page | Purpose | Primary target keyword | Secondary keywords | Primary CTA | Old content moved here |
|---|---|---|---|---|---|---|---|
| 1 | `/` | Home | Hook both audiences, show proof, route to the right service | NYC commercial real estate broker | commercial real estate advisors Manhattan, office leasing NYC | Schedule a consultation | Home hero line, intro, both service blurbs, Gregory Gang quote, 2 long testimonials, About stats, contact strip |
| 2 | `/services/` | Services overview | Hub that explains both services side by side and links down | commercial real estate services NYC | tenant and landlord representation | Schedule a consultation | Home service blurbs, landlord asset types |
| 3 | `/services/tenant-representation/` | Tenant Representation | Convert tenants: problem, TAA, results, proof, FAQs | tenant representation NYC | commercial tenant broker NYC, office lease negotiation, Tenant Advantage Analysis | Request a Tenant Advantage Analysis consult | All of /tenant-advocate; tenant testimonials (Shemesh, Berdzeni, Gofshteyn, Levine, Gulati, Ibragimov, Jenna); article teasers |
| 4 | `/services/landlord-representation/` | Landlord Representation | Convert owners and boards: positioning, strategy, proof, FAQs | landlord representation NYC | office leasing agent NYC, retail leasing NYC, condo and coop commercial leasing | Discuss your property | All of /landlord-representation; landlord testimonials (Jerome, Classi); 116 Nassau lease result |
| 5 | `/about/` | About & Team | Build trust: philosophy, stats, team, careers | about Endurance Real Estate Advisors | NYC commercial real estate team, Gregory Gang | Contact the team | All of /about, all of /contact-us (Team), all of /join-us (as "Join our team" section) |
| 6 | `/insights/` | Insights | Topical authority for AEO; one hub for all articles | NYC commercial leasing insights | tenant lease advice NYC | Talk to an advisor | /pulse-perspective and /blog index |
| 7 | `/insights/tribeca-prep-leases-116-nassau-street/` | Article | Deal announcement / proof | 116 Nassau Street office space | Financial District office lease | Inquire about availability | Blog post 2358641 |
| 8 | `/insights/self-help-clause-commercial-lease-nyc/` | Article | Answer "what is a self-help clause" | self-help clause commercial lease | NYC office lease tenant protections | Talk to an advisor | Blog post 2332136 |
| 9 | `/insights/why-sndas-matter-to-tenants/` | Article | Answer "what is an SNDA" | SNDA for tenants | subordination non-disturbance attornment | Talk to an advisor | Blog post 2270447 |
| 10 | `/insights/lessons-from-a-landlords-troubles/` | Article | Distressed-landlord leverage | distressed landlord tenant leverage NYC | landlord foreclosure tenant rights | Talk to an advisor | Blog post 2337620 |
| 11 | `/insights/renewals-shrinking-ti-allowances/` | Article | TI allowance and renewal strategy | tenant improvement allowance renewal | net deal office lease | Talk to an advisor | Blog post 2272979 |
| 12 | `/faq/` | FAQ | AEO hub: 14 grouped Q&As with FAQPage schema | commercial real estate broker FAQ NYC | how tenant representation works, who pays the broker | Schedule a consultation | Facts drawn from all pages and articles |
| 13 | `/contact/` | Contact | Single conversion endpoint: form, phone, email, map link | contact NYC commercial real estate broker | 136 Madison Ave office | Send message / Call | /contact-us- form and contact block; Join Us form (via "Careers" topic) |
| 14 | `/404.html` | Not found | Recover lost visitors | n/a | n/a | Go home | New |

## Navigation
- **Header:** Services (Tenant Representation, Landlord Representation) · About · Insights · FAQ · [phone] · **Contact** button
- **Footer:** logo + one-line description, NAP block, services links, company links, social links, newsletter note.

## Schema plan
| Page | Schema |
|---|---|
| Home | `RealEstateAgent` (a LocalBusiness subtype) with name, phone, email, address, geo-free, areaServed, sameAs, founder, `WebSite` |
| Services hub | `ItemList` of services, `BreadcrumbList` |
| Each service | `Service` (provider = business, areaServed), `FAQPage`, `BreadcrumbList` |
| About | `AboutPage` + `Person` entries for the team, `BreadcrumbList` |
| Insights hub | `Blog` / `CollectionPage`, `BreadcrumbList` |
| Each article | `Article`, `BreadcrumbList` |
| FAQ | `FAQPage`, `BreadcrumbList` |
| Contact | `ContactPage`, `BreadcrumbList` |

## Redirect map (301)
| Old URL | New URL |
|---|---|
| `/about` | `/about/` |
| `/tenant-advocate` | `/services/tenant-representation/` |
| `/landlord-representation` | `/services/landlord-representation/` |
| `/contact-us` (Team page) | `/about/#team` (served as `/about/`) |
| `/contact-us-` | `/contact/` |
| `/join-us` | `/about/#careers` (served as `/about/`) |
| `/pulse-perspective` | `/insights/` |
| `/blog` | `/insights/` |
| `/blog/post/2358641/tribeca-prep-leases-116-nassau` | `/insights/tribeca-prep-leases-116-nassau-street/` |
| `/blog/post/2332136/self-help-in-today-s-leasing-market` | `/insights/self-help-clause-commercial-lease-nyc/` |
| `/blog/post/2270447/why-sndas-matter-to-tenants` | `/insights/why-sndas-matter-to-tenants/` |
| `/blog/post/2337620/lessons-from-a-landlord-s-troubles` | `/insights/lessons-from-a-landlords-troubles/` |
| `/blog/post/2272979/renewals-and-shrinking-ti-allowances` | `/insights/renewals-shrinking-ti-allowances/` |

These are implemented in `site/_redirects` (Cloudflare Pages format).
