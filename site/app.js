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

const hasMatch = (date, query) => data.restaurants.some((r) =>
  r.days.some((d) => d.date === date && d.items.some((i) => norm(i.name).includes(query))));

function dayButton(date) {
  const d = new Date(date + "T12:00");
  const name = date === iso(new Date()) ? "Dnes" : DAY_NAMES[d.getDay()];
  const b = el("button", null, `${name} ${d.getDate()}.${d.getMonth() + 1}.`);
  b.onclick = () => { selectedDate = date; render(); };
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
    b.onclick = () => { selectedDate = date; render(); document.querySelector("#days [aria-pressed=true]").focus(); };
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
  card.append(h2);

  const note = (text) => {
    const p = el("p", "note", text + " ");
    const link = el("a", null, "Podívejte se na web restaurace");
    link.href = r.menu_url;
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

function render() {
  const today = iso(new Date());
  const dates = [...new Set(data.restaurants.flatMap((r) => r.days.map((d) => d.date)))]
    .filter((d) => d >= today) // never offer an old menu as current
    .sort();
  if (!dates.includes(selectedDate)) selectedDate = dates[0];
  const query = norm(document.getElementById("search").value.trim());
  renderDays(dates, query);
  const cards = data.restaurants.map((r) => renderCard(r, query)).filter(Boolean)
    .sort((a, b) => !!b.querySelector("ul") - !!a.querySelector("ul")); // restaurants with food first
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
    document.getElementById("menus").textContent = "Menu se nepodařilo načíst.";
  });
