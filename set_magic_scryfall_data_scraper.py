import pathlib
import requests
import os

from codes import MTGCodes

mtg_set_codes = MTGCodes().get_set_codes()

def get_card_info(set_code):
    url = f"https://api.scryfall.com/cards/search?q=set%3A{set_code}+%28rarity%3Ar+OR+rarity%3Am%29"
    response = requests.get(url).json().get("data")
    if not response:
        raise Exception(f"set_code {set_code} didn't return any results. Maybe there is a typo?")
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
            # If the card is missing image_uris, give a harcoded photo matching its color
            try:
                card_dict["image_uri"] = card.get("image_uris").get("normal")
            except AttributeError as e:
                card_dict["image_uri"] = MTGCodes().encode_default_image_for_color(card_dict["colors"])
            cards.append(card_dict)
        except TypeError:
            print(f"The card {card.get('name')} was missing an expected value. Skipping!")
            continue
    return cards

def generate_card_csv(set_code=mtg_set_codes[0]):
    csv_file_path = f"{pathlib.Path(__file__).parent.absolute()}/magic_card_csv_files_by_set/{set_code}.csv"
    cards = get_card_info(set_code)
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
    with open(csv_file_path, 'a') as mycsv:
        mycsv.write('name,cmc,release_year,price,color,image\n')
        for card in cards:
            mycsv.write(f"{card['name']},{card['cmc']},{card['release_year']},{card['price']},{MTGCodes().encode_color(card['colors'])},{card['image_uri']}\n")
    print(f"Generated csv data for set: {set_code}")

# TODO: this is a sloppy way of making this work
# Instead find an efficent way to load locally
def git_commit_and_push():
    os.system('git add *')
    os.system('git commit -m iterating')
    os.system('git push')

for set_code in mtg_set_codes:
    generate_card_csv(set_code)
git_commit_and_push()
