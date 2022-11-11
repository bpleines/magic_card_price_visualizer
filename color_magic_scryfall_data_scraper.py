import pathlib
import requests
import os

from codes import MTGCodes

def extract_card_details(card_list):
  cards = []
  for card in card_list:
    card_dict = {}
    try:
      # Replace the commas in name to adhere to csv delimeter
      card_dict["name"] = card.get("name").replace(',', '-')
      card_dict["cmc"] = int(card.get("cmc"))
      card_dict["release_year"] = int(card.get("release_year"))
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

# This not a scalable implementation and should be fixed in the future.
# Ideally the pagination should be evaluated recursively, such that as new cards are added over time
# the pagation is computed automatically without having to add extra code.
def get_card_info(color_code):
  url = f"https://api.scryfall.com/cards/search?q=color%3D{color_code}%28rarity%3Ar+OR+rarity%3Am%29"
  response = requests.get(url).json()
  cards = []
  cards.append(extract_card_details(response.get("data")))
  while response.get('has_more'):
    response = requests.get(response.get('next_page')).json()
    next_page_cards = extract_card_details(response.get("data"))
    cards.append(next_page_cards)
  return cards

def generate_card_csv(color_code='W'):
  for color_code in MTGCodes().get_color_codes():
    csv_file_path = f"{pathlib.Path(__file__).parent.absolute()}/magic_card_csv_files_by_color/{color_code}.csv"
    cards = get_card_info(color_code)
    if os.path.exists(csv_file_path):
      os.remove(csv_file_path)
    with open(csv_file_path, 'a') as mycsv:
      mycsv.write('name,cmc,release_year,price,color,image\n')
      for card in cards:
        mycsv.write(f"{card['name']},{card['cmc']},{card['release_year']},{card['price']},{MTGCodes().encode_color(card['colors'])},{card['image_uri']}\n")
  print(f"Generated csv data for set: {color_code}")

def git_commit_and_push():
  os.system('git add *')
  os.system('git commit -m iterating')
  os.system('git push')

for color_code in MTGCodes().get_color_codes():
  generate_card_csv(color_code)
git_commit_and_push()
