"""FAQ content. Visible Q&A and FAQPage schema are both generated from these lists."""
from common import BIZ, ph

TENANT_FAQ = [
 ('What does a tenant representation broker do?',
  '<p>A tenant representation broker negotiates on behalf of the tenant, not the landlord, to secure the best possible lease terms. At Endurance, our sole fiduciary duty is to protect our clients’ interests. We provide the market data, landlord intel and negotiation strategy you need to make informed decisions throughout the process.</p>'),
 ('What is the Tenant Advantage Analysis?',
  '<p>The Tenant Advantage Analysis (TAA) is Endurance’s proprietary, confidential report on your specific leasing situation. It covers market insights such as rental rates, concessions and comparable properties, intel on your landlord’s motivations and negotiation history, and a customized strategy to secure the best possible lease terms.</p>'),
 ('Can you help me renew my current lease instead of moving?',
  '<p>Yes. Endurance negotiates renewals and expansions as well as relocations. One client toured over 75 spaces across 9 months before realizing that expanding within their current building made the most financial sense, and Endurance negotiated that new lease. In today’s market, renewing tenants may also benefit from <a href="/insights/renewals-shrinking-ti-allowances/">net deals as TI allowances shrink</a>.</p>'),
 ('When should I start looking for new office space?',
  '<p>Start your search 6 to 18 months before your current lease expires. That window allows time for thorough due diligence, market research and negotiation without pressure, and it gives you leverage if a renewal is also on the table.</p>'),
 ('What lease protections should NYC tenants ask for?',
  '<p>Key protections include a <a href="/insights/self-help-clause-commercial-lease-nyc/">self-help clause</a>, an <a href="/insights/why-sndas-matter-to-tenants/">SNDA</a>, and security protections in case of an ownership change. These matter more than ever with many NYC landlords under financial pressure. Always have a qualified real estate attorney review your lease.</p>'),
]

LANDLORD_FAQ = [
 ('What types of properties does Endurance lease for landlords?',
  '<p>Endurance leases buildings, office spaces, retail properties, and condo and coop commercial assets in New York City. We work with property owners, condo and coop boards, and investors in office or retail space.</p>'),
 ('How do you attract tenants to a property?',
  '<p>We attract tenants by crafting a narrative that showcases your property’s best features and competitive edge, then reaching the right prospects with focused, targeted marketing. Our leasing strategy is built on comprehensive market analysis to achieve optimal pricing and quality tenants.</p>'),
 ('How involved are you once a prospect is interested?',
  '<p>Very involved. From initial marketing to lease signing, we work closely with ownership to ensure a seamless transition from prospect to tenant, and our skilled negotiation delivers lease terms tailored to your objectives.</p>'),
 ('How are landlord leasing fees structured?',
  f'<p>{ph("CONFIRM: landlord fee and commission structure")} Endurance reviews compensation with ownership before an exclusive leasing engagement begins. Call {BIZ["phone"]} to discuss your property.</p>'),
]

FAQ = [
 ('Services', [
  ('What does Endurance Real Estate Advisors do?',
   '<p>Endurance Real Estate Advisors is a full-service commercial real estate brokerage and advisory firm in New York City that represents tenants and landlords in commercial leasing. We help tenants lease, renew, expand or relocate office space, and we help owners lease buildings, office, retail, and condo and coop assets. Our focus is attention to detail and exceeding clients’ expectations.</p>'),
  ('What is tenant representation?',
   '<p>Tenant representation means a broker negotiates exclusively on the tenant’s behalf to secure the best lease terms. As a tenant advocate, Endurance provides the market data, landlord intel and negotiation strategy tenants need to make informed decisions. Learn more about our <a href="/services/tenant-representation/">tenant representation services</a>.</p>'),
  ('What is the Tenant Advantage Analysis (TAA)?',
   '<p>The Tenant Advantage Analysis is Endurance’s proprietary, confidential report on a tenant’s specific leasing situation. It covers current rental rates, concessions and comparable properties, intel on the landlord’s motivations and negotiation history, and a customized negotiation strategy.</p>'),
  ('What types of properties do you lease for landlords?',
   '<p>Endurance leases buildings, office spaces, retail properties, and condo and coop commercial assets for owners, boards and investors. We position each property with a tailored narrative and targeted marketing to attract quality tenants. See our <a href="/services/landlord-representation/">landlord representation services</a>.</p>'),
  ('Do you handle lease renewals as well as relocations?',
   '<p>Yes, Endurance negotiates renewals, expansions and relocations. One client toured over 75 spaces across 9 months and ultimately expanded within their current building because it made the most financial sense. Another client’s relocation grew their footprint from 11,000 SF to over 38,000 SF.</p>'),
 ]),
 ('Pricing', [
  ('How much does it cost to hire Endurance?',
   f'<p>{ph("CONFIRM: fee structure for tenant and landlord assignments, for example whether tenant-rep fees are paid by the landlord")} Endurance explains how its compensation works before any engagement begins. Call {BIZ["phone"]} to discuss your situation.</p>'),
 ]),
 ('Process and timing', [
  ('When should I start looking for new office space?',
   '<p>Start looking 6 to 18 months before your current lease expires. This allows ample time for due diligence, market research and negotiation without pressure.</p>'),
  ('How long does it take to find and lease commercial space?',
   f'<p>{ph("CONFIRM: typical timeline from first meeting to signed lease")} Timing depends on your requirements and the market. For example, one Endurance client toured over 75 spaces across 9 months before signing the lease that made the most financial sense.</p>'),
  ('What happens to my lease if my landlord is in financial trouble?',
   '<p>Landlord distress can give tenants negotiating leverage, such as lower rent, abatements or better renewal terms, but it also brings risks like reduced services and ownership uncertainty. Endurance researches ownership finances, loan performance and debt maturity before negotiating, and helps tenants secure protections such as an SNDA. Read <a href="/insights/lessons-from-a-landlords-troubles/">lessons from a landlord’s troubles</a>.</p>'),
  ('What lease protections should a commercial tenant negotiate?',
   '<p>Commercial tenants in NYC should negotiate a self-help clause, an SNDA and security protections in case of an ownership change. A self-help clause lets you fix certain landlord failures and recover the cost, while an SNDA protects your lease if the lender forecloses. Always have a qualified real estate attorney review your lease.</p>'),
  ('Is my information kept confidential?',
   '<p>Yes. Confidentiality is built into the Endurance process, and your information is always protected throughout the negotiation.</p>'),
 ]),
 ('Experience and service area', [
  ('What areas does Endurance serve?',
   f'<p>Endurance serves tenants and landlords across New York City from its office at 136 Madison Avenue in Manhattan. Recent work includes the Financial District, where Tribeca Prep leased 12,900+ SF at 116 Nassau Street. {ph("CONFIRM: other boroughs or markets served")}</p>'),
  ('How experienced is the Endurance team?',
   '<p>Endurance has 30+ years of experience representing landlords and tenants across NYC, more than 1,850 successful leasing transactions, and $3B in aggregate leasing transaction volume. The team is led by Founder and Principal Gregory Gang. <a href="/about/#team">Meet the team</a>.</p>'),
  ('Is Endurance a licensed real estate brokerage?',
   f'<p>{ph("CONFIRM: New York State real estate broker license details")}</p>'),
 ]),
 ('Getting started', [
  ('How do I get started with Endurance?',
   f'<p>Call <a href="tel:{BIZ["tel"]}">{BIZ["phone"]}</a>, email <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a>, or send a message through our <a href="/contact/">contact form</a>. We will discuss your goals, whether you are a tenant or a landlord, and outline next steps.</p>'),
 ]),
]
