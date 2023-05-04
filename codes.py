#!/usr/bin/env python
import requests


class MTGCodes:
    """Class to store set and color codes"""

    def __init__(self):
        self.requests_timeout_seconds = 600

    def encode_color(self, color):
        # Handle colorless case
        if len(color) == 0:
            return "#8c8d8b"
        # Handle multicolored case
        if len(color) >= 2:
            return "#d78f42"
        color_map = {
            "R": "#ff1a1a",
            "W": "#ffffff",
            "U": "#341aff",
            "B": "#000000",
            "G": "#087500",
        }
        return color_map[color[0]]

    def encode_default_image_for_color(self, color):
        # Handle colorless case
        if len(color) == 0:
            return "https://cards.scryfall.io/normal/front/6/9/69b215fe-0d97-4ca1-9490-174220fd454b.jpg?1562916234"
        # Handle multicolored case
        if len(color) >= 2:
            return "https://cards.scryfall.io/normal/front/f/4/f410ae1c-02de-423e-a478-e1dea243ef1e.jpg?1619395458"
        color_map = {
            "R": "https://cards.scryfall.io/normal/front/5/3/53fb7b99-9e47-46a6-9c8a-88e28b5197f1.jpg?1641306121",
            "W": "https://cards.scryfall.io/normal/front/a/9/a9891b7b-fc52-470c-9f74-292ae665f378.jpg?1641306232",
            "U": "https://cards.scryfall.io/normal/front/a/c/acf7b664-3e75-4018-81f6-2a14ab59f258.jpg?1641306192",
            "B": "https://cards.scryfall.io/normal/front/0/2/02cb5cfd-018e-4c5e-bef1-166262aa5f1d.jpg?1641306156",
            "G": "https://cards.scryfall.io/normal/front/3/2/32af9f41-89e2-4e7a-9fec-fffe79cae077.jpg?1641306082",
        }
        return color_map[color[0]]

    def get_color_codes(self):
        return ["W", "U", "B", "R", "G"]

    def get_set_codes(self):
        url = "https://api.scryfall.com/sets"
        response = (
            requests.get(url, timeout=self.requests_timeout_seconds).json().get("data")
        )
        return [set_record["code"].upper() for set_record in response]
