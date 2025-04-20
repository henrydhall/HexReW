"""Some stuff for messing around with a Plants vs. Zombies save file."""

# TODO: refactor above, rest of the offsets from garden location on

import hexrew
from pvz_const import *


if __name__ == '__main__':
    file = hexrew.read_file('user1.dat')
    word = hexrew.get_word(file,MONEY)
    #print( ''.join( [hex(byte) for byte in word] ) )
    print('Money:',10*hexrew.hex_to_int(hexrew.get_word(file, MONEY)))
    print('Level:', hexrew.hex_to_int(hexrew.get_word(file, CURRENT_LEVEL) ))
    print('Adventure completions:', hexrew.hex_to_int(hexrew.get_word(file, ADVENTURE_MODE) ))
    print('Zen Garden Plants:', hexrew.hex_to_int(hexrew.get_word(file, ZEN_GARDEN_COUNT) ))
    print(hexrew.hex_to_int(hexrew.get_word(file, FIRST_PLANT) ) == MARIGOLD)
    # TODO: figure out how we want to structure plant constants, print out all that info.
