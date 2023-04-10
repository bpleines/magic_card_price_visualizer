# Magic: the Gathering Rare Price Visualizer

This repo contains code used to visualize the price of magic rares by set, color, and year. Data is gathered from scryfall on a best-effort basis.

Data is scraped using python and translated into csv files to be consumed by D3 Javascript

## Hosted with Github Pages

https://bpleines.github.io/magic_card_price_visualizer/

### Generate data by set code

```sh
python generate_data.py
```

### Generate data by color

```sh
python color_magic_scryfall_data_scraper.py
```
