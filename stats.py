
MARKS = [("a", "ā"), ("a", "á"), ("a", "ä"), ("a", "ả"), # normal tones
         ("a", "â"), ("a", "à"), ("a", "ã"), ("a", "a"),
         ("e", "ē"), ("e", "é"), ("e", "ë"), ("e", "ẻ"),
         ("e", "ê"), ("e", "è"), ("e", "ẽ"), ("e", "e"),
         ("i", "ī"), ("i", "í"), ("i", "ï"), ("i", "ỉ"),
         ("i", "î"), ("i", "ì"), ("i", "ĩ"), ("i", "i"),
         ("o", "ō"), ("o", "ó"), ("o", "ö"), ("o", "ỏ"),
         ("o", "ô"), ("o", "ò"), ("o", "õ"), ("o", "o"),
         ("u", "ū"), ("u", "ú"), ("u", "ü"), ("u", "ủ"),
         ("u", "û"), ("u", "ù"), ("u", "ũ"), ("u", "u"),
         ("y", "ȳ"), ("y", "ý"), ("y", "ÿ"), ("y", "ỷ"),
         ("y", "ŷ"), ("y", "ỳ"), ("y", "ỹ"), ("y", "y"),
         
         ("a", "ǎ"), ("e", "ě"), ("i", "ǐ"), ("o", "ǒ"), # old third tone
         ("u", "ǔ"), ("y", "y")]

def get_example(line):
    return line.split("\t")[1]

def normalize(example):
    for mark in MARKS:
        example = example.replace( mark[1], mark[0] )

    return example


sentences = open("A_sentences.tsv")

for line in sentences:
    print( normalize( get_example( line ) ) )

sentences.close()
