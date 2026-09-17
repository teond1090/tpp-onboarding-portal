import os, json, base64, pathlib
M=os.path.join(os.path.dirname(os.path.abspath(__file__)),'media')
def b64(f):
    p=os.path.join(M,f); ext=f.split('.')[-1].lower()
    mt='image/jpeg' if ext in('jpg','jpeg') else 'image/png'
    return f"data:{mt};base64,"+base64.b64encode(open(p,'rb').read()).decode()

LOGO=b64('image3.png'); AWARD=b64('image6.jpg'); UNITS=b64('image7.png')
COUCH=b64('image17.png'); DEC1=b64('image18.png'); DEC2=b64('image19.png')
BIRD=b64('image23.png'); FLOOD=b64('image36.jpg'); FORCED=b64('image38.png')
PORTAL=b64('image59.png')
IC={'explosion':b64('image27.png'),'rodent':b64('image28.png'),'water':b64('image29.png'),
    'theft':b64('image30.png'),'light':b64('image31.png'),'vandal':b64('image32.png'),
    'fire':b64('image33.png'),'collapse':b64('image34.png'),'wind':b64('image35.png')}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1920px;height:1080px;font-family:'Segoe UI',Arial,sans-serif;background:#fff;overflow:hidden}
.slide{width:1920px;height:1080px;position:relative;display:flex;flex-direction:column;
  padding:70px 640px 90px 90px;background:#fff}
/* the right 640px is reserved for the presenter card, so nothing is ever covered */
.brand{position:absolute;top:44px;right:660px;height:62px}
h1{font-size:64px;color:#16233F;font-weight:800;letter-spacing:-1.5px;line-height:1.05}
h1 em{color:#B01824;font-style:normal}
.kick{font-size:26px;font-weight:800;letter-spacing:5px;text-transform:uppercase;color:#B01824;margin-bottom:20px}
.sub{font-size:34px;color:#5d6878;margin-top:26px;max-width:1250px;line-height:1.35}
ul{list-style:none;margin-top:36px;max-width:1150px}
li{font-size:31px;color:#1b2330;margin-bottom:26px;padding-left:56px;position:relative;line-height:1.3}
li:before{content:'';position:absolute;left:0;top:14px;width:26px;height:26px;border-radius:50%;background:#B01824}
li b{color:#16233F}
.cards{display:flex;gap:22px;margin-top:42px}
.card{flex:1;border:4px solid #e3e7ee;border-radius:20px;padding:30px 20px;text-align:center;background:#fafbfd}
.card.hi{border-color:#B01824;background:#fff5f5}
.card .amt{font-size:62px;font-weight:800;color:#16233F;line-height:1}
.card .per{font-size:30px;color:#B01824;font-weight:800;margin-top:10px}
.card .day{font-size:26px;color:#5d6878;margin-top:14px}
.title-slide{background:linear-gradient(135deg,#16233F 0%,#20304f 60%,#2b3d63 100%);color:#fff;
  justify-content:center;align-items:flex-start;padding-bottom:300px}
.title-slide h1{color:#fff;font-size:80px}
.title-slide .sub{color:#cdd6e6}
.icons{display:flex;flex-wrap:wrap;gap:26px;margin-top:40px;max-width:1150px}
.ic{width:172px;text-align:center}
.ic img{width:104px;height:104px;object-fit:contain}
.ic span{display:block;font-size:26px;color:#16233F;font-weight:700;margin-top:12px}
.photo{position:absolute;right:660px;top:230px;width:400px;border-radius:20px;box-shadow:0 18px 50px rgba(20,30,50,.25)}
/* A slide with a photo gives up the right of its text column to it, so the
   text wraps beside the picture instead of running underneath it. Photo
   spans 860..1260; text stops at 820. */
.slide:has(> .photo){padding-right:1100px}
.warn{margin-top:34px;background:#fff5d6;border-left:12px solid #e0b23c;border-radius:14px;
  padding:26px 32px;font-size:28px;color:#1b2330;max-width:1150px;line-height:1.35}
.big{font-size:118px;font-weight:800;color:#B01824;line-height:1}
.steps{display:flex;gap:22px;margin-top:44px;max-width:1150px}
.step{flex:1;background:#f2f5f9;border-radius:20px;padding:36px 30px}
.step .n{width:70px;height:70px;border-radius:50%;background:#16233F;color:#fff;font-size:36px;
  font-weight:800;display:flex;align-items:center;justify-content:center;margin-bottom:22px}
.step p{font-size:25px;color:#1b2330;line-height:1.3}
.three{display:flex;gap:22px;margin-top:40px;max-width:1150px}
.three div{flex:1;background:#16233F;color:#fff;border-radius:18px;padding:30px 22px;font-size:27px;
  font-weight:700;text-align:center;line-height:1.25}
"""

def page(body, cls=""):
    return f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='slide {cls}'>{body}</div></body></html>"

S=[]
def add(name, body, cls=""): S.append((name, page(body, cls)))

add('01-title', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>Manager &amp; CSR Certification</div>
<h1>TPP Secure</h1><h1 style='font-size:64px;color:#ff9ba3'>Managers Onboarding to Success</h1>
<div class='sub'>Protecting your tenants, your facility, and your bottom line.</div>""", 'title-slide')

add('02-not-insurance', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>The words you use matter</div>
<h1>It is a <em>Protection Plan</em> &mdash; not insurance</h1>
<ul><li>Per the California Supreme Court, <b>Heckard v. A-1 Self Storage</b>, protection plans are <b>not insurance</b></li>
<li>Not regulated by the Department of Insurance</li>
<li>More flexibility, your own plan limits and pricing</li>
<li><b>No insurance licensing requirements</b></li></ul>
<div class='warn'>Never call it &ldquo;insurance&rdquo; when speaking with a tenant. Say <b>protection plan</b> &mdash; every time.</div>""")

add('03-gap', f"""<img class='brand' src='{LOGO}'>
<img class='photo' src='{UNITS}'>
<div class='kick'>Why TPP Secure exists</div>
<h1>Most tenants are not<br>as covered as they think</h1>
<div class='big'>67%</div>
<div class='sub' style='margin-top:10px'>of self-storage tenants have <b>no homeowners policy at all</b></div>
<ul style='margin-top:34px'><li>Many policies cap off-premises property at <b>10&ndash;50%</b> of the contents limit</li>
<li>Some exclude stored property <b>outright</b></li></ul>""")

add('04-fmv', f"""<img class='brand' src='{LOGO}'>
<img class='photo' src='{COUCH}'>
<div class='kick'>How claims are valued</div>
<h1>Claims are paid at<br><em>Replacement Cost</em></h1>
<div class='sub'>The same year, make and model &mdash; what it costs to replace the item like for like, today.</div>
<div class='warn'><b>Not the same as Full Replacement Cost.</b> Full Replacement Cost would mean a brand-new
item of similar quality regardless of how old the lost one was &mdash; that is a different concept, and not
how these claims are processed.</div>
<ul style='margin-top:34px'><li>Filing a claim <b>never affects a homeowners premium</b></li></ul>""")

add('05-rates', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>Coverage &amp; rates</div>
<h1>Three plan options</h1>
<div class='cards'>
  <div class='card'><div class='amt'>$2,000</div><div class='per'>$12 / month</div><div class='day'>about 40&cent; a day</div></div>
  <div class='card hi'><div class='amt'>$3,000</div><div class='per'>$15 / month</div><div class='day'>about 50&cent; a day</div></div>
  <div class='card'><div class='amt'>$5,000</div><div class='per'>$25 / month</div><div class='day'>about 83&cent; a day</div></div>
</div>
<div class='sub' style='margin-top:40px'>Example levels only &mdash; <b>rates are set for your facility</b>,
and <b>higher limits are available on request</b>.</div>""")

add('06-present', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>How to present it</div>
<h1>Ask <em>what they need</em>,<br>not <em>whether they want it</em></h1>
<div class='three'>
  <div>&ldquo;Would you like a protection plan?&rdquo;<br><span style='color:#ff9ba3;font-size:28px'>invites a NO</span></div>
  <div style='background:#B01824'>&ldquo;What level of coverage do your contents need?&rdquo;<br><span style='font-size:28px'>moves the conversation forward</span></div>
</div>
<ul style='margin-top:46px'><li>Name the <b>middle plan first</b> &mdash; room to move either direction</li>
<li>Frame it <b>daily</b>: nobody argues about 50&cent; a day</li>
<li>Get the <b>addendum signed at the time of rental</b> &mdash; every tenant, every time</li></ul>""")

add('07-birdseye', f"""<img class='brand' src='{LOGO}'>
<img class='photo' src='{BIRD}'>
<div class='kick'>Plans over $5,000</div>
<h1>BirdsEye Protection App</h1>
<div class='sub'>A short application with an <b>inventory list and photos</b>, so underwriters
have a baseline before anything ever happens.</div>
<ul><li>Required for <b>protection plans over $5,000</b> &mdash; the $5,000 plan itself does not need one</li>
<li>Takes only a few minutes at the counter</li></ul>""")

add('08-covered', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>What TPP Secure covers</div>
<h1>Covered perils</h1>
<div class='icons'>
  <div class='ic'><img src='{IC['fire']}'><span>Fire &amp; Smoke</span></div>
  <div class='ic'><img src='{IC['explosion']}'><span>Explosion</span></div>
  <div class='ic'><img src='{IC['theft']}'><span>Burglary</span></div>
  <div class='ic'><img src='{IC['vandal']}'><span>Vandalism</span></div>
  <div class='ic'><img src='{IC['water']}'><span>Water Damage<br>(from plumbing)</span></div>
  <div class='ic'><img src='{IC['wind']}'><span>Windstorm</span></div>
  <div class='ic'><img src='{IC['collapse']}'><span>Building Collapse</span></div>
  <div class='ic'><img src='{IC['rodent']}'><span>Rodent Damage<br>($500 sublimit)</span></div>
</div>""")

add('09-not-covered', f"""<img class='brand' src='{LOGO}'>
<img class='photo' src='{FLOOD}'>
<div class='kick'>Know these cold</div>
<h1>What is <em>not</em> covered</h1>
<ul style='margin-top:40px'>
<li><b>Flood</b> &mdash; only available through the National Flood Insurance Program (NFIP)</li>
<li><b>Mysterious disappearance</b> &mdash; items that go missing with no evidence of forced entry</li>
<li><b>Mold</b></li></ul>
<div class='warn'>Rodent damage <b>is</b> covered &mdash; but capped at a <b>$500 sublimit</b>.</div>""")

add('10-burglary', f"""<img class='brand' src='{LOGO}'>
<img class='photo' src='{FORCED}'>
<div class='kick'>Important and required</div>
<h1>Burglary claims</h1>
<div class='warn' style='margin-top:20px'><b>No burglary claim is paid without a police report.</b></div>
<ul style='margin-top:34px'>
<li><b>The tenant</b> contacts the police and provides a copy of the report</li>
<li>Photos of <b>visible signs of forced entry</b>, from several angles</li>
<li><b>You, the manager,</b> provide your incident report</li></ul>""")

add('11-decpage', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>Reading a declaration page</div>
<h1>Check the <em>off-premises</em> line</h1>
<div style='display:flex;gap:34px;margin-top:30px'>
  <div style='flex:1'><img src='{DEC1}' style='width:100%;border:3px solid #e3e7ee;border-radius:14px'>
    <div style='font-size:26px;color:#B01824;font-weight:800;margin-top:14px'>Does NOT include off-premises coverage</div></div>
  <div style='flex:1'><img src='{DEC2}' style='width:100%;border:3px solid #e3e7ee;border-radius:14px'>
    <div style='font-size:26px;color:#B01824;font-weight:800;margin-top:14px'>Includes other structures, but at reduced liability</div></div>
</div>
<div class='sub' style='margin-top:30px;font-size:30px'>If you spot that exclusion, <b>tell the tenant</b> &mdash; their belongings may not be covered at all.</div>""")

add('12-file-claim', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>Filing a claim</div>
<h1>30 days from <em>discovery</em></h1>
<div class='steps'>
  <div class='step'><div class='n'>1</div><p><b>The tenant</b> files online at <b>tppclaims.com</b> &mdash; any hour, any day</p></div>
  <div class='step'><div class='n'>2</div><p><b>The tenant</b> gathers their own receipts, photos and documentation and submits the claim</p></div>
  <div class='step'><div class='n'>3</div><p><b>You, the manager,</b> provide the incident report and supporting paperwork</p></div>
</div>
<div class='warn'>Tell tenants not to move or discard anything until documentation is complete. <b>Photos first, cleanup second.</b></div>""")

add('13-claims-comm', f"""<img class='brand' src='{LOGO}'>
<img class='photo' src='{PORTAL}'>
<div class='kick'>Claims communication</div>
<h1>Use the <em>claims portal</em></h1>
<ul style='margin-top:36px'>
<li>The claims portal is the <b>preferred workflow</b> &mdash; entries land directly in the claim file</li>
<li>Only the <b>initial filing confirmation is automated</b>. Further updates come from the adjuster as needed</li>
<li>With portal access, you can <b>monitor claim status</b> any time</li>
<li>Portal access is structured by <b>portfolio setup and management structure</b> &mdash; not one login per location</li></ul>""")

add('14-claims-timing', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>Setting expectations</div>
<h1>Claims timing</h1>
<div class='cards'>
  <div class='card hi'><div class='amt' style='font-size:66px'>Up to 30 days</div><div class='day' style='font-size:28px;margin-top:18px'>Processing time &mdash; many claims are completed sooner</div></div>
  <div class='card'><div class='amt' style='font-size:66px'>7AM &ndash; 5PM</div><div class='day' style='font-size:28px;margin-top:18px'>Live adjusters, Monday&ndash;Friday, Arizona time</div></div>
</div>
<div class='warn'><b>Never promise a payment date, and never estimate a reimbursement amount.</b><br>
&ldquo;I&rsquo;m not the right person to put a number on that, but the adjuster will walk you through it.&rdquo;</div>""")

add('15-optout', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>The tenant opt-out process</div>
<h1>Tenants have <em>10 business days</em> from move-in</h1>
<div class='steps'>
  <div class='step'><div class='n'>1</div><p>Tenant submits at <b>myownpolicy.com</b> &mdash; or emails <b>support@myownpolicy.com</b></p></div>
  <div class='step'><div class='n'>2</div><p>Tenant attaches a <b>photo of their declaration page</b></p></div>
  <div class='step'><div class='n'>3</div><p>Our team reviews <b>Monday&ndash;Friday</b> and adds the verified policy</p></div>
</div>
<div class='warn'>If 10 business days pass with no verified policy, the tenant is <b>automatically enrolled</b> in the protection plan.</div>""")

add('16-three-details', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>The photo must show all four</div>
<h1>What we verify on the<br>declaration page</h1>
<div class='three'>
  <div>The <b>Insurance Carrier</b><br><span style='font-size:26px;color:#cdd6e6'>name as it appears on the policy</span></div>
  <div>The <b>Policy Number</b></div>
  <div>The <b>Expiration Date</b></div>
  <div>The <b>Tenant on the Lease</b><br><span style='font-size:26px;color:#cdd6e6'>the name on the policy must match</span></div>
</div>
<div class='warn'>If any one of the four is missing, cut off or unreadable, the policy <b>cannot be added</b>
and the opt-out <b>does not go through</b>.</div>""")

add('17-expiry', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>Before a policy lapses</div>
<h1>The <em>10-day</em> expiration notice</h1>
<div class='sub'>When a tenant&rsquo;s own policy is about to run out, we email them an expiration
notice from <b>myownpolicy.com</b> &mdash; <b>10 days before the policy expires</b>.</div>
<ul style='margin-top:40px'>
<li>That is the tenant&rsquo;s cue to send a <b>renewed declaration page</b></li>
<li>Catches a lapse <b>before</b> it happens</li>
<li>No more reviewing insurance records by hand</li></ul>""")

add('18-exclusion', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>Before launch</div>
<h1>The exclusion list</h1>
<div class='sub'>Some units should never receive an opt-out notice at all:</div>
<ul style='margin-top:36px'>
<li>Tenants who have been <b>grandfathered in</b></li>
<li><b>Company units</b></li>
<li><b>Charity units</b></li></ul>
<div class='warn'>Once a tenant is on the list: <b>no notice, no 10-day clock, no automatic enrollment.</b>
Send your list to Teon Delacruz before launch.</div>""")

add('19-billing', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>Opting out later</div>
<h1>A tenant can opt out<br><em>at any time</em></h1>
<div class='sub'>The 10 business days is the window for avoiding enrollment in the first place &mdash;
it is not a cut-off after which they are stuck on the plan.</div>
<div class='warn' style='margin-top:44px'><b>We do not pro-rate.</b> If a tenant moves out on the 20th, the
coverage amount is still charged &mdash; whether they stay one day or all month, and there is no partial refund.
Say this plainly at the counter.</div>""")

add('20-contact', f"""<img class='brand' src='{LOGO}'>
<img class='photo' src='{AWARD}' style='top:260px;box-shadow:none'>
<div class='kick'>You&rsquo;ve got questions? We&rsquo;ve got answers</div>
<h1>Teon Delacruz</h1>
<div class='sub' style='margin-top:12px'>Client Success Manager</div>
<ul style='margin-top:40px'>
<li>tdelacruz@tenantpropertyprotection.com</li>
<li>Direct: 623-215-0691</li>
<li>Monday&ndash;Friday, 7:00 AM &ndash; 5:30 PM Arizona time</li></ul>
<div class='sub' style='font-size:28px;margin-top:30px'>Training support is always free, and there is no limit on it.</div>""")

add('21-addendum', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>What the tenant signs</div>
<h1>The Tenant Responsibility Addendum</h1>
<div class='sub'>One page that does three jobs &mdash; and the signature is the one that protects you.</div>
<div class='steps'>
  <div class='step'><div class='n'>1</div><p><b>Records the level they chose</b><br>$2,000 at $12, $3,000 at $15,
    or $5,000 at $25 a month &mdash; initialled on that line</p></div>
  <div class='step'><div class='n'>2</div><p><b>Lists what the plan covers</b><br>Printed on the page the tenant
    is signing, so there is no argument later</p></div>
  <div class='step'><div class='n'>3</div><p><b>Proves it was offered</b><br>Signed whether they take the plan or
    show their own policy. Retained with the lease</p></div>
</div>
<div class='warn'>&ldquo;Nobody ever offered me that.&rdquo; The signed addendum in the file is the answer.</div>""")

add('22-addendum-detail', f"""<img class='brand' src='{LOGO}'>
<div class='kick'>Two details to know by heart</div>
<h1>Burglary, water &mdash; and the inventory</h1>
<ul>
<li><b>Burglary</b> must show <b>visible signs of forced entry</b> and be reported to the police and to you.
    A <b>disc or cylinder lock waives the burglary deductible</b> &mdash; worth saying when a tenant buys a lock.</li>
<li><b>Water damage does not include flood or surface water.</b> That is the National Flood Program, not this plan.</li>
<li><b>The inventory is the tenant&rsquo;s responsibility.</b> They keep the list, the photos and the receipts &mdash;
    that is what establishes a baseline if they ever claim.</li>
</ul>
<div class='warn'>Rodent damage is covered on this addendum too &mdash; up to a $500 sublimit.</div>""")

out=pathlib.Path(os.path.dirname(os.path.abspath(__file__)))/'html-secure'; out.mkdir(exist_ok=True)
for n,h in S: (out/f"{n}.html").write_text(h, encoding='utf-8')
print("wrote", len(S), "slides")

