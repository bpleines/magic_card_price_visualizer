import logging
import pathlib
import os
import requests

from codes import MTGCodes

class ScryfallScraper:
    def __init__(self):
        self.mtg_set_codes = MTGCodes().get_set_codes()
        self.requests_timeout_seconds = 60

    def get_card_data(self, set_code : str):
        cards = []
        url = f"https://api.scryfall.com/cards/search?q=set%3A{set_code}+%28rarity%3Ar+OR+rarity%3Am%29"
        response = requests.get(
            url,
            timeout=self.requests_timeout_seconds
        ).json()
        card_data = response.get("data")
        if not card_data:
            logging.warning(f"set_code {set_code} didn't return results")
            return None
        for card in card_data:
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
                # If the card is missing image_uris, give a harcoded image uri matching its color
                try:
                    card_dict["image"] = card.get("image_uris").get("normal")
                except AttributeError as exc:
                    logging.debug(exc)
                    card_dict["image"] = MTGCodes().encode_default_image_for_color(card_dict["color"])
                cards.append(card_dict)
            except TypeError:
                logging.debug(f"The card {card.get('name')} was missing an expected value. Skipping!")
                continue
        return cards

    def generate_local_csv(self, set_code : str):
        csv_file_path = f"{pathlib.Path(__file__).parent.absolute()}/magic_card_csv_files_by_set/{set_code}.csv"
        cards = self.get_card_data(set_code)
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
            return
        if cards is not None:
            with open(csv_file_path, 'a', encoding="utf-8") as local_csv_file:
                local_csv_file.write('name,cmc,release_year,price,color,image,type_line,artist\n')
                for card in cards:
                    local_csv_file.write(f"{card['name']},{card['cmc']},{card['release_year']},{card['price']},{card['color']},{card['image']},{card['type_line']},{card['artist']}\n")
            logging.info(f"Generated csv data for set: {set_code}")

    def populate_all_local_csv(self):
        logging.basicConfig(level=logging.INFO)
        for mtg_set_code in self.mtg_set_codes:
            self.generate_local_csv(mtg_set_code)
