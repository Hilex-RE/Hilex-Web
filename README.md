# Hilex.io

Personal landing page for Michael Abraham — Architect · Realtor · Investor · Designer · Community Builder.

Built as a single static `index.html` (pure Futura type system, navy/electric-blue palette) with assets in `/images`.

## Structure
```
.
├── index.html          # the landing page (self-contained CSS)
├── images/
│   └── headshot-michael-2026.jpg
├── CNAME               # custom domain → hilex.io
└── README.md
```

## Deploy (GitHub Pages)
1. Push to the `main` branch of this repo.
2. Repo → Settings → Pages → Source: **Deploy from a branch** → Branch: **main** / **/(root)** → Save.
3. Under "Custom domain" enter `hilex.io` and save (the included `CNAME` file does this automatically).
4. At your domain registrar (GoDaddy), point DNS at GitHub Pages:
   - Four `A` records for the apex `hilex.io`:
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - One `CNAME` record for `www` → `hilex2030.github.io`
5. Back in Settings → Pages, tick **Enforce HTTPS** once the cert provisions.

## Contact form
The CTA contact form (first name, last name, message) uses EmailJS. Fill the three placeholder values near the bottom of `index.html`: `EMAILJS_PUBLIC_KEY`, `EMAILJS_SERVICE_ID`, `EMAILJS_TEMPLATE_ID`. The EmailJS template variables must be named `first_name`, `last_name`, `full_name`, and `message`. Only the EmailJS public key belongs in client code.

## Notes
- Headshot is referenced at `images/headshot-michael-2026.jpg`.
- Property photos are currently placeholders — swap the `url(...)` values in the `.property-N .property-image` blocks as real photos come in.
- Type stack falls back Futura PT → Futura Std → Century Gothic → Avenir. For exact rendering everywhere, self-host Futura PT (licensed) or substitute a free Futura-alike (Jost*, Spartan).
