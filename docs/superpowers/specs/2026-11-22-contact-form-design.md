# Kontaktní formulář – návrh

Velikost: malá změna (jeden formulář na statické stránce, bez backendu).

## Proč
Lidé (restaurace i návštěvníci) mají mít možnost napsat provozovateli a dostat odpověď. Provozovatelova e-mailová adresa nesmí být na stránce ani ve veřejném repozitáři; v odpovědi ji vidět může. Kontakt nesmí otevřít cestu pro spam.

## Cíle
- Zpráva z webu dorazí do provozovatelova Gmailu s adresou pro odpověď nastavenou na odesílatele, takže se odpovídá obyčejným „Odpovědět“.
- Funguje na telefonu i počítači, bez poštovního klienta.
- Adresa provozovatele není v HTML, JS ani v gitu.

## Mimo rozsah
- Vlastní doména, vlastní backend, ukládání zpráv, odpovídání z neutrální adresy.

## Anti-cíle (selhání, i kdyby to fungovalo)
- Stránka začne při načtení stahovat cizí skripty, cookies nebo měření (dnes nenačítá nic cizího).
- Formulář přebije menu: musí být nenápadný, menu zůstávají hlavní věcí.
- Zpráva tiše zmizí: odesílatel vždy vidí, jestli se odeslala, nebo co dělat, když ne.

## Zvažované cesty
- **A) Formulářová služba Web3Forms (zvoleno).** Formulář posílá zprávu na `api.web3forms.com`, služba ji doručí do Gmailu, Reply-To = odesílatel. Na stránce je jen přístupový klíč, adresa ne. Služba filtruje spam. Daň: zprávy jdou přes cizí službu; klíč je veřejný, takže kdo ho najde, může posílat zprávy přímo do služby (zachytí je její filtr, ne vždy).
- **B) Adresa složená až po kliknutí (mailto).** Bez cizí služby, ale adresa je v kódu jen zakódovaná a repo je veřejné; na telefonu bez pošty nefunguje.
- **Vlastní Worker (vyřazeno).** Bez vlastní domény Cloudflare e-maily neposílá; obchvaty přes další služby jsou křehčí než A.

Provozovatel zvolil A.

## Jak (rozhodnuto)
- **Umístění:** v patičce odkaz-přepínač „Napište nám“ (nativní `<details>`), po rozbalení formulář. Nic se nenačítá, dokud se neodešle.
- **Pole:** e-mail (povinný, `type=email`), zpráva (povinná). Skryté: přístupový klíč, předmět „Meníčko Litomyšl – zpráva z webu“, past na roboty (`botcheck`, skryté políčko, které vyplní jen robot).
- **Odeslání:** `fetch` na `https://api.web3forms.com/submit`; tlačítko během odesílání zakázané; výsledek v textu pod formulářem (`aria-live`): úspěch („Díky, ozveme se e-mailem.“, formulář se vyprázdní) nebo chyba s radou zkusit znovu později. Bez JS funguje obyčejné odeslání formuláře.
- **Soukromí:** pod formulářem jedna věta, že zprávu doručuje služba Web3Forms.
- **Vzhled:** podle DESIGN.md – pole jako vyhledávání (papír, černá linka), tlačítko jako denní štítek, popisky v systémovém písmu, žádná červená mimo stav (chyba odeslání smí být červeně). Funguje ve světlém i tmavém režimu a na telefonu.

## Co udělá provozovatel
- Na web3forms.com zadá svůj e-mail a dostane přístupový klíč (účet a klíč zakládá on, ne Claude). Klíč pošle; přijde do `site/index.html`.

## Nechává se na stavitele
- Přesné CSS a texty v rámci výše; ověřit aktuální API Web3Forms (název pole pro past, formát odpovědi, limit zdarma) v jejich dokumentaci; jeden test odeslání s reálným klíčem.
