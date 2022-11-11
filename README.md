# Magic: the Gathering Rare Price Visualizer

This repo contains code used to visualize the price of magic rares by set, color, and year. Data is gathered from scryfall on a best-effort basis.

Data is scraped using python and translated into csv files to be consumed by D3 Javascript

## Quick Start

```sh
open index.html
```

## Generate data by set code

```sh
python set_magic_scryfall_data_scraper.py
```

## Generate data by color

```sh
python color_magic_scryfall_data_scraper.py
```
