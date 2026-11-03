#!/usr/bin/env python3
"""Build the al-folio-inspired static site using only Python's standard library."""
import html
import json
import re
import shutil
import argparse
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
DATA = json.loads((ROOT / 'content/site.json').read_text())
ESC = html.escape
SCHOLAR = 'https://scholar.google.com/citations?user=WSDsPtMAAAAJ&hl=en'

ICONS = {
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
    'scholar': '<path d="m2 9 10-6 10 6-10 6-10-6Zm4 3v6c4 3 8 3 12 0v-6m4-3v9"/>',
    'github': '<path d="M9 19c-4 1-4-2-6-2m12 5v-4c0-1 .1-1.8-.5-2.5 3.3-.4 6.5-1.6 6.5-7A5.5 5.5 0 0 0 19.5 5c.2-1 .1-2-.3-3 0 0-1.2-.4-4 1.5a14 14 0 0 0-7 0C5.4 1.6 4.2 2 4.2 2c-.4 1-.5 2-.3 3a5.5 5.5 0 0 0-1.5 3.5c0 5.4 3.2 6.6 6.5 7-.6.7-.9 1.6-.9 2.5v4"/>',
    'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
}
def icon(name):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

def link(label, url, cls=''):
    return f'<a href="{ESC(url, quote=True)}" class="{cls}">{ESC(label)}</a>'

def date_label(date):
    year, month = date.split('/')
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    return f'{months[int(month)-1]} {year}'

def page(filename, name, title, content, description=None):
    nav = [('index.html','About'),('research.html','Research'),('group.html','LMF'),('publications.html','Publications'),('talks.html','Talks'),('cv.html','CV')]
    nav_html = ''.join(f'<a href="{url}"'+(' aria-current="page"' if name == label else '')+(' target="_blank" rel="noopener"' if label == 'CV' else '')+f'>{label}</a>' for url,label in nav)
    desc = description or 'Yunshan Ma at Singapore Management University. LMF: Lab for Multimodality and Forecasting. Research across fashion, finance, cybersecurity, music, and social events.'
    markup = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{ESC(title)} | Yunshan Ma · SMU</title><meta name="description" content="{ESC(desc, quote=True)}">
<meta name="color-scheme" content="light dark"><meta property="og:type" content="website"><meta property="og:title" content="{ESC(title)} | Yunshan Ma"><meta property="og:description" content="{ESC(desc, quote=True)}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css">
<script>try{{const t=localStorage.getItem('theme');document.documentElement.dataset.theme=t||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light')}}catch(e){{}}</script>
<script defer src="assets/site.js"></script></head>
<body id="top"><a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="container header-inner"><a class="brand" href="index.html"><strong>Yunshan</strong> Ma<span aria-hidden="true">.</span></a>
<button class="menu-toggle" type="button" aria-label="Toggle navigation" aria-controls="navigation" aria-expanded="false">☰</button>
<nav class="nav" id="navigation" aria-label="Main navigation">{nav_html}</nav>
<button class="theme-toggle" type="button" aria-label="Switch color theme" aria-pressed="false">{icon('sun')}</button></div></header>
<main id="main" class="container">{content}</main>
<footer class="footer"><div class="container footer-inner"><div><p>© 2026 Yunshan Ma. Singapore Management University.</p><p class="footer-secondary">A static adaptation inspired by {link('al-folio','https://github.com/alshedivat/al-folio')}. Content updated November 2026.</p></div><a class="back-top" href="#top">Back to top ↑</a></div></footer></body></html>'''
    (OUT / filename).write_text('\n'.join(line.rstrip() for line in markup.splitlines()) + '\n')

def news(items):
    return ''.join(f'<article class="news-row"><time datetime="{item["date"].replace("/","-")}">{date_label(item["date"])}</time><div>{localize(item["html"])}</div></article>' for item in items)

def localize(value):
    return value.replace('https://mysbupt.github.io/image/', 'image/')

PAPERS = [p for p in DATA['publications'] if p['title'] != 'Yunshan Ma, Lizi Liao, Tat-Seng Chua.']
VENUES = {
 'BundleLM': ('MMM 2027',2027), 'Distilling Transitional': ('TOIS',2026),
 'FashionStylist': ('SIGIR-AP',2026), 'Personalized Context': ('CIKM',2026),
 'AnalysisBank': ('EMNLP',2026), 'Large Language Model Empowered': ('TKDE',2026),
 'FinAlogy': ('ACM MM · Demo',2026), 'CFALR': ('TOIS',2026),
 'Dynamic Spectral': ('KDD',2026), 'Promoting Long-tail': ('TOIS',2026),
 'Frozen LVLMs': ('ICMR',2026), 'MAB-DQA': ('ACL',2026),
 'Scattered Hypothesis': ('ACL · Findings',2026), 'Addressing graph': ('Neurocomputing',2026),
 'Dual-Diffusional': ('SIGIR',2026), 'iTIMO': ('SIGIR · Resource',2026),
 'MetaRAG': ('TOIS',2026), 'MM-AttacKG': ('KBS',2026),
 'Discrete Diffusion': ('ICLR',2026), 'Reasoning on Time-Series for Financial Technical': ('ICLR',2026),
 'ThinkTank-ME': ('WWW · Short',2026), 'Potent but Stealthy': ('AAAI',2026),
 'PortfolioPilot': ('AAAI · Demo¹',2025), 'Integrating Symbolic': ('MMM',2026),
 'Temporal Relational': ('ICAIF · Workshop',2025), 'Reasoning on Time-Series for Financial Analysis': ('ICAIF · Workshop',2025),
 'VibeMus': ('MMAsia · Demo',2025), 'Website Owner': ('TKDD',2025),
 'GenWardrobe': ('ACM MM · Demo',2025), 'LLM2Rec': ('KDD',2025), 'FashionDPO': ('SIGIR',2025),
}
for p in PAPERS:
    for prefix, (venue, year) in VENUES.items():
        if p['title'].startswith(prefix):
            p['venue'], p['year'] = venue, year
            break
    if p['title'].startswith('FashionDPO:Fine'):
        p['title'] = p['title'].replace('FashionDPO:Fine','FashionDPO: Fine')

def paper(p, searchable=False):
    attrs = f' data-search="{ESC((p["title"]+" "+p["authors"]+" "+p["venue"]+" "+str(p["year"])+" "+" ".join(p.get("domains",[]))).lower(), quote=True)}" data-year="{p["year"]}" data-domains="{ESC("|".join(p.get("domains",[])), quote=True)}"' if searchable else f' data-year="{p["year"]}"'
    authors = ESC(p['authors']).replace('Yunshan Ma', '<strong>Yunshan Ma</strong>')
    resources = ''.join(link(r['label'].strip('[]').replace('pdf','PDF'), localize(r['url'])) for r in p['links'])
    award = f'<p class="paper-award">{ESC(p["award"])}</p>' if p.get('award') else ''
    venue = p['venue'] if str(p['year']) in p['venue'] or re.search(r"[‘’']\d{2}",p['venue']) else f'{p["venue"]} · {p["year"]}'
    return f'<article class="pub"{attrs}><div class="venue">{ESC(venue)}</div><div><h3>{ESC(p["title"])}</h3>'+award+(f'<p class="authors">{authors}</p>' if authors else '')+(f'<div class="resources">{resources}</div>' if resources else '')+'</div></article>'

TOPICS = [
 ('multimodality','01','Multimodality','Understanding and fusing text, images, audio, graphs, and symbolic data; modeling how their elements compose and combine.', 'We study multimodal understanding and fusion, together with compositional and combinatorial modeling, across text, images, audio, graphs, and symbolic data. Our methods capture relationships both within and across modalities, with applications in bundle construction, recommender systems, and other structured decision problems.', ['Multimodal understanding and fusion','Compositional and combinatorial modeling','Bundle construction and recommender systems']),
 ('forecasting','02','Forecasting','Anticipating macro-level events and micro-level behavior, from financial markets and geopolitics to users and cyber attacks.', 'We develop forecasting methods across scales. At the macro level, we study financial forecasting and geopolitical event forecasting. At the micro level, we model user behavior in recommender systems and predict cyber attack sequences.', ['Macro-level: financial markets and geopolitical events','Micro-level: user behavior and recommendation','Micro-level: cyber attack sequence prediction'])
]

DOMAINS = [
 ('Fashion','Fashion understanding, personalized styling, outfit and wardrobe generation, and trend forecasting.', ['FashionStylist','CFALR','GenWardrobe']),
 ('Finance','Financial forecasting, explainable stock prediction, time-series reasoning, and financial analysis.', ['Learning to Generate Explainable Stock Predictions','Reasoning on Time-Series for Financial Technical','AnalysisBank']),
 ('Cybersecurity','Cyber threat intelligence, attack graph construction, and cyber attack sequence prediction.', ['AttacKG+:','MM-AttacKG','MetaRAG']),
 ('Music','Connecting symbolic music and audio with language models for music understanding and personalization.', ['Integrating Symbolic','VibeMus']),
 ('Social Events','Understanding and forecasting social and geopolitical events through graph modeling, open-ended hypothesis generation, and multi-expert reasoning.', ['Scattered Hypothesis','ThinkTank-ME','Context-aware Event Forecasting'])
]

def domain_slug(name):
    return name.lower().replace(' ', '-')

def domain_sections():
    result = '<section class="section" id="domains"><p class="eyebrow">Research by Application</p><h2>Vertical Domains</h2><p class="tagline">We apply multimodality and forecasting across Fashion, Finance, Cybersecurity, Music, and Social Events.</p></section>'
    for name, description, prefixes in DOMAINS:
        examples = [next(p for p in PAPERS if p['title'].startswith(prefix)) for prefix in prefixes]
        result += f'<section class="topic" id="{domain_slug(name)}"><span class="topic-label">{ESC(name.upper())}</span><div><h2>{ESC(name)}</h2><p>{ESC(description)}</p><ul class="domain-papers">'+''.join('<li>'+link(p['title'],f'publications.html?q={quote(p["title"])}')+'</li>' for p in examples)+'</ul>'+link(f'All {name.lower()} publications →',f'publications.html?domain={quote(name)}','text-link')+'</div></section>'
    return result

TALKS = [
 ('2026/10','LLM for Cybersecurity','NExT++ Suzhou Workshop','Ma Yunshan - LLM for Cybersecurity.pdf'),
 ('2026/07','Multimodal Open-World Event Forecasting','Invited talk · ChinaMM 2026 Forum','Open-world Event Forecasting.pdf'),
 ('2026/05','Bundle Recommendation and Generation','Invited talk · Workshop on search and recommendation','Generative_Bundle_Recommendation.pdf'),
 ('2025/09','LLM for Cybersecurity','SMU-SCIS MITB AI translational seminar & ST Engineering research workshop','LLM-Enhanced_Cyber_Threat_Intelligence_Analysis.pdf'),
 ('2025/09','Multimodal Open-World Event Forecasting','SMU-SCIS research cluster seminar','Multimodal_LLMs_for_Open-World_Forecasting.pdf'),
 ('2025/08','Bundle Recommendation and Generation','Invited talk · Workshop on generative recommendation','Multimodal_Bundle_Recommendation_and_Generation.pdf')
]

OUT.mkdir(exist_ok=True)
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
shutil.copytree(ROOT/'image',OUT/'image',dirs_exist_ok=True)
shutil.copy2(ROOT/'assets/img/profile.png',OUT/'image/profile.png')
shutil.copytree(ROOT/'licenses',OUT/'licenses',dirs_exist_ok=True)
(OUT/'.nojekyll').touch()
(OUT/'assets/img/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#8b228d"/><text x="32" y="43" text-anchor="middle" font-family="Arial,sans-serif" font-size="34" fill="white">M</text></svg>')

intro = '''<div class="hero"><div><p class="eyebrow">Singapore Management University</p><h1><strong>Yunshan</strong> Ma <span class="chinese" lang="zh">马云山</span></h1><p class="subtitle">Assistant Professor<br><a href="https://computing.smu.edu.sg/">School of Computing and Information Systems</a></p>
<div class="intro"><p>I am a tenure-track Assistant Professor at Singapore Management University. My research centers on <strong>multimodality and forecasting</strong>. I lead <a href="group.html"><strong>LMF: Lab for Multimodality and Forecasting</strong></a>, where we connect multimodal modeling with forecasting across scales.</p>
<p>Before joining SMU, I was a Postdoctoral Research Fellow at the <a href="https://www.nextcenter.org/team">NExT++ Research Center</a>, National University of Singapore, supervised by <a href="https://www.chuatatseng.com/">Prof. Tat-Seng Chua</a>. I also worked with Prof. Chang Ee-Chien and Prof. Liang Zhenkai at the <a href="https://ncl.sg/">National Cybersecurity R&amp;D Lab</a>. I received my PhD from NUS in 2022, supervised by Prof. Chua.</p>
<p>I am interested in discovering and formulating new problems, and in developing data mining, information retrieval, and multimedia methods with practical impact.</p></div>
<div class="socials">'''+link('Email','mailto:ysma@smu.edu.sg')+link('Google Scholar ↗',SCHOLAR)+link('GitHub ↗','https://github.com/mysbupt')+'''</div></div>
<aside><img class="portrait" src="assets/img/profile.png" alt="Portrait of Yunshan Ma" width="250" height="285" fetchpriority="high"><p class="profile-caption"><strong>Yunshan Ma · 马云山</strong><br>Assistant Professor, SMU<br>Singapore<br><a href="mailto:ysma@smu.edu.sg">ysma@smu.edu.sg</a></p></aside></div>'''
research_grid = '<section class="section"><div class="section-heading"><h2>Research Interests</h2>'+link('Explore research →','research.html')+'</div><div class="research-grid">'+''.join(f'<article class="research-item"><span class="number">{t[1]}</span><h3>{t[2]}</h3><p>{t[3]}</p>'+link('Read more →',f'research.html#{t[0]}','text-link')+'</article>' for t in TOPICS)+'</div><div class="domain-nav" aria-label="Research application domains">'+''.join(link(name,f'research.html#{domain_slug(name)}') for name,_,_ in DOMAINS)+'</div></section>'
latest = '<section class="section"><div class="section-heading"><h2>News</h2>'+link('All updates →','news.html')+'</div>'+news(DATA['news'][:6])+'</section>'
selected = sorted([p for p in PAPERS if p.get('selected') or p['title'].startswith('CrossCBR:')],key=lambda p:p['year'],reverse=True)
selection = '<section class="section" id="selected-publications"><div class="section-heading"><h2>Selected Publications</h2>'+link('All publications →','publications.html')+'</div>'+''.join(paper(p) for p in selected)+'</section>'

research_intro = '<div class="page-intro"><p class="eyebrow">LMF · Research</p><h1>Multimodality<br>&amp; Forecasting.</h1><p>Our research can be viewed through two complementary organizations: the fundamental technologies we develop and the vertical domains where we apply them.</p><div class="domain-nav">'+link('Fundamental Technologies','#fundamental-technologies')+link('Vertical Domains','#domains')+'</div></div>'
topics = '''<section class="section" id="fundamental-technologies"><p class="eyebrow">Research by Method</p><h2>Fundamental Technologies</h2></section>
<section class="topic" id="multimodality"><span class="topic-label">MULTIMODALITY</span><div><h2>Multimodality</h2><p>We investigate multimodal understanding, fusion, and compositional and combinatorial modeling across text, images, audio, graphs, and symbolic data.</p><h3>Understanding and Fusion</h3><p>Learning representations of heterogeneous information, understanding the relationships between modalities, and combining complementary signals.</p><h3>Compositional and Combinatorial Modeling</h3><p>Modeling how individual elements combine into coherent structures and sets, with applications in bundle construction, recommender systems, and related tasks.</p></div></section>
<section class="topic" id="forecasting"><span class="topic-label">FORECASTING</span><div><h2>Forecasting</h2><p>We aim to anticipate future events and behavior at both macro and micro scales.</p><h3>Macro-level Forecasting</h3><p>Financial forecasting and geopolitical event forecasting: reasoning about markets, economies, and evolving events in the wider world.</p><h3>Micro-level Forecasting</h3><p>User behavior forecasting in recommender systems and cyber attack sequence prediction: modeling how individual actions and sequences unfold over time.</p></div></section>'''
page('research.html','Research','Research',research_intro+topics+domain_sections()+'<section class="section"><h2>Research talks</h2><p class="tagline">Slides on bundle recommendation and generation, LLMs for cybersecurity, and multimodal open-world event forecasting.</p>'+link('Browse talks and slides →','talks.html','text-link')+'</section>')

group_intro = '<div class="page-intro"><p class="eyebrow">Singapore Management University</p><h1 class="lab-name">LMF<span>Lab for Multimodality<br>and Forecasting</span></h1><p>We connect multimodal understanding and modeling with forecasting at macro and micro scales, grounded in real-world problems.</p><p class="lab-director">Led by '+link('Yunshan Ma','index.html')+' · School of Computing and Information Systems</p></div>'
group_pillars = '<section class="section"><h2>What we study</h2><div class="research-grid">'+''.join('<article class="research-item"><span class="number">'+t[1]+'</span><h3>'+t[2]+'</h3><p>'+t[3]+'</p>'+link('Explore this direction →','research.html#'+t[0],'text-link')+'</article>' for t in TOPICS)+'</div></section>'
group_domains = '<section class="section"><h2>Where we apply it</h2><div class="domain-grid">'+''.join('<article><h3>'+link(name,'research.html#'+domain_slug(name))+'</h3><p>'+ESC(description)+'</p></article>' for name,description,_ in DOMAINS)+'</div></section>'
page('group.html','LMF','LMF · Lab for Multimodality and Forecasting',group_intro+group_pillars+group_domains+'<section class="section"><h2>Connect with LMF</h2><p class="tagline">For research inquiries, contact '+link('Yunshan Ma','mailto:ysma@smu.edu.sg')+'.</p>'+link('ysma@smu.edu.sg','mailto:ysma@smu.edu.sg','text-link')+'</section>')

years = sorted({p['year'] for p in PAPERS},reverse=True)
pub_intro = '<div class="page-intro"><p class="eyebrow">Publications</p><h1>Research &amp; publications.</h1><p>Multimodality and forecasting, with applications in fashion, finance, cybersecurity, music, and social events.</p>'+link('Google Scholar ↗',SCHOLAR,'text-link')+'</div>'
filters = '<div class="filters"><div class="search-wrap">'+icon('search')+'<label class="skip" for="publication-search">Search publications</label><input id="publication-search" type="search" placeholder="Search by title, author, or venue…" autocomplete="off"></div><label class="skip" for="publication-domain">Filter by domain</label><select id="publication-domain"><option value="">All domains</option>'+''.join(f'<option value="{name}">{name}</option>' for name,_,_ in DOMAINS)+'</select><label class="skip" for="publication-year">Filter by year</label><select id="publication-year"><option value="">All years</option>'+''.join(f'<option value="{y}">{y}</option>' for y in years)+'</select></div><p class="result-count" id="result-count" role="status" aria-live="polite">'+str(len(PAPERS))+' publications</p>'
groups = ''.join(f'<section class="publication-group" aria-label="Publications {y}"><h2 class="year-heading">{y}</h2>'+''.join(paper(p,True) for p in PAPERS if p['year']==y)+'</section>' for y in years)
note = '<p class="provenance">Recent entries were added from the news on my existing website. Author lists are included where provided in the original publications page. ¹ PortfolioPilot is listed under 2025 as announced; its conference year needs confirmation.</p>'
page('publications.html','Publications','Publications',pub_intro+filters+groups+'<p class="empty" id="empty-results" hidden>No matching publications. Try another search or year.</p>'+note)

talk_intro = '<div class="page-intro"><p class="eyebrow">Talks &amp; slides</p><h1>Ideas in conversation.</h1><p>Invited talks and research seminars on multimodal forecasting, cybersecurity, and generative recommendation.</p></div>'
talk_topics = ['Bundle Recommendation and Generation','LLM for Cybersecurity','Multimodal Open-World Event Forecasting']
talks = ''
for topic in talk_topics:
    talks += '<section class="section"><h2>'+ESC(topic)+'</h2>'
    for d,title,where,file in sorted([talk for talk in TALKS if talk[1] == topic],key=lambda talk:talk[0]):
        talks += f'<article class="talk"><time datetime="{d.replace("/","-")}">{date_label(d)}</time><div><h3>{ESC(where)}</h3><div class="resources">'+link('Slides ↗', 'image/'+quote(file))+'</div></div></article>'
    talks += '</section>'
page('talks.html','Talks','Talks',talk_intro+talks)

cv_intro = '<div class="page-intro"><p class="eyebrow">Curriculum vitae</p><h1>Yunshan Ma <span class="chinese" lang="zh">马云山</span></h1><p>Assistant Professor · School of Computing and Information Systems<br>Singapore Management University</p><div class="page-actions"><button type="button" class="print-button" data-print>Print / save as PDF ↗</button>'+link('ysma@smu.edu.sg','mailto:ysma@smu.edu.sg','text-link')+'</div></div>'
experience = '<section class="cv-section"><h2>Education &amp;<br>Experience</h2><div>'+''.join(f'<div class="experience-item">{item}</div>' for item in DATA['experience'])+'</div></section>'
awards = '<section class="cv-section"><h2>Honors &amp;<br>Awards</h2><ul>'+''.join(f'<li>{ESC(item)}</li>' for item in DATA['awards'])+'</ul></section>'
service_html = ''
for s in DATA['service']:
    parts = re.split(r'<br\s*/?>',s['html'])
    service_html += '<div class="service-group"><h3>'+re.sub('<[^>]+>','',parts[0]).strip()+'</h3><ul>'+''.join('<li>'+re.sub(r'^\s*-\s*','',part.strip())+'</li>' for part in parts[1:] if part.strip())+'</ul></div>'
service = '<section class="cv-section"><h2>Professional<br>Service</h2><div>'+service_html+'</div></section>'
background = '<section class="section" id="background"><h2>Background &amp; Service</h2>'+experience+awards+service+'</section>'
page('index.html','About','About',intro+research_grid+latest+selection+background)
cv_pdf = ROOT / 'assets/pdf/Yunshan_Ma_CV.pdf'
if cv_pdf.is_file():
    cv_viewer = '<div class="page-intro"><p class="eyebrow">Curriculum Vitae</p><h1>Yunshan Ma · CV</h1><p><a id="download-cv" href="assets/pdf/Yunshan_Ma_CV.pdf" download="Yunshan_Ma_CV.pdf">Download CV (PDF) ↓</a></p></div><iframe class="cv-pdf" src="assets/pdf/Yunshan_Ma_CV.pdf" title="Yunshan Ma curriculum vitae PDF"></iframe><script>document.getElementById("download-cv").click();</script>'
    page('cv.html','CV','Curriculum Vitae',cv_viewer)
else:
    # Retain the existing working CV until the user supplies the requested PDF.
    page('cv.html','CV','Curriculum Vitae',cv_intro+experience+awards+service)

page('news.html','News','News','<div class="page-intro"><p class="eyebrow">News archive</p><h1>Updates &amp; milestones.</h1><p>Research announcements, awards, and academic activities.</p></div><div class="news-archive">'+news(DATA['news'])+'</div>')
page('404.html','404','Page not found','<div class="page-intro"><p class="eyebrow">404</p><h1>Page not found.</h1><p>The page may have moved.</p>'+link('Return to the homepage →','index.html')+'</div>')

print(f'Built {len(list(OUT.glob("*.html")))} pages with {len(PAPERS)} publications, {len(DATA["news"])} news items, and {len(TALKS)} talks in {OUT}')

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--publish-root', action='store_true', help='Also copy the built site to the repository root for branch-based GitHub Pages hosting.')
args = parser.parse_args()
if args.publish_root:
    for source in OUT.iterdir():
        destination = ROOT / source.name
        if source.is_dir():
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(source, destination)
    print('Updated root HTML and assets for branch-based GitHub Pages hosting; existing extra files were preserved.')
