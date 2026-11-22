# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Anyone in Litomyšl deciding where to have lunch today: mostly locals who work in town. They look on a phone (a quick glance before heading out or on the street) and on a computer at work (a large monitor in the late morning) about equally often, so both must work equally well.

## Product Purpose

One page with today's (and this week's) lunch menus from Litomyšl restaurants: dishes, prices, allergens where the source gives them, and a link to each restaurant. Success: in a few seconds you know what is cooking where today and can pick a place, or find a specific dish ("knedlík") across all restaurants.

## Positioning

Menus are read straight from each restaurant's own website (HTML, PDF, or an image read with OCR), never from aggregators such as menicka.cz. Refreshed automatically every weekday morning.

## Operating Context

- Lunch decision made between roughly 10:30 and 12:00 on weekdays; weekends mostly show "no menu".
- Restaurants publish weekly or daily; some only today's offer. Some sources fail and show the last good menu marked as not updated, or a link to the restaurant.
- Czech-language UI and content.

## Capabilities and Constraints

- Static site (plain HTML, CSS, vanilla JS, no build step) on GitHub Pages, data from a generated `menus.json`.
- Day switching (today first, rest of the week), diacritics-insensitive dish search that also points to other days with a match.
- Favourite restaurants (heart next to the name, stored in the browser) sort to the top.
- Dish types: soup, main (often with a label like A, 1, Pizza I), dessert. Price in Kč; allergens as numbers or names, often missing.
- 10 restaurants today; the number grows over time.

## Brand Commitments

- Must keep: dish search and day switching; favourite hearts with favourites first.
- The name "Meníčko Litomyšl" is current but not marked as binding.

## Evidence on Hand

- Real menus in `site/menus.json`, refreshed by the scraper. No photos of restaurants or dishes; no logos; none may be invented.

## Product Principles

1. Today's food first: the menu content is the page; everything else supports scanning it.
2. Honest sources: always link to the restaurant and say plainly when a menu could not be read or is outdated.
3. Same answer on phone and monitor: no device gets a lesser version.
4. Fast to scan: price and dish name readable at a glance, search finds a dish anywhere.

## Accessibility & Inclusion

Czech UI; keyboard and screen-reader use of search, day switching and favourite toggles must keep working; reduced-motion respected.
