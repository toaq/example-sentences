
# Replacements to make to remove diacricits

MARKS = [("a", "āáäảâàãaǎ"),
         ("e", "ēéëẻêèẽeě"),
         ("i", "īíïỉîìĩiǐ"),
         ("o", "ōóöỏôòõoǒ"),
         ("u", "ūúüủûùũuǔ"),
         ("y", "ȳýÿỷŷỳỹyy̌")]


# Particle words to take stats on:

#   SA (sa, sıa, tu, ja, ke, hı, co, baq, hoı)
#   TO (to) RU (ru, ra, ro, rı, roı) 
#   DA (da, ba, ka, moq)
#   LU (lu, lı, ma, tıo)
#   GO (fı, go, cu, ta)
#   PO (po, jeı, mea) 
#   JE (je, keo, tıu) 
#   KU (ku, tou, beı)
#   BI (bı, pa)
#   JU (ju, la) 
#   MI (mı) SHU (shu)
#   KIO (kıo) KI (kı) 
#   MO (mo) TEO (teo)
#   HU (hu) 
#   NA (na), GA (ga), CEI (ceı)


def get_example(line):
    return line.split("\t")[1]

def normalize(example):
    for mark in MARKS:
        for marky in mark[1]:
            example = example.replace( marky, mark[0] )

    return example


sentences = open("A_sentences.tsv")

for line in sentences:
    print( normalize( get_example( line ) ) )

sentences.close()
