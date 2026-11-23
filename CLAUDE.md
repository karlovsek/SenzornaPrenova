# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Not a software project: the Slovenian-language book series **Senzorna prenova** by Peter Karlovšek. All content and UI text is Slovenian; write new text in correct, grammatically declined Slovenian, with vikanje (»poimenujte«, not »poimenuj«). The only exception is the youth handbook, which uses tikanje with forms for both genders (»si opazil(a)«).

Three books, each a single self-contained HTML file (CSS, content, JS) that is the source of truth, with a PDF generated from it (never edit a PDF by hand, rebuild instead):

- `Senzorna prenova – zgornji del trupa.html` / `.pdf` — the textbook **»Senzorna prenova: kako prebuditi zakrčeno telo in um«** (upper-body 30-day program, 2nd edition draft, 37 chapters, ~81 pages). Ideas from Gabor Maté's *The Myth of Normal* are woven into chapters 9, 10, 18, 19, 21, 23, 34 and 35 as metaphors, questions and exercises (no claims that emotions cause illness), each credited with a `navdih` line, source in Dodatek B. `analiza-myth-of-normal.md` holds the analysis behind them.
- `Senzorna prenova – čustvena inteligenca.html` / `.pdf` — the sister handbook **»Senzorna prenova: čustvena inteligenca«** (1st edition draft, 18 chapters, 4-week program, ~52 pages). Goleman's five pillars with the body as the common thread; it cross-references textbook chapters by number (2, 8–9, 22–24, 29, 35), so renumbering the textbook means updating those too. Content from Elizabeth April's video is kept only inside boxes labelled »Pogled Elizabeth April« (her personal view, not science) in chapters 9 and 11, with the source in Dodatek B. Likewise, content from Gabor Maté's *The Myth of Normal* is kept in boxes labelled »Pogled Gaborja Matéja« (chapters 6, 11, 16; one plain sentence in chapter 7 points to them), sources in Dodatek B. Chapter 10 (»Od odtisa do spremembe«) and parts of chapters 9, 11 and 18 are based on a Teal Swan interview (»How the Law of Attraction REALLY works! (Part 1)«), written in psychological language without naming her (author's decision); the only trace is the video title in Dodatek B. Her unsafe or false claims (sink into depression, every recalled image is a true memory, science proves simultaneous timelines) were deliberately left out. When the text means the textbook or the series, it names them with the noun (»učbenik Senzorna prenova«, »zbirka Senzorna prenova«, title undeclined); bare »Senzorna prenova« (declined) means only the method.
- `Senzorna prenova – čustvena inteligenca – mladi.html` / `.pdf` — the youth handbook **»Senzorna prenova: čustvena inteligenca za mlade«** (ages 12–16, 1st edition draft, 16 chapters in 7 parts, 4-week challenge, ~45 pages). Same red thread as the adult handbook (five pillars as »pet supermoči«, emotion starts in the body, short rhythm), but simpler: tikanje, chapters of 400–600 words, sentences up to ~15 words, no English terms and no »Za radovedne« boxes (removed at the author's request). A recurring cast (Nika 12, Marko 13, Žan 14, Lara 15, each with a colour and an SVG avatar `#lik-*`) opens every chapter with a `.strip` comic. **No personal views:** no Elizabeth April, Gabor Maté or Teal Swan content (and no »Most v otroštvo« or digging into childhood memories), no appendix for parents/teachers, no textbook chapter cross-references. Food or weight is never used as an example of escape. Safety box »Tvoj varni kotiček« in the intro (TOM 116 111 daily 12–20, Samarijan in Sopotnik 116 123 24 h, Klic v duševni stiski 01 520 99 00 daily 19–7, 112, school counsellor, safe.si; verified November 2026), repeated on the »Moja kartica za umirjanje« worksheet and in Dodatek B. `analiza-prirocnik-za-mlade.md` holds the writing guidelines and the adult → youth chapter mapping.
- `UČBENIK PROGRAMA ZA ZGORNJI DEL TELESA.pdf` — the original 1st edition (A. Ernst, V. Cijan, 2021). Read-only source material.

## Branding rules (decided by the author)

- The former brand **AEQ** (and `®`, `www.aeq.si`, the AEQ teacher "stopnje" system) must not appear anywhere. The method is called »Senzorna prenova« (decline it: Senzorne prenove, Senzorni prenovi, Senzorno prenovo).
- The original authors appear only as a source, and only in the textbook: one line in the footer (»Delno po gradivu A. Ernsta in V. Cijan (2021).«) and one entry in Dodatek B. The emotional-intelligence handbook is not based on their material and must not mention them at all.
- Check after edits: `grep -n -i "aeq\|ernst\|cijan\|senčar\|®" "Senzorna prenova – zgornji del trupa.html"` should hit only those two lines; the same grep on `Senzorna prenova – čustvena inteligenca.html` should hit nothing. On the youth handbook, `grep -n -i "aeq\|ernst\|cijan\|senčar\|®\|april\|maté\|swan" "Senzorna prenova – čustvena inteligenca – mladi.html"` should hit nothing (so never write the month »april« there).

## Building the PDF

Run from the project root:

```
python tools/build_pdf.py                                   # builds the textbook PDF next to its HTML
python tools/build_pdf.py "Senzorna prenova – čustvena inteligenca.html"   # any other HTML: PDF of the same name next to it
python tools/render.py "<pdf>" tools/build/out.png 1,2,3    # contact sheet of chosen pages for a visual check
```

Python deps (pypdf, pypdfium2, pillow) are vendored in `tools/pylib/` (system Python doesn't have them); both scripts add it to `sys.path`. To reinstall: `pip install --target tools/pylib -r tools/requirements.txt`. Intermediate files and the cached inlined fonts (`fonts.css`, delete to refetch) go to `tools/build/`.

How the build works:
- Prints with headless Chrome (`C:\Program Files\Google\Chrome\Application\chrome.exe --print-to-pdf`), Google Fonts inlined as base64 so headless rendering uses them.
- Print TOC page numbers come from `data-page` attributes that the build injects: pass 1 inserts invisible `@@id@@` markers into every `[data-toc]` heading, reads which PDF page each lands on, writes `data-page`, re-renders until the numbers are stable, then does a final render without markers.
- Fails with a clear message if the output PDF is open in another program.

After building, extract the PDF text with pypdf and grep it for the brand rules above, and look at rendered pages (cover, TOC, a chapter, the tracker, last page).

## HTML structure

Both books share the same structure and CSS (the handbook's `<style>` was copied from the textbook without the cycle diagrams, state ladder, check-in and budget widgets); the running header text in `@page @top-right` differs. The youth handbook starts from the adult handbook's CSS but with Bricolage Grotesque as body font, a livelier palette (`--nika`, `--marko`, `--zan`, `--lara`, mood colours `--red`/`--yellow`/`--green`/`--blue`) and its own components: `.cast`, `.strip`/`.pan`/`.say`/`.bub`/`.sms` (comics; `.ch-head` wraps eyebrow, title, key sentence and strip so they print unbroken), `.phone`, `.mood` (colour mood meter), `.emo-grid`, `.card-grid`/`.tcard`, `.chips`, `details.flip` (flip cards) and `details.qz` (quiz; all `details` open in print), `.missions`, `.calm`, `.mood-days`, `.fill`/`.sentence` (fill-in lines). In print its parts and worksheets start on a new page, chapters flow on. The adult handbook adds `.spectrum`, `.myths`/`.myth` and `.journal`, and in print lays out `section.ch` as a block (not grid) so `break-after:avoid` keeps the chapter eyebrow with its heading.

- **Chapters:** `<section class="ch" id="pN" data-toc="Title" data-num="N">`; **parts:** `<div class="part-head" id="delN" data-toc="VIII · Title">`. Both the screen TOC (sticky `<nav class="toc">`) and the print TOC are generated by JS from `[data-toc]` — change titles there, not in a TOC list.
- Chapter numbers are hard-coded in `data-num` and in in-text cross references (»več v poglavju 29«) and in Dodatek C's table. Renumbering or inserting a chapter means updating all of these.
- Recurring blocks: `.box` variants `kljucne` (Ključne točke), `vprasanja` (Vprašanja zase), `primer`, `vaja`, `varno`, `razlaga`; collapsible `<details class="radoved">` (»Za radovedne«); `<figure class="figure">` with inline SVG. Two cycle diagrams (`#cyc-bad`, `#cyc-good`) are drawn by JS.
- Colours are CSS custom properties on `:root` with a dark-mode override (`prefers-color-scheme` + `[data-theme]`); `<html data-theme="light">` in all books forces the light theme on screen (the dark palette stays in the CSS but is switched off at the author's request; remove the attribute to restore it); print styles are in `@page` / `@media print` (running header text is in `@page @top-right`).
- The trackers (`#weeks`) save checkboxes to `localStorage`: the textbook's 30-day tracker under key `sp30-dni-izdaja2`, the handbook's 4-week (28-day) tracker under `sp-eq-4-tedni`, the youth handbook's stamp tracker under `sp-eq-mladi-4-tedni` (only the stamps are stored, never journal text); changing a key resets users' progress.
- Dodatek C (»Opombe za avtorja«) in the textbook holds only open questions for the author; it is meant to be removed before print. The handbook's Dodatek C was removed at the author's request (it ends with Dodatek B). The change log versus the 1st edition was removed at the author's request (it is in git history before that commit); do not re-add it, record changes in commit messages instead.
