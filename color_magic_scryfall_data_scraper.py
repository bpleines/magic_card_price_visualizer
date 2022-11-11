import pathlib
import requests
import os

mtg_color_codes = ['W', 'U', 'B', 'R', 'G']
mtg_set_codes = ['BRO', 'DMU', 'SNC', 'NEO', 'VOW', 'MID', 'AFR',
                 'STX', 'KHM', 'ZNR', 'IKO', 'THB', 'ELD', 'WAR', 'RNA', 'GRN', 'DOM', 'RIX',
                 'XLN', 'HOU', 'AKH', 'AER', 'KLD', 'EMN', 'SOI', 'OGW', 'BFZ', 'DTK', 'FRF',
                 'KTK', 'JOU', 'BNG', 'THS', 'DGM', 'GTC', 'RTR', 'AVR', 'DKA', 'ISD', 'NPH',
                 'MBS', 'SOM', 'ROE', 'WWK', 'ZEN', 'ARB', 'CON', 'ALA', 'EVE', 'SHM', 'MOR',
                 'LRW', 'FUT', 'PLC', 'TSP', 'CSP', 'DIS', 'GPT', 'RAV', 'SOK', 'BOK', 'CHK',
                 '5DN', 'DST', 'MRD', 'SCG', 'LGN', 'ONS', 'JUD', 'TOR', 'ODY', 'APC', 'PLS',
                 'INV', 'PCY', 'NEM', 'MMQ', 'UDS', 'ULG', 'USG', 'EXO', 'STH', 'TMP', 'WTH',
                 'VIS', 'MIR', 'ALL', 'HML', 'ICE', 'FEM', 'DRK', 'LEG', 'ATQ', 'ARN']

def encode_color(color):
   # Handle colorless case
   if len(color) == 0:
     return '#8c8d8b'
   elif len(color) >= 2:
     return '#d78f42'
   else:
     color_map = {
       "R": "#ff1a1a",
       "W": "#ffffff",
       "U": "#341aff",
       "B": "#000000",
       "G": "#087500"
     }
     return color_map[color[0]]

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
  first_page_cards = extract_card_details(response.get("data"))
  if response.get('has_more'):
    second_response = requests.get(response.get('next_page')).json()
    second_page_cards = extract_card_details(second_response.get("data"))
    if second_response.get('has_more'):
      third_response = requests.get(second_response.get('next_page')).json()
      third_page_cards = extract_card_details(third_response.get("data"))
      if third_response.get('has_more'):
        fourth_response = requests.get(third_response.get('next_page')).json()
        fourth_page_cards = extract_card_details(fourth_response.get("data"))
        if fourth_response.get('has_more'):
          fifth_response = requests.get(fourth_response.get('next_page')).json()
          fifth_page_cards = extract_card_details(fifth_response.get("data"))
          if fifth_response.get('has_more'):
            sixth_response = requests.get(fifth_response.get('next_page')).json()
            sixth_page_cards = extract_card_details(sixth_response.get("data"))
            if sixth_response.get('has_more'):
              seventh_response = requests.get(sixth_response.get('next_page')).json()
              seventh_page_cards = extract_card_details(seventh_response.get("data"))
  return first_page_cards + second_page_cards + third_page_cards + fourth_page_cards + fifth_page_cards + sixth_page_cards

def generate_card_csv(color_code='W'):
  for set_code in mtg_set_codes:
    csv_file_path = f"{pathlib.Path(__file__).parent.absolute()}/magic_card_csv_files_by_color/{color_code}.csv"
    cards = get_card_info(color_code)
    if os.path.exists(csv_file_path):
      os.remove(csv_file_path)
    with open(csv_file_path, 'a') as mycsv:
      mycsv.write('name,cmc,release_year,price,color,image\n')
      for card in cards:
        mycsv.write(f"{name},{cmc},{release_year},{price},{color},{image}\n")
  print("Generated csv data for set: " + color_code)

def git_commit_and_push():
  os.system('git add *')
  os.system('git commit -m iterating')
  os.system('git push')

for color_code in mtg_color_codes:
  generate_card_csv(color_code)
git_commit_and_push()
