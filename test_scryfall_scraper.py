import unittest

from scryfall_scraper import ScryfallScraper


class TestScryfallScraper(unittest.TestCase):
    scraper = ScryfallScraper()

    def test_extract_card_data(self):
        card_data = self.scraper.query_card_set_data("CHK")
        cards = self.scraper.extract_card_data(card_data)
        single_card = cards[0]
        # This below tests on name confirm delimiter replacement for writing as csv file
        self.assertFalse(
            single_card["name"] == "Akki Lavarunner // Tok-Tok, Volcano Born"
        )
        self.assertTrue(
            single_card["name"] == "Akki Lavarunner // Tok-Tok- Volcano Born"
        )
        self.assertTrue(single_card["cmc"] == 4)
        self.assertTrue(single_card["release_year"] == 2004)
        self.assertTrue(single_card["color"] == "#ff1a1a")
        self.assertTrue(
            single_card["type_line"]
            == "Creature — Goblin Warrior // Legendary Creature — Goblin Shaman"
        )
        self.assertTrue(single_card["artist"] == "Matt Cavotta")

    def test_query_card_color_data(self):
        card_data = self.scraper.query_card_color_data("W")
        self.assertTrue(all(data is not None for data in card_data))
        self.assertTrue(len(card_data) > 1)

    def test_query_card_set_data(self):
        card_data = self.scraper.query_card_set_data("CHK")
        self.assertTrue(card_data[0] is not None)
        self.assertTrue(len(card_data) == 1)


if __name__ == "__main__":
    unittest.main()
