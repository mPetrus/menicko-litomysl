# Kontaktní formulář – implementační plán

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** V patičce stránky rozbalovací formulář „Napište nám“, který přes Web3Forms doručí zprávu do provozovatelova Gmailu s Reply-To na odesílatele.

**Architecture:** Statická stránka bez backendu. `<details>` v `<footer>` obsahuje `<form>` s `action` na Web3Forms (funguje i bez JS); `app.js` odeslání zachytí, pošle `fetch` jako JSON a výsledek vypíše do řádku s `aria-live`. Styl v `style.css` podle DESIGN.md.

**Tech Stack:** HTML, vanilla JS, CSS (stávající `site/`); Web3Forms API `https://api.web3forms.com/submit`.

**Spec:** `docs/superpowers/specs/2026-11-22-contact-form-design.md`

## Global Constraints

- Přístupový klíč: `959502bd-9044-4449-836e-18aeb983b6ac` (veřejný z principu, patří do `site/index.html`). Provozovatelova e-mailová adresa nesmí být v žádném souboru.
- Při načtení stránky se nesmí načíst nic cizího; jediný cizí požadavek je odeslání formuláře.
- Předmět zprávy: `Meníčko Litomyšl – zpráva z webu`.
- Texty: přepínač `Napište nám`, popisky `Váš e-mail` a `Zpráva`, tlačítko `Odeslat`, úspěch `Díky, ozveme se e-mailem.`, chyba `Zprávu se nepodařilo odeslat. Zkuste to prosím později.`, poznámka `Zprávu doručuje služba Web3Forms.`
- DESIGN.md: pole jako vyhledávání (papír, bez rámečku na černé, na okrové 2px linka), tlačítko jako denní štítek, popisky v systémovém písmu, Grenze ne; červená jen pro chybový stav; žádné stíny kromě focus ringu.
- Funguje ve světlém i tmavém režimu, na 375px i 1440px, bez vodorovného posunu stránky.

## Review Focus

- Odeslání bez připojení nebo s 429/500 od služby: tlačítko se znovu povolí, zobrazí se chybová věta, text zprávy zůstane ve formuláři.
- Dvojklik na Odeslat: odejde jen jedna zpráva (tlačítko je během odesílání zakázané).
- Prázdný nebo neplatný e-mail: odeslání zastaví prohlížeč (`required`, `type=email`), nic neodejde.
- Robot vyplní skryté pole `botcheck`: služba zprávu zahodí; políčko není vidět ani dosažitelné Tabem.
- Bez JavaScriptu: formulář se odešle obyčejně a služba přesměruje na svou stránku úspěchu.

---

### Task 1: Formulář v patičce

Projekt nemá JS testy; ověřuje se v náhledu (`preview_start` „site“) a jedním skutečným odesláním.

**Files:**
- Modify: `site/index.html` (uvnitř `<footer>`)
- Modify: `site/app.js` (na konec souboru)
- Modify: `site/style.css` (za pravidlo `footer`)
- Commit také: `docs/superpowers/specs/2026-11-22-contact-form-design.md`, tento plán

**Interfaces:**
- Produces: `<form id="contact">` s poli `access_key`, `subject`, `botcheck` (skryté), `email`, `message`; `<p id="contact-status" aria-live="polite">`.

- [ ] **Step 1: Markup v `site/index.html`**

Do `<footer>` za stávající větu přidat `<details class="contact"><summary>Napište nám</summary>…</details>`. Formulář: `id="contact"`, `action="https://api.web3forms.com/submit"`, `method="POST"`; skrytá pole `access_key` a `subject` s hodnotami z Global Constraints; `<input type="checkbox" name="botcheck" hidden tabindex="-1" autocomplete="off">`; `<label>` + `<input type="email" name="email" required autocomplete="email">`; `<label>` + `<textarea name="message" required rows="4">`; `<button type="submit">Odeslat</button>`; `<p id="contact-status" aria-live="polite"></p>`; poznámka o Web3Forms.

- [ ] **Step 2: Odeslání v `site/app.js`**

`submit` listener na `#contact`: `preventDefault`, zakázat tlačítko, `fetch(form.action, {method: "POST", headers: {"Content-Type": "application/json", Accept: "application/json"}, body: JSON.stringify(Object.fromEntries(new FormData(form)))})`; úspěch = `response.ok && json.success` → úspěšná věta do `#contact-status`, `form.reset()`; jinak (i výjimka sítě) chybová věta a `data-error` na `#contact-status`; vždy znovu povolit tlačítko. Texty z Global Constraints.

- [ ] **Step 3: Styl v `site/style.css`**

`summary` jako odkaz (podtržení, kurzor), pole a tlačítko podle DESIGN.md s tokeny `--paper`, `--line`, `--ink`, `--red`; formulář max ~480px, sloupec s mezerou 8px; `#contact-status[data-error]` v `--red`.

- [ ] **Step 4: Ověřit v náhledu**

Světlý i tmavý režim, 375px a 1440px: přepínač otevře formulář; Tab projde e-mail → zpráva → Odeslat (botcheck se nepřeskočí na něj); prázdné odeslání zastaví prohlížeč; `document.documentElement.scrollWidth === innerWidth`; `read_network_requests` při načtení nemá žádný cizí host. Chybový stav: v devtools přesměrovat `fetch` na neplatnou URL (dočasně v konzoli, ne v kódu) → chybová věta, text zůstane.

- [ ] **Step 5: Skutečné odeslání**

Odeslat jednu testovací zprávu z náhledu. Expected: úspěšná věta; provozovatel potvrdí, že zpráva dorazila a „Odpovědět“ míří na zadaný e-mail.

- [ ] **Step 6: Commit**

```bash
git add site/index.html site/app.js site/style.css docs/superpowers/specs/2026-11-22-contact-form-design.md docs/superpowers/plans/2026-11-22-contact-form.md
git commit -m "Contact form in the footer via Web3Forms"
```
