import sys
from colorama import Fore, Back, Style

# Key to modding out aesthetic information

AEST_REDUCE = [ ("i", "ı"),
                ("j", "ȷ"), 
                ("", ".!?,") ]

# Key to modding out tone information

TONE_REDUCE = [ ("a", "āáäảâàãaǎ"),
                ("e", "ēéëẻêèẽeě"),
                ("i", "īíïỉîìĩıǐ"),
                ("o", "ōóöỏôòõoǒ"),
                ("u", "ūúüủûùũuǔ"),
                ("y", "ȳýÿỷŷỳỹyy̌") ]

# Particle words to take stats on

CLASSES = [

    ("SA",     ["sa", "sia", "tu", "ke", "baq", "ja", "hi", "co", "hoi"]),
    ("TO/RU",  ["to", "ru", "ra", "ro", "ri", "roi"]),

    ("JE",     ["je", "keo", "tiu"]),
    ("BI",     ["bi", "pa"]),
    ("GO",     ["fi", "go", "cu", "ta"]),
    ("DA",     ["da", "ba", "ka", "nha", "moq"]),

    ("KU",     ["ku", "tou", "bei"]),
    ("AQ",     ["aq", "cheq"]),
    ("POI",    ["poi"]),

    ("KIO/KI", ["kio", "ki"]),
    ("JU",     ["ju", "la"]),
    ("HU",     ["hu"]),

    ("TERM",   ["na", "ga", "cei"]),

    ("PO",     ["pó", "pö", "pỏ", "pô"]),
    ("JEI",    ["ȷéı", "ȷëı", "ȷẻı", "ȷêı"]),
    ("MEA",    ["méa", "mëa", "mẻa", "mêa"]),

    ("MO/TEO", ["mó", "mö", "mỏ", "mô", "teo"]),

    ("MI",     ["mí", "mï", "mỉ", "mî"]),
    ("SHU",    ["shú", "shủ", "shû"]),

    ("LU",     ["lú", "lü", "lủ", "lû", "lù", "lũ"]),
    ("LI",     ["lí", "lï", "lỉ", "lî", "lì", "lĩ"]),
    ("MA",     ["mả", "mâ", "tỉo", "tîo"]),

    ]

GROUP_COUNTS = [2, 4, 3, 3, 1, 3, 1, 2, 3]


# Just the particles alone 

PARTICLES = [part for cls in CLASSES for part in cls[1]]

# Special exceptional rule for aq and cheq

PARTICLES += ["áq", "chéq"]



# Extract the example from a line in the tsv file

def get_example(line):
    return line.split("\t")[1]


# Mod some information out of a string using a given key

def mod_out(string, key):
    for item in key:
        for synonym in item[1]:
            string = string.replace( synonym, item[0] )

    return string


# Remove aesthetic differences that don't change a word's identity

def normalize_word(word):
    return mod_out( word.lower(), AEST_REDUCE )


# Remove tone information

def detone_word(word):
    return mod_out( word, TONE_REDUCE )


# Put a word into the dictionary (if it's a particle)

def account_word(dicto, word, line_num):
    normal = normalize_word(word)

    if normal in PARTICLES:
        if normal not in dicto:
            dicto[normal] = set()

        dicto[normal].add(line_num)


# Parse a whole line's worth of words

def account_line(dicto, line, line_num):
    for word in get_example(line).split(" "):
        account_word(dicto, word, line_num)


# Add color to a number to indicate how good it is

def colorize(number):
    if number < 3:
        return Fore.RED + str(number) + Style.RESET_ALL

    if number < 15:
        return Fore.YELLOW + str(number) + Style.RESET_ALL

    return Fore.GREEN + str(number) + Style.RESET_ALL


# Open the file and parse all the lines

sentences = open("A_sentences.tsv")

dicto = dict()
line_num = 1

for line in sentences:
    account_line( dicto, line, line_num )
    line_num += 1

sentences.close()


# Special exceptional rule for aq and cheq, which can be written with
# or without tone marks

for special in ["áq", "chéq"]:
    if special in dicto:
        for line in dicto[special]:
            account_word(dicto, detone_word(special), line)


# Print the words we found

print()

for cls in CLASSES:
    print("  " + cls[0] + ":" + (9 - len(cls[0])) * " ", end='')

    for word in cls[1]:
        length = len(dicto[word]) if word in dicto else 0

        word = word + (5 - len(word)) * " "
        length = colorize(length) + (6 - len(str(length))) * " "

        print(word + length, end='')

    print()

    GROUP_COUNTS[0] -= 1
    if GROUP_COUNTS[0] == 0:
        GROUP_COUNTS = GROUP_COUNTS[1:]
        print()

