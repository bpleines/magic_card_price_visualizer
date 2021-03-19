import matplotlib.pyplot as plt
import requests
import os.path
from os import path

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
     print(color[0]) 
     return color_map[color[0]]

def get_card_info(set_code):
  url = 'https://api.scryfall.com/cards/search?q=set%3A' + set_code + '+%28rarity%3Ar+OR+rarity%3Am%29'
  response = requests.get(url).json().get("data")
  cards = []
  for card in response:
    card_dict = {}
    card_dict["name"] = card.get("name")
    card_dict["cmc"] = int(card.get("cmc"))
    card_dict["price"] = float(card.get("prices").get("usd"))
    card_dict["colors"] = card.get("color_identity")
    cards.append(card_dict)
  return cards

'''
def generate_scatterplot(set_code='ZNR'):
  sorted_cards_by_price = sorted(get_card_info(set_code), key = lambda i: i['price'])
  fig, ax = plt.subplots()
  for color in ['red', 'white', 'green', 'blue', 'black']:
    on_color_cards = [ card for card in sorted_cards_by_price if encode_color(color) in card["colors"] ]
    x = [ card['cmc'] for card in on_color_cards ]
    y = [ card['price'] for card in on_color_cards ] 
    scale = 100.0
    ax.scatter(x, y, c=color, s=scale, label=color,
               alpha=0.4, edgecolors='black')

  ax.set_xlabel('Converted Mana Cost (cmc)', fontsize=15)
  ax.set_ylabel('Price of Card ($)', fontsize=15)
  ax.set_title('Magic the Gathering Rares (' + set_code + ') : Price by Mana Cost and Color')
  ax.legend()
  ax.grid(True)
  plt.show()
'''

# Some other interesting codes: RAV, 2XM, IKO
# generate_scatterplot('CHK')
def generate_card_csv(csv_file_path='/Users/bpleines/dataVisualization/finalProject/data_vis/magiccards.csv'):
  cards = get_card_info('ZNR')
  if os.path.exists(csv_file_path):
    os.remove(csv_file_path)  
  with open(csv_file_path, 'a') as mycsv:
    mycsv.write('cmc,price,color\n')
    for card in cards:
      mycsv.write(str(card["cmc"]) + "," + str(card["price"]) + ',' + str(encode_color(card["colors"])) + '\n' )
  os.system('git add *')
  os.system('git commit -m iterating')
  os.system('git push')

generate_card_csv()
