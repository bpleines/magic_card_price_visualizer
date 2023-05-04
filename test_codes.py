import unittest

from codes import MTGCodes


class TestMTGCodes(unittest.TestCase):
    codes = MTGCodes()

    def test_encode_color(self):
        self.assertTrue(self.codes.encode_color("") == "#8c8d8b")
        self.assertTrue(self.codes.encode_color("WU") == "#d78f42")
        self.assertTrue(self.codes.encode_color("RBG") == "#d78f42")
        self.assertTrue(self.codes.encode_color("W") == "#ffffff")
        self.assertTrue(self.codes.encode_color("U") == "#341aff")
        self.assertTrue(self.codes.encode_color("R") == "#ff1a1a")
        self.assertTrue(self.codes.encode_color("B") == "#000000")
        self.assertTrue(self.codes.encode_color("G") == "#087500")

    def test_encode_default_image_for_color(self):
        self.assertTrue(
            self.codes.encode_default_image_for_color("")
            == "https://cards.scryfall.io/normal/front/6/9/69b215fe-0d97-4ca1-9490-174220fd454b.jpg?1562916234"
        )
        self.assertTrue(
            self.codes.encode_default_image_for_color("WU")
            == "https://cards.scryfall.io/normal/front/f/4/f410ae1c-02de-423e-a478-e1dea243ef1e.jpg?1619395458"
        )
        self.assertTrue(
            self.codes.encode_default_image_for_color("RBG")
            == "https://cards.scryfall.io/normal/front/f/4/f410ae1c-02de-423e-a478-e1dea243ef1e.jpg?1619395458"
        )
        self.assertTrue(
            self.codes.encode_default_image_for_color("W")
            == "https://cards.scryfall.io/normal/front/a/9/a9891b7b-fc52-470c-9f74-292ae665f378.jpg?1641306232"
        )
        self.assertTrue(
            self.codes.encode_default_image_for_color("U")
            == "https://cards.scryfall.io/normal/front/a/c/acf7b664-3e75-4018-81f6-2a14ab59f258.jpg?1641306192"
        )
        self.assertTrue(
            self.codes.encode_default_image_for_color("R")
            == "https://cards.scryfall.io/normal/front/5/3/53fb7b99-9e47-46a6-9c8a-88e28b5197f1.jpg?1641306121"
        )
        self.assertTrue(
            self.codes.encode_default_image_for_color("B")
            == "https://cards.scryfall.io/normal/front/0/2/02cb5cfd-018e-4c5e-bef1-166262aa5f1d.jpg?1641306156"
        )
        self.assertTrue(
            self.codes.encode_default_image_for_color("G")
            == "https://cards.scryfall.io/normal/front/3/2/32af9f41-89e2-4e7a-9fec-fffe79cae077.jpg?1641306082"
        )

    def test_get_set_codes(self):
        set_codes = self.codes.get_set_codes()
        self.assertTrue(set_codes is not None)
        self.assertTrue("CHK" in set_codes)
        self.assertTrue(len(set_codes) > 1)


if __name__ == "__main__":
    unittest.main()
