# Magic: the Gathering Rare Price Visualizer

This repo contains code used to visualize the price of magic rares by set, color, and year.

Data is gathered from [Scryfall](https://scryfall.com/) using python on a best-effort basis.

[D3.js](https://github.com/d3/d3) consumes the generated CSV files and creates the plots.

## Hosted with Github Pages

https://bpleines.github.io/magic_card_price_visualizer/

### Generate data

```sh
python generate_data.py
```
