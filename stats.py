import sys

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

    ("SA 1",  ["sa", "sia", "tu"]),
    ("SA 2",  ["ja", "hi", "co"]),
    ("SA 3",  ["ke", "baq"]),
    ("SA 4",  ["hoi"]),

    ("TO",    ["to"]),
    ("RU 1",  ["ru", "ra", "ro"]),
    ("RU 2",  ["ri"]),
    ("RU 3",  ["roi"]),

    ("JE",    ["je", "keo", "tiu"]),
    ("BI",    ["bi", "pa"]),
    ("DA",    ["da", "ba", "ka", "nha", "moq"]),

    ("GO",    ["fi", "go", "cu", "ta"]),
    ("KU",    ["ku", "tou", "bei"]),

    ("KIOKI", ["kio", "ki"]),
    ("JU",    ["ju", "la"]),

    ("HU",    ["hu"]),

    ("TERM",  ["na", "ga", "cei"]),

    ("PO",    ["pó", "pö", "pỏ", "pô"]),
    ("JEI",   ["ȷéı", "ȷëı", "ȷẻı", "ȷêı"]),
    ("MEA",   ["méa", "mëa", "mẻa", "mêa"]),

    ("MOTEO", ["mó", "mö", "mỏ", "mô", "teo"]),

    ("MI",    ["mí", "mï", "mỉ", "mî"]),
    ("SHU",   ["shú", "shủ", "shû"]),

    ("LU",    ["lú", "lü", "lủ", "lû", "lù", "lũ"]),
    ("LI",    ["lí", "lï", "lỉ", "lî", "lì", "lĩ"]),
    ("MA",    ["mả", "mâ", "tỉo", "tîo"]),

    ]


# Just the particles alone 

PARTICLES = [part for cls in CLASSES for part in cls[1]]



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


# Add spaces to the end of a word to make it a certain length

def lengthen(word, length):
    return word + (length - len(word)) * " "


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


# Open the file and parse all the lines

sentences = open("A_sentences.tsv")

dicto = dict()
line_num = 1

for line in sentences:
    account_line( dicto, line, line_num )
    line_num += 1

sentences.close()


# Print the words we found

for cls in CLASSES:
    print(lengthen(cls[0] + ":", 10), end="")

    for word in cls[1]:
        length = len(dicto[word]) if word in dicto else 0
        printout = lengthen(word, 5) + str(length)
        print(lengthen(printout, 11), end="")

    print()


