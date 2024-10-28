# Hamming
from scipy.spatial.distance import hamming

def compute_ratio (score, buffer_size):
    # Error max
    # float64 * buffer_size
    Emax = 1*buffer_size
    return ( (score*100)/ (Emax-score))

## Computes Hamming Distance between seq1 and seq2
#  Using Scipy spatial distance
def hamming_distance_scipy (seq1, seq2):
    return hamming(seq1, seq2) * len(seq1)

def hamming_files(f1_path, f2_path, buffer_size=32):
    with open(f1_path, "r") as f1:
        with open(f2_path, "r") as f2:
            linesf1 = f1.readlines()
            linesf2 = f2.readlines()
            assert(len(linesf1) == len(linesf2))
            for idx in range(len(linesf1)):
                # Set default filename
                filename1 = linesf1[idx].split("\n")[0]
                filename2 = linesf2[idx].split("\n")[0]

                hamming_single(filename1, filename2, buffer_size)

def hamming_single(f1_path, f2_path, buffer_size=32):

    # Total Score
    TOTAL_SCORE = 0
    # Number of buffer used
    NBUFFER = 0
    # Total ratio
    TOTAL_RATIO = 0

    # Open files in byte mode
    # Cut the files into N bytes with N=64
    # Compatible with Python 2.6 and Python 3.x
    with open(f1_path, "rb") as f1, open(f2_path, "rb") as f2:
        f1_byte = f1.read(buffer_size)
        f2_byte = f2.read(buffer_size)
        max_distance = 0

        if not f1_byte:
            f1_byte.zfill(buffer_size)
        if not f2_byte:
            f2_byte.zfill(buffer_size)

        while True:
        # while f1_byte and f2_byte:
            # Run Hamming Distance computation
            # score = hamming_distance(f1_byte, f2_byte)
            score = hamming_distance_scipy(f1_byte, f2_byte)
            if max_distance < score:
                max_distance = score
            NBUFFER += 1
            TOTAL_SCORE += score
            TOTAL_RATIO += compute_ratio (score, buffer_size)
            # Initialize strings
            f1_byte = f1.read(buffer_size)
            f2_byte = f2.read(buffer_size)

            if not f1_byte and not f2_byte:
                break

            if not f1_byte:
                f1_byte.zfill(buffer_size)
            if not f2_byte:
                f2_byte.zfill(buffer_size)
            print ("Comparing::")
            print (f1_byte)
            print (f2_byte)
            print ("\n")



        print ("Total Distance = " + str(TOTAL_SCORE))
        print ("Maximum Hamming Distance = " + str(max_distance))
        print ("Nb buffers = " + str(NBUFFER))
        print ("Average Distance = " + str(TOTAL_SCORE / NBUFFER))
        print ("Average Ratio = " + str(TOTAL_RATIO / NBUFFER * 100) + " %")
