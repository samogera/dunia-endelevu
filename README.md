# Dunia Endelevu website

The website of **Dunia Endelevu**, a youth-led climate incubator in Nairobi, Kenya. It helps children under 18 publish their own climate books, speak on the podcast *Climate Gumzo* and take the stage at environmental events.

It is a fast, dependency-free static site: plain HTML, one stylesheet and one small script. The fonts are self-hosted, so the site sets no tracking cookies.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home |
| `about.html` | Who we are, what we believe, founder bio, volunteer form, safety FAQ |
| `programs.html` | The Youth Advocate Journey: Storyteller, Voice and Diplomat tracks, sponsor options, FAQ |
| `donate.html` | Donation pledge: choose one or more gifts (a child’s book, a podcast episode, a child at an event, books for a school, where it’s needed most), any amount, payment preference, named or anonymous. We email the donor how to pay. |
| `contact.html` | Apply for a child (parent or guardian form) and an enquiry form |
| `privacy.html`, `terms.html`, `cookies.html` | Legal pages |
| `404.html` | Page not found |

## Put it online with GitHub Pages

1. On GitHub, open **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**, then branch **main** and folder **/ (root)**. Save.
3. After a minute the site is live at **https://samogera.github.io/dunia-endelevu/**.

## Social media links

The footer shows Instagram, TikTok, X, Facebook, LinkedIn, YouTube and Spotify icons. Only Spotify (Climate Gumzo) has a link so far. To switch the others on, paste each full profile link into `SOCIAL` near the top of `src/build.py`, then run `python3 src/build.py`. Icons without a link are shown but are not clickable.

## Switch on the forms

The application, enquiry, volunteer and donation forms send email through [FormSubmit](https://formsubmit.co) to **hello@duniaendelevu.org**.

1. Make sure that inbox exists. To use a different one, change `FORM_INBOX` at the top of `assets/js/site.js`, and the address shown on the pages (`EMAIL` in `src/build.py`), then rebuild.
2. Send one test message from the live site. FormSubmit emails the inbox an **Activate Form** link. Click it once.
3. From then on every submission arrives as an email. The person who filled in the form gets an automatic confirmation.

If sending fails, the form keeps what the visitor typed and offers to open it as an email instead.

## Edit the site

The finished pages are generated, so edit the sources and rebuild:

- `src/pages/*.html` holds the main content of each page.
- `src/build.py` holds the shared parts: the `<head>`, header, mobile menu and footer, plus page titles and descriptions.
- `src/art/*.svg` holds the illustrations.
- `assets/css/site.css` and `assets/js/site.js` hold all styling and behaviour.

Then run:

```bash
python3 src/build.py
```

This rewrites the `.html` pages at the root, plus `sitemap.xml` and `robots.txt`. It needs only Python 3, with no packages to install.

### Use your own domain

In `src/build.py`, set `SITE_URL` (for example `https://duniaendelevu.org/`) and `BASE_PATH` (`/`), then rebuild. Add the domain under **Settings → Pages → Custom domain**.

### Replace an illustration with a photo

Each illustration sits in a `<figure class="art">`. To use a photo, put the image in `assets/img/` and replace the `{{art:...}}` line with:

```html
<img src="assets/img/your-photo.jpg" alt="Describe what the photo shows" width="1000" height="800" loading="lazy">
```

Only publish photos of children with separate written permission from a parent or guardian. Never show a child's face together with their full name or school.

## Brand

- **Logo, "The Speaking D":** the D of Dunia is a speech bubble, the E of Endelevu hides inside it, and a sun rises over the horizon. In the wordmark, the dot of the i is the same sun. The full logo pack (SVG, PNG, favicon, social banner) is at `assets/brand/dunia-endelevu-logo-pack.zip`.
- **Colours:** Sage page `#EDF3EF`, White cards `#FFFFFF`, Evergreen `#12372F`, Ink `#0F2A23`, Sun `#F2B233`. Use the accents sparingly: Leaf `#2F6B57` and Clay `#B9542F`.
- **Type:** Inter Tight (headings) and Inter (text). Both are under the SIL Open Font License, included in `assets/fonts/`. The logo wordmark is drawn from Fraunces and stored as outlines.
- **Buttons, one rule:** the filled Evergreen button is the main action, used once per section; the outlined button is the secondary action beside it. Sun yellow is used for the small arrow circle inside buttons, and as the button colour on dark Evergreen surfaces, where Evergreen would not show.
- **Forms:** field borders are `#8A938F`, which meets the 3:1 contrast needed for form controls.

### Photos

Photos live in `assets/img/photos/`, each as `.webp` with a `.jpg` fallback. Before launch, confirm the licence for every stock photo (some free licences require a credit line). Only publish photos of children with written permission from a parent or guardian.

## Before launch

- Confirm the contact inbox and activate the forms (see above).
- Have the Privacy Policy, Terms and Cookie Policy reviewed by a Kenyan lawyer, especially the sections on children's data under the Data Protection Act, 2019.
- Submit `sitemap.xml` in Google Search Console.

© Dunia Endelevu. All rights reserved.
