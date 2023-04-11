import logging
import pathlib
import os
import requests
import time

from codes import MTGCodes

class ScryfallScraper:
    def __init__(self):
        self.mtg_color_codes = MTGCodes().get_color_codes()
        self.mtg_set_codes = MTGCodes().get_set_codes()
        self.requests_timeout_seconds = 60

    def api_rate_limiter(self, delay_in_milliseconds=100):
        # Scryfall kindly requests that API users add 50-100ms delay between calls https://scryfall.com/docs/api
        time.sleep(delay_in_milliseconds / 1000)

    def extract_card_data(self, card_data_json_list):
        if card_data_json_list is None or card_data_json_list[0] is None:
            return None
        cards = []
        for card_data_json in card_data_json_list:
            for card in card_data_json:
                card_attributes = {}
                try:
                    # Replace the commas in name to adhere to csv delimeter
                    card_attributes["name"] = card.get("name").replace(',', '-')
                    card_attributes["cmc"] = int(card.get("cmc"))
                    card_attributes["release_year"] = int(card.get("released_at").split('-')[0])
                    card_attributes["price"] = float(card.get("prices").get("usd"))
                    card_attributes["color"] = MTGCodes().encode_color(card.get("color_identity"))
                    card_attributes["type_line"] = card.get("type_line")
                    card_attributes["artist"] = card.get("artist")
                    # If the card is missing image_uris, give a harcoded image uri matching its color
                    try:
                        card_attributes["image"] = card.get("image_uris").get("normal")
                    except AttributeError as exc:
                        logging.debug(exc)
                        card_attributes["image"] = MTGCodes().encode_default_image_for_color(card_attributes["color"])
                    cards.append(card_attributes)
                except TypeError:
                    logging.debug(f"The card {card.get('name')} was missing an expected value. Skipping!")
                    continue
        return cards

    def generate_local_csv(self, set_or_color_code : str):
        base_path = pathlib.Path(__file__).parent.absolute()
        if set_or_color_code in self.mtg_color_codes:
            csv_file_path = f"{base_path}/magic_card_csv_files_by_color/{set_or_color_code}.csv"
            card_data = self.query_card_color_data(set_or_color_code)
        else:
            csv_file_path = f"{base_path}/magic_card_csv_files_by_set/{set_or_color_code}.csv"
            card_data = self.query_card_set_data(set_or_color_code)
        cards = self.extract_card_data(card_data)
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
        if cards is not None:
            with open(csv_file_path, 'a', encoding="utf-8") as local_csv_file:
                local_csv_file.write('name,cmc,release_year,price,color,image,type_line,artist\n')
                for card in cards:
                    # TODO: break out into multiple lines
                    local_csv_file.write(f"{card['name']},{card['cmc']},{card['release_year']},{card['price']},{card['color']},{card['image']},{card['type_line']},{card['artist']}\n")
            logging.info(f"Completed csv data generation for: {set_or_color_code}")

    def populate_all_local_csv(self):
        logging.basicConfig(level=logging.INFO)
        for mtg_set_code in self.mtg_set_codes:
            self.generate_local_csv(mtg_set_code)
            self.api_rate_limiter()
        for mtg_color_code in self.mtg_color_codes:
            logging.info(f"Generating csv data for {mtg_color_code}")
            self.generate_local_csv(mtg_color_code)

    def query_card_color_data(self, color_code : str):
        url = f"https://api.scryfall.com/cards/search?q=color%3D{color_code}%28rarity%3Ar+OR+rarity%3Am%29"
        response = requests.get(
            url,
            timeout=self.requests_timeout_seconds
        ).json()
        card_data = [response.get("data")]
        page_count = 1
        while response.get('has_more'):
            response = requests.get(
                response.get('next_page'),
                timeout=self.requests_timeout_seconds
            ).json()
            card_data.append(response.get("data"))
            logging.info(f"Appended page {page_count} for color {color_code}")
            page_count += 1
            self.api_rate_limiter()
        if not card_data or not card_data[0]:
            logging.warning(f"color_code {color_code} didn't return results")
            return None
        return card_data

    def query_card_set_data(self, set_code : str):
        url = f"https://api.scryfall.com/cards/search?q=set%3A{set_code}+%28rarity%3Ar+OR+rarity%3Am%29"
        response = requests.get(
            url,
            timeout=self.requests_timeout_seconds
        ).json()
        # Making card_data a single element list is unnecessary but matches paginated color design
        # This allows extract_card_data to be identical for each
        card_data = [response.get("data")]
        if not card_data or not card_data[0]:
            logging.warning(f"set_code {set_code} didn't return results")
            return None
        return card_data
