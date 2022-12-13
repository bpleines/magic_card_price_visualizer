import pathlib
import requests
import os

import pandas as pd

from codes import MTGCodes

def pandas_implementation(color_code='R'):
    cards = []

    url = f"https://api.scryfall.com/cards/search?q=color%3D{color_code}%28rarity%3Ar+OR+rarity%3Am%29"
    response = requests.get(url).json()
    data = response.get('data')
    for card in extract_card_details(data):
        cards.append(card)
    while response.get('has_more'):
        response = requests.get(response.get('next_page')).json()
        for card in extract_card_details(response.get('data')):
            cards.append(card)
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

def extract_card_details(card_list):
  cards = []
  for card in card_list:
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
          try:
              card_dict["image"] = card.get("image_uris").get("normal")
          except AttributeError as e:
              card_dict["image"] = None
          cards.append(card_dict)
      except TypeError:
          print(f"The card {card.get('name')} was missing an expected value. Skipping!")
          continue
  return cards

def generate_card_csv(color_code='W'):
    csv_file_path = f"{pathlib.Path(__file__).parent.absolute()}/magic_card_csv_files_by_color/{color_code}.csv"
    cards = pandas_implementation(color_code)
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
    cards.to_csv(csv_file_path, index=False)
    print(f"Generated csv data for set: {color_code}")

for color_code in MTGCodes().get_color_codes():
    generate_card_csv(color_code)
