
# Fuzzy String comparisons
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Compare two list of files
# f1_path contains the first list of files
# f2_path contains the second list of files
# f1 and f2 must have the same number of lines (of files to compare, each line is a path of a file)
# The files will be compared one by one and are supposed to have bijective relation:
# f1:line 1 <-> f2:line 1
# f1:line 2 <-> f2:line 2
# f1:line n <-> f2:line n
def levenshtein (f1_path, f2_path, buffer_size=32):

    with open(f1_path, "r") as f1:
        with open(f2_path, "r") as f2:
            linesf1 = f1.readlines()
            linesf2 = f2.readlines()
            assert(len(linesf1) == len(linesf2))
            for idx in range(len(linesf1)):
                # Set default filename
                filename1 = linesf1[idx].split("\n")[0]
                filename2 = linesf2[idx].split("\n")[0]

                levenshtein_single(filename1, filename2, buffer_size)


def levenshtein_single (f1_path, f2_path, buffer_size=32):

    # Total Score
    TOTAL_SCORE = 0
    # Number of buffer used
    NBUFFER = 0

    # Open files in byte mode
    # Cut the files into N bytes with N=32
    # Compatible with Python 2.6 and Python 3.x
    # ref: https://stackoverflow.com/questions/1035340/reading-binary-file-and-looping-over-each-byte
    with open(f1_path, "rb") as f1, open(f2_path, "rb") as f2:
        f1_byte = f1.read(buffer_size)
        f2_byte = f2.read(buffer_size)

        while f1_byte and f2_byte:
            # Run Levenshtein Distance computation
            score = fuzz.ratio(str(f1_byte), str(f2_byte))

            NBUFFER += 1
            TOTAL_SCORE += score
            # Initialize strings

            f1_byte = f1.read(buffer_size)
            f2_byte = f2.read(buffer_size)

        # Last comparison in case the files closed before filling 64 bytes arrays
        if len(str(f1_byte)):
            score = fuzz.ratio(str(f1_byte), str(f2_byte))
            NBUFFER += 1
            TOTAL_SCORE += score
            # print ("Last score for arrays of size " + str(len(f1_str)) + " " + str(len(f2_str)) + " = " + str(score))
        print ("Total = " + str(TOTAL_SCORE))
        print ("Total buffer = " + str(NBUFFER))
        print ("Total ratio = " + str(TOTAL_SCORE / NBUFFER) + " %")
