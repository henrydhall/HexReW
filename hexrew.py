"""Some utilities for messing around with hexadecimal files."""

def read_file(file_name) -> list:
    """Read a file and return it as a list."""
    with open(file_name, 'rb') as rf:
        rf = rf.read()
        hex_list = [int(c) for c in rf]
    return hex_list


def get_word(hex_list, offset) -> list[int]:
    return hex_list[offset:offset+4:]


def get_byte(hex_list, offset) -> int:
    return hex_list[offset]


def hex_to_int(hex_word) -> int:
    return int(''.join( [hex(byte).replace('0x','') for byte in hex_word[-1::-1]] ), base=16)


def create_file(filename, contents):
    with open(filename,mode='xb') as wf:
        contents = bytearray(contents)
        wf.write(contents)


def over_write_file(filename, contents: int):
    with open(filename,'wb') as wf:
        contents = bytearray(contents)
        wf.write(contents)


def set_byte(bytes, offset, value):
    raise NotImplementedError('TODO: set_byte')


if __name__ == '__main__':
    my_bytes = read_file('user1.dat')
    my_bytes[0] = 0x0D
    over_write_file('hello.dat',my_bytes)
