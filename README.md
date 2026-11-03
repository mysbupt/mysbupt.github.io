# Yunshan Ma — personal academic website

Recommended template: **[al-folio](https://github.com/alshedivat/al-folio)**, a popular academic website theme with publication, news, and CV layouts. [View its demo](https://alshedivat.github.io/al-folio/).

This implementation is a **static adaptation inspired by al-folio**, with its academic layout, restrained purple accent, right-aligned portrait, publication rows, and light/dark appearance. It is not the upstream Jekyll theme installation. It uses HTML, CSS, JavaScript, and a Python build script so it can run without Ruby, Jekyll, npm, or external frontend dependencies. Theme attribution and the upstream MIT license are included.

Content was imported from https://mysbupt.github.io/ on 3 November 2026. The original HTML is preserved in `content/original/` for comparison. The website includes About, Research, Publications, Talks, CV, and a news archive; publication search, year filtering, responsive navigation, dark mode, and a print-friendly CV are implemented. The seven existing public PDFs are included, and existing `/image/` PDF paths are preserved.

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

- The original Publications page ends at 2024. Recent papers were carried over from the homepage news; missing author lists have not been invented.
- 60 valid publication entries, 33 news announcements, 6 talks, and 8 honors are included.
- An ACM Multimedia 2019 demo entry repeats an author list where its title should be. It is preserved in the original source and imported JSON, but excluded from the displayed list pending a correct title.
- PortfolioPilot's source announcement is dated October 2025 and says AAAI 2025. The new list keeps it under 2025 and flags the conference year for confirmation.
- The music paper is listed under MMM 2026 based on the explicit January 2026 award announcement, despite an older announcement saying MMM 2025.
- BundleLM is listed under MMM 2027; Potent but Stealthy under AAAI 2026, matching the announced conference years.
- Minor typography fixes include the duplicated “DiFashion” prefix, spacing in FashionDPO, and “Finalist”. Unavailable PDFs are plain text, not broken empty links.
- PDF/code/dataset links are preserved from the source, not independently checked against publisher metadata. Bibliographic details should be reviewed before public deployment.

## LMF research structure and selected publications

The group is **LMF: Lab for Multimodality and Forecasting**, with a group overview at `group.html`. The research page presents two pillars: multimodal understanding/fusion and compositional/combinatorial modeling; and forecasting at macro scales (financial and geopolitical events) and micro scales (user behavior and cyber attack sequences). Applications are organized into Fashion, Finance, Cybersecurity, Music, and Social Events. Social Events includes Context-aware Event Forecasting via Graph Disentanglement (KDD 2023), Scattered Hypothesis Generation for Open-Ended Event Forecasting (ACL 2026 Findings), and ThinkTank-ME (WWW 2026 Short). The publication page supports domain filtering and title-based deep links.

The homepage presents a single list of nine selected publications in reverse chronological order by publication year: six paper/demo award winners, AttacKG+, Learning to Generate Explainable Stock Predictions using Self-Reflective Large Language Models, and CrossCBR. Awards appear on the corresponding papers; there are no category subheadings. No current citation counts or comprehensive citation ranking are asserted. The 2018 finalist and the personal NUS research achievement award remain in the CV but are not classified as award-winning papers in this selection.

AttacKG+ and AlphaEdit were missing from the initial imported publication list and have been added using their author/publisher records. Bibliographic source URLs are stored on those records in `content/site.json`. The earlier public group page is retained in `content/original/group.html` for reference; the new group page does not assert a current member roster.

## Page organization and CV PDF

Navigation labels use initial capitals. Research is organized by Fundamental Technologies and Vertical Domains. Talks are grouped into the three original topics, with oldest-to-newest talk dates within each topic. Education/experience, honors/awards, and professional service now appear at the bottom of About.

The CV navigation opens a new tab. The user-supplied `CV_Ma_Yunshan_202608.pdf` is preserved byte-for-byte at `assets/pdf/Yunshan_Ma_CV.pdf`. The CV page displays that PDF and requests its download, with a visible Download CV link if the browser blocks automatic downloads. Background, education, honors, and service remain at the bottom of About.
