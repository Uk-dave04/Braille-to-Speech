LETTER_MAP = {
    "100000": "a",
    "110000": "b",
    "100100": "c",
    "100110": "d",
    "100010": "e",
    "110100": "f",
    "110110": "g",
    "110010": "h",
    "010100": "i",
    "010110": "j",
    "101000": "k",
    "111000": "l",
    "101100": "m",
    "101110": "n",
    "101010": "o",
    "111100": "p",
    "111110": "q",
    "111010": "r",
    "011100": "s",
    "011110": "t",
    "101001": "u",
    "111001": "v",
    "010111": "w",
    "101101": "x",
    "101111": "y",
    "101011": "z",
    "010011": ".",
    "011000": ",",
    "011001": "-",
}

NUMBER_SIGN = "001111"
SPACE_TOKEN = "SPACE"
NUMBER_MAP = {
    "100000": "1",
    "110000": "2",
    "100100": "3",
    "100110": "4",
    "100010": "5",
    "110100": "6",
    "110110": "7",
    "110010": "8",
    "010100": "9",
    "010110": "0",
}


def decode_braille_patterns(patterns: list[str]) -> str:
    decoded: list[str] = []
    number_mode = False

    for pattern in patterns:
        if pattern == SPACE_TOKEN:
            decoded.append(" ")
            number_mode = False
            continue

        if pattern == NUMBER_SIGN:
            number_mode = True
            continue

        if number_mode and pattern in NUMBER_MAP:
            decoded.append(NUMBER_MAP[pattern])
            continue

        number_mode = False
        decoded.append(LETTER_MAP.get(pattern, "?"))

    return "".join(decoded)
