# Yunshan Ma — personal academic website

The frontend is inspired by [Yicong Li’s homepage](https://yl3800.github.io/): a navy-to-teal profile banner, circular portrait, curved transition, and light content sections with compact research cards and publication rows. The site uses its own HTML, CSS, JavaScript, and Python build script, with a light default and an optional dark theme. The earlier layout was inspired by [al-folio](https://github.com/alshedivat/al-folio); its license remains in the repository.

Content was imported from https://mysbupt.github.io/ on 3 November 2026. The original HTML is preserved in `content/original/` for comparison. The website includes About, Research with integrated talks, an LMF overview and Members page, Publications, CV, and a news archive; publication search, year filtering, responsive navigation, dark mode, and a print-friendly CV are implemented. The seven existing public PDFs are included, and existing `/image/` PDF paths are preserved.

## Build and preview

```sh
python3 scripts/build.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:8765/. The `dist` directory is the complete deployable site and can also be opened directly through `dist/index.html`.

## Update content

- `content/site.json`: imported publications, news, honors, service, and experience.
- `scripts/build.py`: biography, research topics, talks, selected publications, page templates, and recent publication venue/year metadata.
- `assets/site.css` and `assets/site.js`: appearance and browser interactions.
- `assets/img/profile.png`: profile photograph.
- `image/`: locally preserved slides and GenWardrobe paper.

Run the build after changes. `scripts/import_original.rb` reproduces the initial import from the preserved source HTML; it requires Ruby and Nokogiri. It is not needed for normal builds and will overwrite edits to `content/site.json`, including curated publication records, domain tags, and award/selection metadata.

## Publish to the existing GitHub Pages site

The target repository is `mysbupt/mysbupt.github.io`, whose default branch is `master`. The upload preserves its root-based static website layout, existing images/PDFs, `group.html`, and legacy styles. The existing `index.html`, `research.html`, and `publications.html` routes are preserved. The previous version remains in Git history.

To update content and regenerate the root files used by GitHub Pages:

```sh
python3 scripts/build.py --publish-root
git add index.html research.html publications.html talks.html cv.html news.html 404.html .nojekyll assets image licenses content scripts README.md .gitignore
git commit -m "Update academic website"
git push origin master
```

GitHub Pages should continue using its existing branch-based deployment configuration (`master`, repository root). The upload does not install a new Actions workflow or change repository settings. `dist/`, preview screenshots, and ZIP archives are excluded from Git.

## Content review notes

- The original Publications page ends at 2024. Recent papers were carried over from the homepage news and completed using public author metadata; BundleLM's author list was supplied directly by Yunshan Ma.
- 66 publication entries, 33 news announcements, 6 talks, and 8 honors are included.
- The malformed ACM Multimedia 2019 demo entry was resolved as Automatic Fashion Knowledge Extraction from Social Media using its arXiv record and DOI; the original HTML remains archived.
- PortfolioPilot's year is corrected to AAAI 2026 using the official AAAI proceedings, which also provide its full author list.
- The music paper is listed under MMM 2026 based on the explicit January 2026 award announcement, despite an older announcement saying MMM 2025.
- BundleLM is listed under MMM 2027; Potent but Stealthy under AAAI 2026, matching the announced conference years.
- Minor typography fixes include the duplicated “DiFashion” prefix, spacing in FashionDPO, and “Finalist”. Unavailable PDFs are plain text, not broken empty links.
- PDF/code/dataset links are preserved from the source, not independently checked against publisher metadata. Bibliographic details should be reviewed before public deployment.

## LMF research structure and selected publications

The group is **LMF: Lab for Multimodality and Forecasting**, with a group overview at `group.html`. The research page presents two pillars: multimodal understanding/fusion and compositional/combinatorial modeling; and forecasting at macro scales (financial and geopolitical events) and micro scales (user behavior and cyber attack sequences). Applications are organized into Fashion, Finance, Cybersecurity, Social Events, and Music. Social Events includes Context-aware Event Forecasting via Graph Disentanglement (KDD 2023), Scattered Hypothesis Generation for Open-Ended Event Forecasting (ACL 2026 Findings), and ThinkTank-ME (WWW 2026 Short). The publication page supports domain filtering and title-based deep links.

The homepage presents a single list of nine selected publications in reverse chronological order by publication year: six paper/demo award winners, AttacKG+, Learning to Generate Explainable Stock Predictions using Self-Reflective Large Language Models, and CrossCBR. Awards appear on the corresponding papers; there are no category subheadings. No current citation counts or comprehensive citation ranking are asserted. The 2018 finalist and the personal NUS research achievement award remain in the CV but are not classified as award-winning papers in this selection.

AttacKG+ and AlphaEdit were missing from the initial imported publication list and have been added using their author/publisher records. Bibliographic source URLs are stored on those records in `content/site.json`. The earlier public group page is retained in `content/original/group.html` for reference; the current member roster is supplied by Yunshan Ma and maintained in `content/members.json`.

## Page organization and CV PDF

Navigation labels use initial capitals. Research is organized by Fundamental Technologies and Vertical Domains. Talks are grouped into the three original topics under Research Talks on the Research page, with oldest-to-newest talk dates within each topic. The main Talks navigation item is removed; `talks.html` redirects to `research.html#research-talks`. Education/experience, honors/awards, and professional service now appear at the bottom of About.

The CV navigation opens a new tab. The user-supplied `CV_Ma_Yunshan_202608.pdf` is preserved byte-for-byte at `assets/pdf/Yunshan_Ma_CV.pdf`. The CV page displays that PDF and requests its download, with a visible Download CV link if the browser blocks automatic downloads. Background, education, honors, and service remain at the bottom of About.

## Palette and author metadata

The logo at https://www.nextcenter.org/ supplied four sampled colors: yellow `#eeb11c`, orange `#de5c1d`, sky blue `#579ece`, and purple `#7962a9`. These colors complement the teal theme in research cards, the LMF monogram, awards, and favicon; readable tonal variants are used for text in light and dark modes. The logo itself is not used as site branding.

All nine selected publications have full author lists. The missing Frozen LVLMs, symbolic/waveform music, financial time-series reasoning, and VibeMus records were completed using arXiv, Springer, and SMU repository metadata. Source URLs are retained on the records in `content/site.json`.

## LMF members

The LMF overview links to `members.html` through the Overview/Members navigation and a Members section. The roster in `content/members.json` preserves the roles and spellings supplied by Yunshan Ma: Assistant Professor, Postdoc, PhD Students, Visiting PhD Students, and Alumni. No personal links, photographs, or additional affiliations have been inferred.

## Full topic citations and publication coverage

All 66 publication records have full author lists. Yunshan Ma is highlighted by name in every citation. The Research page provides expandable publication lists for both fundamental technologies and all five vertical domains; these use the same complete citation component as the Publications and About pages.

On 3 November 2026, an arXiv author search for Yunshan Ma returned 67 records. One known withdrawn record (2005.13129) was excluded. Existing published records were matched by arXiv ID, title, or manually verified renamed-title mappings; 26 previously missing records were added. Distinct existing workshop and conference records were preserved. Confirmed venue information was retained where available, with other added records labeled as arXiv versions rather than inferring an acceptance. arXiv metadata and primary publisher/institutional sources are recorded alongside publication entries. FinAlogy has no verified arXiv identifier, so its placeholder identifier in the code repository was not copied.

Author-list corrections include FashionReGen (SMU/publisher record) and Causal Disentangled Recommendation (arXiv/SMU record). The BundleLM authors are Shuo Xu, Teng Tu, Ai Li, Haokai Ma, Yunshan Ma, Lei Meng, and Xiangxu Meng, in the order provided by Yunshan Ma.

On 4 November 2026, the 21 entries listed only as arXiv preprints were removed at Yunshan Ma’s request. The site retains 66 papers with publication venues; PDF links hosted on arXiv remain available for published papers.
