import pathlib
import requests
import os

import pandas as pd

from codes import MTGCodes

mtg_set_codes = MTGCodes().get_set_codes()

def pandas_implementation(set_code):
    cards = []

    url = f"https://api.scryfall.com/cards/search?q=set%3A{set_code}+%28rarity%3Ar+OR+rarity%3Am%29"
    response = requests.get(url).json().get("data")
    if not response:
        print(f"set_code {set_code} didn't return any results. Maybe there is a typo?")
        return None
    for card in response:
        card_dict = {}
        try:
            # Replace the commas in name to adhere to csv delimeter
            card_dict["name"] = card.get("name").replace(',', '-')
            card_dict["cmc"] = int(card.get("cmc"))
            card_dict["release_year"] = int(card.get("released_at").split('-')[0])
            card_dict["price"] = float(card.get("prices").get("usd"))
            card_dict["color"] = MTGCodes().encode_color(card.get("color_identity"))
            card_dict["type_line"] = card.get("type_line")
            card_dict["artist"] = card.get("artist")
            # If the card is missing image_uris, give a harcoded photo matching its color
            try:
                card_dict["image"] = card.get("image_uris").get("normal")
            except AttributeError as e:
                card_dict["image"] = MTGCodes().encode_default_image_for_color(card_dict["color"])
            cards.append(card_dict)
        except TypeError:
            print(f"The card {card.get('name')} was missing an expected value. Skipping!")
            continue
    cards_data_frame = pd.DataFrame(
        {
            'name': [card["name"] for card in cards],
            'cmc': [card["cmc"] for card in cards],
            'release_year': [card["release_year"] for card in cards],
            'price': [card["price"] for card in cards],
            'color': [card["color"] for card in cards],
            'image': [card["image"] for card in cards],
            'type_line': [card["type_line"] for card in cards],
            'artist': [card["artist"] for card in cards]
        }
    )
    return cards_data_frame

def generate_card_csv(set_code=mtg_set_codes[0]):
    csv_file_path = f"{pathlib.Path(__file__).parent.absolute()}/magic_card_csv_files_by_set/{set_code}.csv"
    cards = pandas_implementation(set_code)
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
    if cards is not None:
        cards.to_csv(csv_file_path, index=False)
        print(f"Generated csv data for set: {set_code}")

for set_code in mtg_set_codes:
    generate_card_csv(set_code)
