import sys
from colorama import Fore, Back, Style


# ---------- READ RECIPE FILE ---------- #

# Parse "ku* 50" into ("ku", True, 50, [])

def parse_search_item(term, target_quantity):
    if term[-1] == "*":
        return (term[:-1], True,  target_quantity, set())
    else:
        return (term,      False, target_quantity, set())

# Parse "[class name] [search item...]" into a list

def parse_recipe_line(line):
    parts = line.split()
    
    if parts == []:
        return []

    ret = [parts[0].upper()]
    parts = parts[1:]

    while len(parts) > 0:
        ret += [parse_search_item( parts[0], int(parts[1]) )]
        parts = parts[2:]

    return ret

# Parse a whole file, with blank lines producing blank classes

def parse_recipe(f):
    fh = open(f)
    ret = list([parse_recipe_line(l) for l in fh])
    fh.close()
    return ret


# ---------- ACCOUNT FOR A WORD ---------- #

AEST_REDUCE = [ ("i", "ı"), ("j", "ȷ"), ("", ".!?,") ]

TONE_REDUCE = [ ("a", "āáäảâàãaǎ"), ("e", "ēéëẻêèẽeě"),
                ("i", "īíïỉîìĩıǐ"), ("o", "ōóöỏôòõoǒ"),
                ("u", "ūúüủûùũuǔ"), ("y", "ȳýÿỷŷỳỹyy̌") ]

# Remove information from a word according to key

def mod_out(string, key):
    for item in key:
        for synonym in item[1]:
            string = string.replace( synonym, item[0] )

    return string

# Remove aesthetic information

def normalize_word(word):
    return mod_out( word.lower(), AEST_REDUCE )

# Remove tone information

def detone_word(word):
    return mod_out( word, TONE_REDUCE )

# Check if a search item matches a given word

def check_match( search_item, word ):
    search = normalize_word( search_item[0] )
    word   = normalize_word( word )

    if search_item[1]:
        search = detone_word( search )
        word   = detone_word( word )

    return search == word

# If this search item matches this word, add this line to its record

def item_account_word( search_item, word, line ):
    if check_match( search_item, word ):
        search_item[3].add(line)

# Check all search terms in a recipe against this word and line

def recipe_account_word( recipe, word, line ):
    for cls in recipe:
        for item in cls[1:]:
            item_account_word( item, word, line )


# ---------- READ THROUGH THE EXAMPLES ---------- #

# Extract the example from a line in the tsv file

def get_example(line):
    return line.split("\t")[1]

# Parse a whole file

def account_file(recipe, f):
    fh = open(f)
    line_num = 1

    for line in fh:
        for word in get_example(line).split(" "):
            recipe_account_word(recipe, word, line_num)

        line_num += 1

        if line_num % 100 == 0:
            print( str(line_num) + " / 1000" )

    fh.close()


# ---------- PRINT THE RESULTS ---------- #

# Add color to a number to indicate how good it is

def colorize(text, proportion):
    if proportion < .2:
        return Fore.RED + Style.BRIGHT + text + Style.RESET_ALL

    if proportion < .7:
        return Fore.RED + text + Style.RESET_ALL

    if proportion < 1:
        return Fore.YELLOW + text + Style.RESET_ALL

    return Fore.GREEN + text + Style.RESET_ALL

def greyify(text):
    return Style.DIM + text + Style.RESET_ALL


# ---------- PROGRAM ---------- #

recipe = parse_recipe( "recipe_2.txt" )
account_file( recipe, "A_sentences.tsv" )


# Print the words we found

print()

for cls in recipe:
    if cls == []:
        print()
        continue

    print("  " + cls[0] + ":" + (9 - len(cls[0])) * " ", end='')

    for item in cls[1:]:
        word = item[0]
        target = item[2]
        count = len(item[3])

        length = 5 + len(str(count)) + 1 + len(str(target))

        word  = word + (5 - len(word)) * " "
        count = colorize(str(count), count / target)
        denom = greyify("/" + str(target))

        padding = (15 - length) * " "

        print(word + count + denom + padding, end='')

    print()
