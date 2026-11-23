# Meníčko Litomyšl

Daily lunch menus from Litomyšl restaurants on one page, with search. The menus come from each restaurant's own website (never from menicka.cz).

Restaurants: U Kolji, Bohém (Hotel Aplaus), Underground, Da Nicola, Šnyt, Oáza zdraví, Rettigovka, U Medvěda (from its weekly PDF), Karlov and Plums (menu images read with Tesseract OCR in the GitHub workflow; not runnable on an Intel Mac, where Homebrew cannot build Tesseract).
Not included: Veselka (only a menicka.cz widget), Zlatá Hvězda (shows a CAPTCHA to GitHub and Cloudflare).

## How it works
- `scraper/` downloads each restaurant's menu page and parses it into `site/menus.json`.
- `site/` is a static page (`index.html`, `app.js`, `style.css`) that renders that JSON.
- `.github/workflows/update.yml` runs the scraper every weekday at 6:23, 7:53 and 9:23 (Prague, winter time; GitHub sometimes delays or skips a scheduled run, hence three) and publishes `site/` to Cloudflare Pages.

## Proxy for blocked sites
Underground and Da Nicola drop connections from GitHub's servers, so they are fetched through a Cloudflare Worker (`proxy/worker.js`, deployed at `menicko-proxy.martin-norty.workers.dev`). It only forwards the hosts listed in `ALLOWED`. To redeploy after a change: `cd proxy && npx wrangler deploy`.
## Run locally
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m scraper.run
python3 -m http.server 8765 --directory site   # open http://localhost:8765
```

## Publish
The site is at **https://menicko-litomysl.pages.dev** (Cloudflare Pages, free). The GitHub Actions workflow scrapes, tests and deploys it on schedule and on every push to `main`.
1. Cloudflare Pages project `menicko-litomysl` (created once: `npx wrangler pages project create menicko-litomysl --production-branch main`).
2. Repository secrets (**Settings → Secrets and variables → Actions**): `CLOUDFLARE_API_TOKEN` (a token with *Account → Cloudflare Pages → Edit*) and `CLOUDFLARE_ACCOUNT_ID`.
3. Under **Actions → Update menus**, click **Run workflow**.

## Adding a restaurant
1. Save its menu page into `tests/fixtures/<id>.html` and write a test in `tests/test_parsers.py`.
2. Add `scraper/parsers/<id>.py` with `parse(html) -> [{"date": "YYYY-MM-DD", "items": [...]}]`. Use `page_lines()` and `item()` from `scraper/parsers/__init__.py`.
3. Register it in `scraper/restaurants.py`.
