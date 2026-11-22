const DAY_NAMES = ["Ne", "Po", "Út", "St", "Čt", "Pá", "So"];

const norm = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
const iso = (d) => d.toLocaleDateString("sv-SE"); // YYYY-MM-DD in local time
const el = (tag, cls, text) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
};

let data, selectedDate;

// favourite restaurants live only in this browser; storage can be blocked (private mode), so never rely on it
const FAV_KEY = "menicko-favorites";
let favorites = new Set();
try { favorites = new Set(JSON.parse(localStorage.getItem(FAV_KEY)) || []); } catch {}

function toggleFavorite(id) {
  if (!favorites.delete(id)) favorites.add(id);
  try { localStorage.setItem(FAV_KEY, JSON.stringify([...favorites])); } catch {}
  render();
  document.querySelector(`.fav[data-id="${id}"]`)?.focus(); // the card moved; keep keyboard focus on its heart
}

const HEART = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>';

function favButton(r) {
  const on = favorites.has(r.id);
  const b = el("button", "fav");
  b.innerHTML = HEART;
  b.dataset.id = r.id;
  b.setAttribute("aria-pressed", on);
  b.setAttribute("aria-label", `${r.name}: ${on ? "odebrat z oblíbených" : "přidat do oblíbených"}`);
  b.title = on ? "Odebrat z oblíbených" : "Přidat do oblíbených";
  b.onclick = () => toggleFavorite(r.id);
  return b;
}

const hasMatch = (date, query) => data.restaurants.some((r) =>
  r.days.some((d) => d.date === date && d.items.some((i) => norm(i.name).includes(query))));

// switching day moves along the week: menus enter from the side of time (see style.css)
function goToDay(date) {
  const dir = date > selectedDate ? "later" : "earlier";
  selectedDate = date;
  if (!document.startViewTransition) return Promise.resolve(render());
  document.documentElement.dataset.dayDir = dir;
  return document.startViewTransition(render).updateCallbackDone;
}

function dayButton(date) {
  const d = new Date(date + "T12:00");
  const name = date === iso(new Date()) ? "Dnes" : DAY_NAMES[d.getDay()];
  const b = el("button", null, `${name} ${d.getDate()}.${d.getMonth() + 1}.`);
  b.onclick = () => goToDay(date);
  return b;
}

function renderDays(dates, query) {
  document.getElementById("days").replaceChildren(...dates.map((date) => {
    const b = dayButton(date);
    b.setAttribute("aria-pressed", date === selectedDate);
    if (query && !hasMatch(date, query)) b.classList.add("no-match");
    return b;
  }));
}

// a search with no hit on the selected day points to the days that have it
function renderEmpty(p, dates, query) {
  const typed = document.getElementById("search").value.trim();
  const other = query ? dates.filter((d) => hasMatch(d, query)) : [];
  if (!query) return p.replaceChildren("Nic nenalezeno.");
  if (!other.length) return p.replaceChildren(`„${typed}“ tento týden nikde nevaří. Zkuste jiné slovo.`);
  p.replaceChildren(`„${typed}“ v tento den nikde nevaří, ale najdete to tady:`, ...other.map((date) => {
    const b = dayButton(date);
    b.onclick = () => goToDay(date).then(() => document.querySelector("#days [aria-pressed=true]").focus());
    return b;
  }));
}

function renderItem(item) {
  const li = el("li", item.type);
  const name = el("span", "name");
  if (item.label) name.append(el("b", null, item.label + " "));
  name.append(item.name);
  li.append(name);
  if (item.price != null) li.append(el("span", "price", item.price + " Kč"));
  if (item.allergens?.length) li.append(el("span", "allergens", "alergeny " + item.allergens.join(", ")));
  return li;
}

function renderCard(r, query) {
  const card = el("section", "card");
  const h2 = el("h2");
  const a = el("a", null, r.name);
  a.href = r.url;
  a.target = "_blank";
  a.rel = "noopener";
  h2.append(a);
  const head = el("div", "card-head");
  head.append(h2, favButton(r));
  card.append(head);
  if (favorites.has(r.id)) card.dataset.fav = "";

  const note = (text) => {
    const p = el("p", "note", text + " ");
    const link = el("a", null, "Podívejte se na web restaurace");
    link.href = r.menu_url;
    link.target = "_blank";
    link.rel = "noopener";
    p.append(link);
    return p;
  };

  if (r.status !== "ok") {
    if (query) return null;
    card.append(note("Menu se nepodařilo načíst."));
    return card;
  }
  if (r.stale) card.append(note("Menu se teď nepodařilo aktualizovat, zobrazujeme poslední načtené."));

  const day = r.days.find((d) => d.date === selectedDate);
  const items = (day?.items ?? [])
    .filter((i) => !query || norm(i.name).includes(query));
  if (!items.length) {
    if (query) return null;
    card.append(el("p", "note", selectedDate ? "Na tento den menu není." : "Menu na tento týden zatím nejsou."));
    return card;
  }
  const ul = el("ul");
  ul.append(...items.map(renderItem));
  card.append(ul);
  return card;
}

// restaurants with food first, favourites first within each group (sort is stable: list order otherwise)
const rank = (card) => 2 * !!card.querySelector("ul") + ("fav" in card.dataset);

function render() {
  const today = iso(new Date());
  const dates = [...new Set(data.restaurants.flatMap((r) => r.days.map((d) => d.date)))]
    .filter((d) => d >= today) // never offer an old menu as current
    .sort();
  if (!dates.includes(selectedDate)) selectedDate = dates[0];
  const query = norm(document.getElementById("search").value.trim());
  renderDays(dates, query);
  const cards = data.restaurants.map((r) => renderCard(r, query)).filter(Boolean)
    .sort((a, b) => rank(b) - rank(a));
  document.getElementById("menus").replaceChildren(...cards);
  const empty = document.getElementById("empty");
  empty.hidden = cards.length > 0;
  if (!cards.length) renderEmpty(empty, dates, query);
}

fetch("menus.json", { cache: "no-cache" })
  .then((r) => r.json())
  .then((json) => {
    data = json;
    const u = new Date(json.updated);
    document.getElementById("updated").textContent =
      `Aktualizováno ${u.toLocaleDateString("cs-CZ")} v ${u.toLocaleTimeString("cs-CZ", { hour: "2-digit", minute: "2-digit" })}`;
    document.getElementById("search").addEventListener("input", render);
    render();
  })
  .catch(() => {
    const p = el("p", "note warn", "Menu se nepodařilo načíst. Zkuste stránku obnovit.");
    document.getElementById("menus").replaceChildren(p);
  });
