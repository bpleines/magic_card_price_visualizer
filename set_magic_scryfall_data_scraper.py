import pathlib
import requests
import os

mtg_set_codes = ['STX', 'KHM', 'ZNR', 'IKO', 'THB', 'ELD', 'WAR', 'RNA', 'GRN', 'DOM', 'RIX',
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

def get_card_info(set_code):
  url = 'https://api.scryfall.com/cards/search?q=set%3A' + set_code + '+%28rarity%3Ar+OR+rarity%3Am%29'
  response = requests.get(url).json().get("data")
  cards = []
  for card in response:
    card_dict = {}
    try:
      # Replace the commas in name to adhere to csv delimeter
      card_dict["name"] = card.get("name").replace(',', '-')
      card_dict["cmc"] = int(card.get("cmc"))
      card_dict["release_year"] = int(card.get("released_at").split('-')[0])
      card_dict["price"] = float(card.get("prices").get("usd"))
      card_dict["colors"] = card.get("color_identity")
      cards.append(card_dict)
    except TypeError:
      print("The card " + card.get("name") + " was missing an expected value. Skipping!")
      continue
  return cards

def generate_card_csv(set_code='KHM'):
  csv_file_path = str(pathlib.Path(__file__).parent.absolute()) + '/magic_card_csv_files_by_set/' + set_code + '.csv'
  cards = get_card_info(set_code)
  if os.path.exists(csv_file_path):
    os.remove(csv_file_path)  
  with open(csv_file_path, 'a') as mycsv:
    mycsv.write('name,cmc,release_year,price,color\n')
    for card in cards:
      mycsv.write(str(card["name"]) + "," +
                  str(card["cmc"]) + "," +
                  str(card["release_year"]) + "," +
                  str(card["price"]) + ',' +
                  str(encode_color(card["colors"])) + '\n' )
  print("Generated csv data for set: " + set_code)

def git_commit_and_push():
  os.system('git add *')
  os.system('git commit -m iterating')
  os.system('git push')

for set_code in mtg_set_codes:
  generate_card_csv(set_code)
#git_commit_and_push()
