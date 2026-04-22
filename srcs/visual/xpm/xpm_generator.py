def create_xpm_title(text: str, filename: str, size: int) -> None:
    """
    create a xpm file with a given word and given size
    """
    chars = {"A": [" AAA ", "A   A", "AAAAA", "A   A", "A   A"],
             "M": ["M   M", "MM MM", "M M M", "M   M", "M   M"],
             "Z": ["ZZZZZ", "   Z ", "  Z  ", " Z   ", "ZZZZZ"],
             "E": ["EEEEE", "E    ", "EEE  ", "E    ", "EEEEE"],
             "I": ["IIIII", "  I  ", "  I  ", "  I  ", "IIIII"],
             "N": ["N   N", "NN  N", "N N N", "N  NN", "N   N"],
             "G": ["GGGGG", "G    ", "G  GG", "G   G", "GGGGG"],
             "-": ["     ", "     ", " --- ", "     ", "     "],
             "C": [" CCCC", "C    ", "C    ", "C    ", " CCCC"],
             "O": [" OOO ", "O   O", "O   O", "O   O", " OOO "],
             "D": ["DDD  ", "D  D ", "D   D", "D  D ", "DDD  "],
             "S": [" SSS ", "S    ", " SSS ", "    S", " SSS "]}
    word = text.upper()
    height = 5
    width = len(text) * 6
    if word == "COMMANDS":
        color = "4682B4"
    else:
        color = "D2042D"
    with open(filename, "w") as f:
        f.write("/* XPM */\n")
        f.write("static char * amazing_xpm[] = {\n")
        f.write(f"\"{width * size} {height * size} 2 1\",\n")
        f.write("\"  c #000000\",\n")
        f.write(f"\"X c #{color}\",\n")
        for i in range(height):
            for _ in range(size):
                line = "\""
                for char in word:
                    for byte in chars[char][i]:
                        byte = "X" if byte == char else byte
                        line += byte * size
                    line += " " * size
                line += "\",\n"
                f.write(line)
        f.write("};")
