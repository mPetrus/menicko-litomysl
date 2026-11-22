// Fetches a restaurant menu page from Cloudflare's network for sites that block GitHub's servers.
// Usage: GET https://<worker>/?url=https://www.danicola.cz/denni-menu
const ALLOWED = ["www.jidlolit.cz", "www.danicola.cz"]; // not an open proxy

export default {
  async fetch(request) {
    const target = new URL(request.url).searchParams.get("url");
    if (!URL.canParse(target) || !ALLOWED.includes(new URL(target).hostname)) {
      return new Response("not allowed", { status: 403 });
    }
    return fetch(target, {
      headers: {
        "User-Agent": "Mozilla/5.0 (compatible; menicko-litomysl/1.0)",
        "Accept-Language": "cs-CZ,cs;q=0.9",
      },
    });
  },
};
