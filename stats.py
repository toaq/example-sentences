import sys

# Key to modding out aesthetic information

AEST_REDUCE = [ ("ı", "i"),
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

    ("MOTEO", ["mo", "teo"]),
    ("KIOKI", ["kio", "ki"]),
    ("JU",    ["ju", "la"]),

    ("PO",    ["po", "jei", "mea"]),

    ("MI",    ["mi"]),
    ("SHU",   ["shu"]),

    ("LU 1",  ["lu", "li"]),
    ("LU 2",  ["ma", "tio"]),

    ("HU",    ["hu"]),

    ("TERM",  ["na", "ga", "cei"])

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

def detone(word):
    return mod_out( word, TONE_REDUCE )


# Put a single word into the dictionary

def account_word(dicto, word, line_num):
    normal = normalize_word(word)
    base = detone(normal)

    print("  Accounting word: " + word + " (" + normal + "," + base + ")")

    # If this word is a particle (detected by inspecting <normal>)
    # then add it to the dictionary (without aesthetic info but with tone)

    if base in PARTICLES:
        if normal not in dicto:
            dicto[normal] = set()

        dicto[normal].add(line_num)


# Parse a whole line's worth of words

def account_line(dicto, line, line_num):
    print("Accounting line: " + line, end='')

    for word in get_example(line).split(" "):
        account_word(dicto, word, line_num)


# Open the file and parse all the lines

sentences = open("A_sentences.tsv")

dicto = dict()
line_num = 1

for line in sentences:
    account_line( dicto, line, line_num )
    line_num += 1

    if line_num > 10:    # temporary
        break

sentences.close()


# Print the words we found

for cls in CLASSES:
    print(cls[0])

    for base in cls[1]:
        represented = False

        for word in dicto:
            if detone(word) == base:
                represented = True
                print("  " + word + "\t" + str(dicto[word]))

        if not represented:
            print("  " + base + "\t" + "Unrepresented!")
                

    print()


