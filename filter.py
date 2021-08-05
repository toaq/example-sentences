
import sys

infile         = open("filter/original.tsv", "r")
outfile_keep   = open("filter/keep.tsv",     "a")
outfile_delete = open("filter/delete.tsv",   "a")
outfile_fix    = open("filter/fix.tsv",      "a")
outfile_ponder = open("filter/ponder.tsv",   "a")

lines = [line.strip() for line in infile]
infile.close()
    
while lines != []:
    line = lines[0]
    parts = line.split("\t")
    toaq = parts[1]
    eng  = parts[2]

    if not (toaq == "" and eng == ""):
        print()
        print("    " + toaq)
        print("    " + eng)
        print("")
        print(" (k) keep this sentence as-is")
        print(" (d) delete this sentence")
        print(" (f) fix this sentence later")
        print(" (p) ponder this sentence later")
        print(" (q) quit and save progress")
        print("")

        response = ""

        while True:
            response = input("> ")

            if response == "k":
                print(line, file=outfile_keep)
                break

            if response == "d":
                print(line, file=outfile_delete)
                break

            if response == "f":
                print(line, file=outfile_fix)
                break

            if response == "p":
                print(line, file=outfile_ponder)
                break

            if response == "q":
                outfile_keep.close()
                outfile_delete.close()
                outfile_fix.close()

                infile = open("filter/original.tsv", "w")

                for line in lines:
                    print(line, file=infile)

                sys.exit()

    lines = lines[1:]
