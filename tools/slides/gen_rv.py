import os, pathlib
OUT = pathlib.Path(__file__).resolve().parent/'html-rv'; OUT.mkdir(exist_ok=True)

# Matches the RV template pulled from the existing video: white slide, dark green
# headings, letterspaced green eyebrow, footer rail, and the right 27% kept empty
# for the presenter so nothing is ever covered.
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1920px;height:1080px;font-family:'Segoe UI',Arial,sans-serif;background:#fff;overflow:hidden}
.slide{width:1920px;height:1080px;position:relative;background:#fff;padding:96px 640px 0 120px}
/* the right 640px is reserved for the presenter card, so nothing is ever covered */
.stage{width:100%}
.kick{font-size:27px;font-weight:800;letter-spacing:6px;text-transform:uppercase;color:#15944B;margin-bottom:18px}
h1{font-size:78px;color:#0c3b22;font-weight:800;letter-spacing:-1.5px;line-height:1.04}
h1 em{color:#15944B;font-style:normal}
.lede{font-size:34px;color:#5d6878;margin-top:24px;line-height:1.35}
.rows{margin-top:56px}
.row{display:flex;gap:30px;align-items:flex-start;margin-bottom:38px}
.ic{width:78px;height:78px;border-radius:50%;background:#15944B;flex:none;display:flex;
  align-items:center;justify-content:center;color:#fff;font-size:34px;font-weight:800}
.row .t{font-size:37px;font-weight:800;color:#0c3b22;line-height:1.2}
.row .d{font-size:29px;color:#5d6878;margin-top:8px;line-height:1.35}
table{width:100%;border-collapse:collapse;margin-top:52px;font-size:34px}
th{background:#14532d;color:#fff;text-align:left;padding:26px 30px;font-size:31px}
th:last-child,td:last-child{text-align:right}
td{padding:26px 30px;color:#0c3b22;font-weight:700;border-bottom:2px solid #eef2f6}
tr:nth-child(even) td{background:#f7faf8}
td.fee{color:#15944B;font-weight:800}
.note{font-size:27px;color:#5d6878;margin-top:26px;line-height:1.4}
.grid{display:flex;flex-wrap:wrap;gap:26px;margin-top:50px}
.tile{flex:0 0 calc((100% - 52px)/3);min-width:0;background:#f4f8f5;border-radius:18px;padding:30px 28px}  /* exactly three across the 1160px text column */
.tile > b{display:block;font-size:31px;color:#0c3b22;margin-bottom:10px}
.tile span{font-size:26px;color:#5d6878;line-height:1.3}
.flag{margin-top:46px;background:#fff5d6;border-left:12px solid #e0b23c;border-radius:14px;
  padding:32px 38px;font-size:32px;color:#1b2330;line-height:1.35}
.foot{position:absolute;bottom:52px;left:120px;right:640px;display:flex;
  font-size:24px;color:#9aa5b1;font-weight:700}
.title-slide{background:linear-gradient(135deg,#0c3b22 0%,#14532d 60%,#15944B 100%)}
.title-slide h1,.title-slide .kick{color:#fff}
.title-slide .kick{color:#9ae6b4}
.title-slide .lede{color:#cfe8d9}
.big{font-size:132px;font-weight:800;color:#15944B;line-height:1}
"""
def page(body, foot, cls=""):
    return (f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
            f"<div class='slide {cls}'><div class='stage'>{body}</div>"
            # The section label used to sit at the right end of this rail, which
            # is exactly where the presenter stands — she covered words like
            # "The Addendum". Only the company name is kept, at the far left
            # and well clear of her. `foot` stays in the signature so each
            # slide still records which section it belongs to.
            f"<div class='foot'><span>Tenant Property Protection</span></div>"
            f"</div></body></html>")

S=[]
def add(n, body, foot, cls=""): S.append((n, page(body, foot, cls)))

add('01-title', """<div class='kick'>Manager &amp; CSR Certification Training</div>
<h1>RV Park &lsquo;n&rsquo; Protect</h1>
<div class='lede' style='font-size:44px;margin-top:20px'>Managers Onboarding to Success</div>
<div class='lede'>What the program is, what it covers, how to present it, and how to guide a tenant through a claim.</div>""",
"Welcome", "title-slide")

add('02-why', """<div class='kick'>Why it exists</div>
<h1>Two things collided</h1>
<div class='grid'>
 <div class='tile'><b>Driven ~42 days a year</b><span>These vehicles sit in your spaces the rest of the year.</span></div>
 <div class='tile'><b>54%+ drop coverage</b><span>More than half of veteran owners drop collision and comprehensive for the off season.</span></div>
 <div class='tile'><b>Inexperienced drivers</b><span>Large vehicles, tight turns, and on-site manoeuvring do the rest.</span></div>
</div>
<div class='flag'>A minor on-site bump then comes straight out of the tenant&rsquo;s pocket. <b>That is the moment this plan exists for.</b></div>""",
"Why It Exists")

add('03-covers', """<div class='kick'>What the program covers</div>
<h1>Whatever is in the space</h1>
<div class='lede'>RVs, campers, trailers, boats, cars and trucks &mdash; indoors or out, covered or uncovered.</div>
<div class='grid'>
 <div class='tile'><b>Contents travel</b><span><b>Half the plan limit</b>, covered <b>on-site and off-site</b> &mdash; even on a weekend away.</span></div>
 <div class='tile'><b>Second vehicle</b><span>A car left in the space while the RV is out is covered. List it on the addendum.</span></div>
 <div class='tile'><b>Deductible reimbursement</b><span>The plan effectively covers a tenant&rsquo;s auto deductible.</span></div>
</div>""",
"Coverage")

add('04-pricing', """<div class='kick'>Example plan options</div>
<h1>Sample coverage &amp; pricing</h1>
<table>
<tr><th>Protection Limit</th><th>Contents</th><th>Vehicle Parts</th><th>Monthly Fee</th></tr>
<tr><td>$1,000</td><td style='font-weight:400;color:#5d6878'>$500</td><td style='font-weight:400;color:#5d6878'>$500</td><td class='fee'>$12.00</td></tr>
<tr><td>$1,500</td><td style='font-weight:400;color:#5d6878'>$750</td><td style='font-weight:400;color:#5d6878'>$750</td><td class='fee'>$15.00</td></tr>
<tr><td>$2,500</td><td style='font-weight:400;color:#5d6878'>$1,250</td><td style='font-weight:400;color:#5d6878'>$1,250</td><td class='fee'>$25.00</td></tr>
</table>
<div class='note'>Contents and vehicle parts coverage are each <b>half the protection limit</b>, and both apply
<b>on-site and off-site</b>. Coverage levels and pricing are flexible &mdash; we can accommodate most customer needs and
requests. Billed with the rent, and the plan ends automatically when the tenant moves out.</div>""",
"Plans &amp; Pricing")

add('05-present', """<div class='kick'>Lead with these</div>
<h1>Ask <em>which</em>, not <em>whether</em></h1>
<div class='rows'>
 <div class='row'><div class='ic'>1</div><div><div class='t'>&ldquo;Which level of protection would you like?&rdquo;</div>
   <div class='d'>&ldquo;Would you like a protection plan?&rdquo; invites a no. This moves the conversation forward.</div></div></div>
 <div class='row'><div class='ic'>2</div><div><div class='t'>Look at what they are actually parking</div>
   <div class='d'>A fishing boat and a forty-foot motorhome are two very different conversations.</div></div></div>
 <div class='row'><div class='ic'>3</div><div><div class='t'>$12 a month vs a $1,000 deductible</div>
   <div class='d'>The plan effectively pays their auto deductible for them. That is the whole pitch.</div></div></div>
</div>""",
"Presenting")

add('06-covered', """<div class='kick'>Know this cold</div>
<h1>Comprehensive protection</h1>
<div class='grid'>
 <div class='tile'><b>Dings &amp; dents</b><span>On-site accidental damage and collision</span></div>
 <div class='tile'><b>Fire &amp; explosion</b><span>Including smoke damage</span></div>
 <div class='tile'><b>Burglary damage</b><span>Police report required</span></div>
 <div class='tile'><b>Vandalism</b></div>
 <div class='tile'><b>Building collapse</b></div>
 <div class='tile'><b>Contents theft</b><span>On-site and off-site, half the plan limit</span></div>
 <div class='tile'><b>Stolen attached parts</b><span>The part itself, up to the plan sublimit &mdash; not the labor to install it</span></div>
 <div class='tile'><b>Deductible reimbursement</b><span>Covers the tenant&rsquo;s auto deductible</span></div>
</div>""",
"Coverage")

add('07-not-covered', """<div class='kick'>Know these cold</div>
<h1>What is <em>not</em> covered</h1>
<div class='rows'>
 <div class='row'><div class='ic'>&times;</div><div><div class='t'>Rodent and critter damage</div>
   <div class='d'>These vehicles sit outdoors in non-climate-controlled spaces &mdash; a deliberate exclusion.</div></div></div>
 <div class='row'><div class='ic'>&times;</div><div><div class='t'>Flood</div>
   <div class='d'>Available only through the National Flood Insurance Program.</div></div></div>
 <div class='row'><div class='ic'>&times;</div><div><div class='t'>Mysterious disappearance &amp; mold</div></div></div>
</div>
<div class='flag'>Fire and explosion are covered &mdash; but <b>wildfires are specifically excluded.</b> Know that line before fire season.</div>""",
"Exclusions")

add('08-burglary', """<div class='kick'>Important and required</div>
<h1>Burglary claims</h1>
<div class='flag' style='margin-top:30px'><b>No burglary claim is paid without a police report.</b></div>
<div class='rows'>
 <div class='row'><div class='ic'>1</div><div><div class='t'>The tenant contacts the police</div>
   <div class='d'>And provides a copy of the report.</div></div></div>
 <div class='row'><div class='ic'>2</div><div><div class='t'>Photos of visible forced entry</div>
   <div class='d'>From several angles.</div></div></div>
 <div class='row'><div class='ic'>3</div><div><div class='t'>You, the manager, file the incident report</div></div></div>
</div>""",
"Burglary")

add('09-file-claim', """<div class='kick'>Filing a claim</div>
<h1>30 days from <em>discovery</em></h1>
<div class='lede'>All claims are filed online at <b>rvparknprotectclaims.com</b> &mdash; any hour of any day.</div>
<div class='rows'>
 <div class='row'><div class='ic'>1</div><div><div class='t'>The tenant files and submits their own claim</div>
   <div class='d'>Gathering their own receipts, photos and repair quotes.</div></div></div>
 <div class='row'><div class='ic'>2</div><div><div class='t'>You provide the incident report</div>
   <div class='d'>Plus supporting paperwork from the facility.</div></div></div>
 <div class='row'><div class='ic'>3</div><div><div class='t'>Start quotes right away</div>
   <div class='d'>They must arrive before the 30-day window closes.</div></div></div>
</div>""",
"Filing a Claim")

add('10-claims-team', """<div class='kick'>Filing a claim</div>
<h1>Our claims team</h1>
<div class='rows'>
 <div class='row'><div class='ic'>&#9679;</div><div><div class='t'>rvparknprotectclaims.com</div>
   <div class='d'>File a claim online any hour of any day.</div></div></div>
 <div class='row'><div class='ic'>&#9679;</div><div><div class='t'>Live adjusters</div>
   <div class='d'>Monday&ndash;Friday, <b>7:00 AM &ndash; 5:00 PM Arizona time</b>.</div></div></div>
 <div class='row'><div class='ic'>&#9679;</div><div><div class='t'>Processing can take up to 30 days</div>
   <div class='d'>Many claims are completed sooner. <b>Never promise a payment date.</b></div></div></div>
</div>""",
"Claims Team")

add('11-communication', """<div class='kick'>Claim communication</div>
<h1>Use the <em>claims portal</em></h1>
<div class='rows'>
 <div class='row'><div class='ic'>&#9679;</div><div><div class='t'>The portal is the preferred workflow</div>
   <div class='d'>Everything you put there lands directly in the claim file, where the adjuster sees it.</div></div></div>
 <div class='row'><div class='ic'>&#9679;</div><div><div class='t'>Only the filing confirmation is automated</div>
   <div class='d'>Further updates are sent by the adjuster as the claim needs them.</div></div></div>
 <div class='row'><div class='ic'>&#9679;</div><div><div class='t'>Check status any time</div>
   <div class='d'>Users with portal access can monitor a claim directly in the portal.</div></div></div>
</div>
<div class='flag'>Do not tell a tenant they will receive automatic notifications at every stage &mdash; they will not.</div>""",
"Claim Communication")

add('12-portal-access', """<div class='kick'>Manager claims portal</div>
<h1>How portal access<br>is set up</h1>
<div class='lede'>Access is structured around your <b>portfolio setup</b>, your <b>management structure</b>,
third-party management relationships, client preference and some system limitations.</div>
<div class='flag'>Some organizations have a <b>single login covering several locations</b>; others are split
differently. It is not one login per location. If you are not sure how yours is configured, ask Teon.</div>""",
"Manager Portal")

add('13-optout', """<div class='kick'>The tenant opt-out process</div>
<h1>Tenants have <em>10 business days</em><br>from move-in</h1>
<div class='rows'>
 <div class='row'><div class='ic'>1</div><div><div class='t'>Submit at myownpolicy.com</div>
   <div class='d'>Or email <b>support@myownpolicy.com</b> if the upload will not work.</div></div></div>
 <div class='row'><div class='ic'>2</div><div><div class='t'>Attach a photo of the declaration page</div>
   <div class='d'>One readable image showing all four required details.</div></div></div>
 <div class='row'><div class='ic'>3</div><div><div class='t'>Our team reviews Monday&ndash;Friday</div>
   <div class='d'>Once verified, the policy is added to the tenant&rsquo;s account.</div></div></div>
</div>
<div class='flag'>If 10 business days pass with no verified policy, the tenant is <b>automatically enrolled</b> in the protection plan.</div>""",
"Opt-Out")

add('14-three-details', """<div class='kick'>The photo must show all four</div>
<h1>What we verify on the<br>declaration page</h1>
<div class='grid'>
 <div class='tile' style='flex:0 0 calc((100% - 78px)/4)'><b>The Insurance Carrier</b><span>Name as it appears on the policy</span></div>
 <div class='tile' style='flex:0 0 calc((100% - 78px)/4)'><b>The Policy Number</b></div>
 <div class='tile' style='flex:0 0 calc((100% - 78px)/4)'><b>The Expiration Date</b></div>
 <div class='tile' style='flex:0 0 calc((100% - 78px)/4)'><b>The Tenant on the Lease</b><span>The name on the policy must match</span></div>
</div>
<div class='flag'>If any one of the four is missing, cut off or unreadable, the policy <b>cannot be added</b>
and the opt-out <b>does not go through</b>. The declaration page normally shows all of it in one shot.</div>""",
"Opt-Out")

add('15-expiry', """<div class='kick'>Before a policy lapses</div>
<h1>The <em>10-day</em><br>expiration notice</h1>
<div class='lede'>When a tenant&rsquo;s own policy is about to run out, we email them an expiration notice
from <b>myownpolicy.com</b> &mdash; <b>10 days before the policy expires</b>.</div>
<div class='rows'>
 <div class='row'><div class='ic'>&#9679;</div><div><div class='t'>Their cue to send a renewed declaration page</div></div></div>
 <div class='row'><div class='ic'>&#9679;</div><div><div class='t'>Catches a lapse before it happens</div>
   <div class='d'>No more reviewing insurance records by hand.</div></div></div>
</div>""",
"Opt-Out")

add('16-billing', """<div class='kick'>Opting out later</div>
<h1>A tenant can opt out<br><em>at any time</em></h1>
<div class='lede'>The 10 business days is the window for avoiding enrollment in the first place &mdash; not a
cut-off after which they are stuck on the plan.</div>
<div class='flag'><b>We do not pro-rate.</b> If a tenant moves out on the 20th the coverage amount is still
charged &mdash; whether they stay one day or all month, and there is no partial refund. Say this plainly at the counter.</div>""",
"Opt-Out")

add('17-exclusion', """<div class='kick'>Before launch</div>
<h1>The exclusion list</h1>
<div class='lede'>Some units should never receive an opt-out notice at all:</div>
<div class='grid'>
 <div class='tile' style='width:400px'><b>Grandfathered tenants</b></div>
 <div class='tile' style='width:400px'><b>Company units</b></div>
 <div class='tile' style='width:400px'><b>Charity units</b></div>
</div>
<div class='flag'>Once a tenant is on the list: <b>no notice, no 10-day clock, no automatic enrollment.</b>
Send your list to Teon Delacruz before launch.</div>""",
"Opt-Out")

add('18-contact', """<div class='kick'>You&rsquo;ve got questions? We&rsquo;ve got answers</div>
<h1>Teon Delacruz</h1>
<div class='lede' style='margin-top:14px'>Client Success Manager</div>
<div class='rows'>
 <div class='row'><div class='ic'>&#9993;</div><div><div class='t'>tdelacruz@tenantpropertyprotection.com</div></div></div>
 <div class='row'><div class='ic'>&#9742;</div><div><div class='t'>623-215-0691</div>
   <div class='d'>Monday&ndash;Friday, 7:00 AM &ndash; 5:30 PM Arizona time</div></div></div>
</div>
<div class='note' style='margin-top:20px'>Training support is always free, and there is no limit on it.</div>""",
"Support")

add('19-addendum', """<div class='kick'>What the tenant signs</div>
<h1>The RV Park &lsquo;n&rsquo; Protect addendum</h1>
<div class='lede'>One page. It records the space, the vehicles in it, and the level of protection chosen.</div>
<div class='rows'>
 <div class='row'><div class='ic'>1</div><div><div class='t'>The protection limit they chose</div>
   <div class='d'>$1,000, $1,500 or $2,500 &mdash; initialled on that line.</div></div></div>
 <div class='row'><div class='ic'>2</div><div><div class='t'>Every vehicle and licence plate in the space</div>
   <div class='d'>Written on the addendum. This is what a claim is validated against.</div></div></div>
 <div class='row'><div class='ic'>3</div><div><div class='t'>Their signature</div>
   <div class='d'>Proof the plan was offered. Retained with the lease either way.</div></div></div>
</div>
<div class='flag'>Burglary still needs visible signs of forced entry and a police report.</div>""",
"The Addendum")

add('20-addendum-sublimits', """<div class='kick'>The two numbers tenants ask about</div>
<h1>Contents and vehicle parts &mdash; <em>half</em> the limit</h1>
<table>
<tr><th>Protection Limit</th><th>Contents Coverage</th><th>Vehicle Parts Coverage</th></tr>
<tr><td>$1,000</td><td class='fee'>$500</td><td class='fee'>$500</td></tr>
<tr><td>$1,500</td><td class='fee'>$750</td><td class='fee'>$750</td></tr>
<tr><td>$2,500</td><td class='fee'>$1,250</td><td class='fee'>$1,250</td></tr>
</table>
<div class='rows' style='margin-top:34px'>
 <div class='row'><div class='ic'>&#10003;</div><div><div class='t'>Contents are covered off-site too</div>
   <div class='d'>Stolen items from inside the stored property &mdash; on your lot or away from it.</div></div></div>
 <div class='row'><div class='ic'>&#10003;</div><div><div class='t'>So are stolen vehicle parts</div>
   <div class='d'>Replacement up to the parts sublimit, on-site and off-site.</div></div></div>
</div>""",
"The Addendum")

for n,h in S: (OUT/f"{n}.html").write_text(h, encoding='utf-8')
print("wrote", len(S), "RV slides")
