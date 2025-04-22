"""Some stuff for messing around with a Plants vs. Zombies save file."""

import hexrew
import pvz_const


class PvZParser:
    """Plants vs. Zombies save file parser."""

    def __init__(self, save_file):
        self.file = hexrew.read_file(save_file)

    def get_money(self):
        """Return the amount of money in the save."""
        return 10 * hexrew.hex_to_int(hexrew.get_word(self.file, pvz_const.MONEY))

    def get_level(self):
        """Get the current level."""
        return hexrew.hex_to_int(hexrew.get_word(self.file, pvz_const.CURRENT_LEVEL))

    def get_attribute(self, attribute):
        """Get the attribute."""
        return self.file[attribute]

    def get_plant(self, n) -> str:
        """Get the nth plant."""
        return pvz_const.PLANTS[self.get_attribute(pvz_const.FIRST_PLANT + (pvz_const.PLANT_SIZE * n))]

    def get_plant_garden(self, n) -> str:
        """Get the nth plant's garden as a str."""
        return pvz_const.GARDENS[
            self.get_attribute(pvz_const.GARDEN_LOCATION + pvz_const.FIRST_PLANT + (pvz_const.PLANT_SIZE * n))
        ]


if __name__ == '__main__':
    my_parser = PvZParser('user1.dat')
    print('Money:', my_parser.get_money())
    print('Level:', my_parser.get_level())
    print('Adventure Completions:', my_parser.get_attribute(pvz_const.ADVENTURE_MODE))
    print('Zen Garden Plants:', my_parser.get_attribute(pvz_const.ZEN_GARDEN_COUNT))
    print()
    for i in range(my_parser.get_attribute(pvz_const.ZEN_GARDEN_COUNT)):
        print(my_parser.get_plant(i) + ':', my_parser.get_plant_garden(i))
