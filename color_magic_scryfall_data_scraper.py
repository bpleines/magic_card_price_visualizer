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
            'colors': [card["colors"] for card in cards],
            'image_uri': [card["image_uri"] for card in cards]
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
          card_dict["colors"] = card.get("color_identity")
          try:
              card_dict["image_uri"] = card.get("image_uris").get("normal")
          except AttributeError as e:
              card_dict["image_uri"] = None
          cards.append(card_dict)
      except TypeError:
          print(f"The card {card.get('name')} was missing an expected value. Skipping!")
          continue
  return cards

def get_card_info(color_code):
    cards = []

    url = f"https://api.scryfall.com/cards/search?q=color%3D{color_code}%28rarity%3Ar+OR+rarity%3Am%29"
    response = requests.get(url).json()
    data = response.get("data")
    for card in extract_card_details(data):
        cards.append(card)
    while response.get('has_more'):
        response = requests.get(response.get('next_page')).json()
        for card in extract_card_details(response.get('data')):
            cards.append(card)
    return cards

def generate_card_csv(color_code='W'):
    for color_code in MTGCodes().get_color_codes():
        csv_file_path = f"{pathlib.Path(__file__).parent.absolute()}/magic_card_csv_files_by_color/{color_code}.csv"
        cards = get_card_info(color_code)
        print(cards)
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
        with open(csv_file_path, 'a') as mycsv:
            mycsv.write('name,cmc,release_year,price,color,image\n')
            for card in cards:
                print(card)
                mycsv.write(f"{card['name']},{card['cmc']},{card['release_year']},{card['price']},{MTGCodes().encode_color(card['colors'])},{card['image_uri']}\n")
        print(f"Generated csv data for set: {color_code}")

def git_commit_and_push():
    os.system('git add *')
    os.system('git commit -m iterating')
    os.system('git push')

for color_code in MTGCodes().get_color_codes():
    generate_card_csv(color_code)
git_commit_and_push()

#for color_code in MTGCodes().get_color_codes():
    #pandas_implementation(color_code)
