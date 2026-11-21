# Meníčko Litomyšl

Daily lunch menus from Litomyšl restaurants on one page, with search. The menus come from each restaurant's own website (never from menicka.cz).

Restaurants: U Kolji, Zlatá Hvězda, Bohém (Hotel Aplaus), Underground, Da Nicola, Šnyt, Oáza zdraví, Rettigovka.
Not included: U Medvěda (PDF), Karlov and Plums (menu is an image), Veselka (only a menicka.cz widget).

## How it works
- `scraper/` downloads each restaurant's menu page and parses it into `site/menus.json`.
- `site/` is a static page (`index.html`, `app.js`, `style.css`) that renders that JSON.
- `.github/workflows/update.yml` runs the scraper every weekday at 7:00 and 10:00 (Prague, winter time) and publishes `site/` to GitHub Pages.

## Proxy for blocked sites
Underground and Da Nicola drop connections from GitHub's servers, so they are fetched through a Cloudflare Worker (`proxy/worker.js`, deployed at `menicko-proxy.martin-norty.workers.dev`). It only forwards the hosts listed in `ALLOWED`. To redeploy after a change: `cd proxy && npx wrangler deploy`.
Zlatá Hvězda shows a CAPTCHA to both GitHub and Cloudflare, so the site only links to it.

## Run locally
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m scraper.run
python3 -m http.server 8765 --directory site   # open http://localhost:8765
```

## Publish on GitHub Pages
1. Create an empty public repository on github.com.
2. Push this folder to it (`git init`, `git add .`, `git commit`, `git remote add origin …`, `git push -u origin main`).
3. In the repository, go to **Settings → Pages → Source** and select **GitHub Actions**.
4. Under **Actions → Update menus**, click **Run workflow**. The site appears at `https://<user>.github.io/<repo>/`.

## Adding a restaurant
1. Save its menu page into `tests/fixtures/<id>.html` and write a test in `tests/test_parsers.py`.
2. Add `scraper/parsers/<id>.py` with `parse(html) -> [{"date": "YYYY-MM-DD", "items": [...]}]`. Use `page_lines()` and `item()` from `scraper/parsers/__init__.py`.
3. Register it in `scraper/restaurants.py`.
