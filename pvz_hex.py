"""Some stuff for messing around with a Plants vs. Zombies save file."""

import hexrew
import pvz_const


if __name__ == '__main__':
    file = hexrew.read_file('user1.dat')
    word = hexrew.get_word(file, pvz_const.MONEY)
    print('Money:',10*hexrew.hex_to_int(hexrew.get_word(file, pvz_const.MONEY)))
    print('Level:', hexrew.hex_to_int(hexrew.get_word(file, pvz_const.CURRENT_LEVEL) ))
    print('Adventure completions:', hexrew.hex_to_int(hexrew.get_word(file, pvz_const.ADVENTURE_MODE) ))
    print('Zen Garden Plants:', hexrew.hex_to_int(hexrew.get_word(file, pvz_const.ZEN_GARDEN_COUNT) ))
    print()
    current_plant = pvz_const.FIRST_PLANT
    while current_plant < len(file):
        print( pvz_const.PLANTS[(hexrew.hex_to_int(hexrew.get_word(file, current_plant) ))])
        print( (hexrew.hex_to_int(hexrew.get_word(file, current_plant + pvz_const.GARDEN_LOCATION))))
        current_plant += pvz_const.PLANT_SIZE
