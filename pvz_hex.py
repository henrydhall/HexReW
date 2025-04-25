"""Some stuff for messing around with a Plants vs. Zombies save file."""

from collections import defaultdict

import hexrew
import pvz_const


class PvZParser:
    """Plants vs. Zombies save file parser."""

    def __init__(self, save_file):
        self.file = hexrew.read_file(save_file)
        self.plants = self.get_plants()

    def get_money(self):
        """Return the amount of money in the save."""
        return 10 * hexrew.hex_to_int(hexrew.get_word(self.file, pvz_const.MONEY))

    def get_level(self):
        """Get the current level."""
        return hexrew.hex_to_int(hexrew.get_word(self.file, pvz_const.CURRENT_LEVEL))

    def get_attribute(self, attribute):
        """Get the attribute."""
        return self.file[attribute]

    def get_plant_attribute(self, n, attribute):
        """Get the attribute of a plant."""
        return self.file[attribute + pvz_const.FIRST_PLANT + (pvz_const.PLANT_SIZE * n)]

    def get_plant(self, n) -> str:
        """Get the nth plant."""
        return pvz_const.PLANTS[self.get_attribute(pvz_const.FIRST_PLANT + (pvz_const.PLANT_SIZE * n))]

    def get_plant_garden(self, n) -> str:
        """Get the nth plant's garden as a str."""
        return pvz_const.GARDENS[
            self.get_attribute(pvz_const.GARDEN_LOCATION + pvz_const.FIRST_PLANT + (pvz_const.PLANT_SIZE * n))
        ]

    def get_plant_direction(self, n) -> str:
        """Get the nth plant's direction as a str."""
        return pvz_const.DIRECTIONS[
            self.get_attribute(pvz_const.FACING + pvz_const.FIRST_PLANT + (pvz_const.PLANT_SIZE * n))
        ]

    def get_plant_location(self, n) -> tuple:
        """Get the column and row or placement of the nth plant."""
        if self.get_plant_garden(n) == 'Zen Garden':
            return (self.get_plant_attribute(n, pvz_const.COLUMN), self.get_plant_attribute(n, pvz_const.ROW))
        else:
            return (self.get_plant_attribute(n, pvz_const.COLUMN),)

    def max_money(self) -> None:
        """Set money to max displayable amount. 0x0001869f"""
        self.file[pvz_const.MONEY] = 0x9F
        self.file[pvz_const.MONEY + 1] = 0x86
        self.file[pvz_const.MONEY + 2] = 0x01
        self.file[pvz_const.MONEY + 3] = 0x00

    def create_save_file(self, file_name):
        """Write self.file to file_name."""
        hexrew.create_file(file_name, self.file)

    def write_save_file(self, file_name) -> None:
        """Overwrite save file."""
        hexrew.over_write_file(file_name, self.file)

    def get_blank_space(self) -> tuple:
        """Get a free space in the Zen Garden"""
        new_pos = None
        for i in range(0, 8):
            for j in range(0, 4):
                if (i, j) not in self.plants:
                    return (i, j)
        else:
            raise IndexError('No free space in Zen Garden')

    def new_plant(self, plant_type, aquatic=False) -> None:
        """Put in a new plant in a new place."""
        new_bytes = [0 for i in range(0, 0x58)]

        new_pos = self.get_blank_space()

        new_bytes[0] = plant_type
        new_bytes[pvz_const.COLUMN] = new_pos[0]
        new_bytes[pvz_const.ROW] = new_pos[1]
        new_bytes[pvz_const.FERTILIZED_COUNT] = 1
        if not aquatic:
            new_bytes[pvz_const.WATER_REQUIREMENT] = 3
        self.file.extend(new_bytes)
        self.file[pvz_const.ZEN_GARDEN_COUNT] = self.file[pvz_const.ZEN_GARDEN_COUNT] + 1

        self.plants = self.get_plants()

    def get_plants(self) -> dict[tuple]:
        """Make a dictionary of the plants."""
        plants = defaultdict(int)
        for i in range(self.get_attribute(pvz_const.ZEN_GARDEN_COUNT)):
            plants[self.get_plant_location(i)] = self.get_plant(i)
        return plants


if __name__ == '__main__':
    my_parser = PvZParser('user1.dat')
    print('Money:', my_parser.get_money())
    print('Level:', my_parser.get_level())
    print('Adventure Completions:', my_parser.get_attribute(pvz_const.ADVENTURE_MODE))
    print('Zen Garden Plants:', my_parser.get_attribute(pvz_const.ZEN_GARDEN_COUNT))
    print()
    for i in range(my_parser.get_attribute(pvz_const.ZEN_GARDEN_COUNT)):
        print(
            my_parser.get_plant(i) + ':',
            my_parser.get_plant_garden(i),
            my_parser.get_plant_direction(i),
            my_parser.get_plant_location(i),
            my_parser.get_plant_attribute(i, pvz_const.FERTILIZED_COUNT),
        )
    my_parser.max_money()
    my_parser.new_plant(0x0F)
    my_parser.new_plant(0x30)
    my_parser.new_plant(0x2F)
    my_parser.new_plant(0x32)
    my_parser.new_plant(0x21)
    my_parser.new_plant(0x31)
    my_parser.new_plant(0x10, True)

    my_parser.write_save_file('new.dat')
