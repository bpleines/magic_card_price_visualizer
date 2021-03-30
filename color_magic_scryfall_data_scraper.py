import requests
import os

mtg_color_codes = ['W', 'U', 'B', 'R', 'G']
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

def extract_card_details(card_list):
  cards = []
  for card in card_list:
    card_dict = {}
    try:
      # Replace the commas in name to adhere to csv delimeter
      card_dict["name"] = card.get("name").replace(',', '-')
      card_dict["cmc"] = int(card.get("cmc"))
      card_dict["price"] = float(card.get("prices").get("usd"))
      card_dict["colors"] = card.get("color_identity")
      cards.append(card_dict)
    except TypeError:
      print("The card " + card.get("name") + " was missing an expected value. Skipping!")
      continue
  return cards

#def dig_into_pagination(response, total_cards):
#  if response.get('has_more') == False:
#    return total_cards
#  else:
#    next_page_url = response.get('next_page')
#    new_response = requests.get(next_page_url).json()
#    new_cards = extract_card_details(new_response.get("data"))
#    new_total_cards = total_cards + new_cards
#    print("Extracted url: " + next_page_url)
#    dig_into_pagination(new_response, new_total_cards)


def get_card_info(color_code):
  url = 'https://api.scryfall.com/cards/search?q=color%3D' + color_code + '+%28rarity%3Ar+OR+rarity%3Am%29' 
  response = requests.get(url).json()
  first_page_cards = extract_card_details(response.get("data"))
  if response.get('has_more'):
    new_response = requests.get(response.get('next_page')).json()
    second_page_cards = extract_card_details(new_response.get("data"))
  return first_page_cards + second_page_cards

def generate_card_csv(color_code='W'):
  for set_code in mtg_set_codes:
    csv_file_path= '/Users/bpleines/dataVisualization/finalProject/data_vis/magic_card_csv_files_by_color/' + color_code + '.csv'
    cards = get_card_info(color_code)
    if os.path.exists(csv_file_path):
      os.remove(csv_file_path)  
    with open(csv_file_path, 'a') as mycsv:
      mycsv.write('name,cmc,price,color\n')
      for card in cards:
        mycsv.write(str(card["name"]) + "," +
                    str(card["cmc"]) + "," +
                    str(card["price"]) + ',' +
                    str(encode_color(card["colors"])) + '\n' )
  print("Generated csv data for set: " + color_code)

def git_commit_and_push():
  os.system('git add *')
  os.system('git commit -m iterating')
  os.system('git push')

for color_code in mtg_color_codes:
  generate_card_csv(color_code)
git_commit_and_push()
