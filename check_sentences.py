
def find_problems(lines, exceptions):
    letters = "àèìòùỳ"
    count = 0

    exceptions = [e.lower() for e in exceptions]

    for line in lines:
        for word in line.split("\t")[1].split(" "):
            if any(letter in word for letter in letters) and not word.lower() in exceptions:
                print(line, end="")
                count += 1
                break

    return count

lines = [line for line in open("A_sentences.tsv")]

exceptions = ["rào", "kùı", "gào", "shìu", "jìe", "tì", "bìe", "còu", "chùochā", "nìe", "chòe", "dùoı", "cà", "gòe"]
ignore = []
#ignore     = ["jìa", "pù", "shè", "nàı", "bù", "dè"]

count = find_problems(lines, exceptions + ignore)
print("\n" + str(count))
