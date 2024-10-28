# List of comparison methods to compare two files and retrieve closest ones

# Nilsimsa
from nilsimsa import Nilsimsa, compare_digests, convert_hex_to_ints
import neo

import os
import hashlib
# import validators
import urllib.request
import file_comparison.npz as npz
import file_comparison.neo
import file_comparison.nilsimsa


adjacent_matrix_list1 = {}
adjacent_matrix_list2 = {}

# all_methods = {"npz":npz.npz_single, "neo":file_comparison.neo.compare_neo_file, "byte":file_comparison.nilsimsa.nilsimsa_single}

def build_adjacency_matrix():
    pass

# class FileInfo:
#     name = ""
#     url = ""
#     extention = ""
#     size = 0.

#     def finfo_to_dict (self): 
#         return {"name": self.name, "url": self.url, "size": self.size}

#     def __init__(self, file_path):

#         if validators.url (file_path):
#             # the file location is an URL
#             file = urllib.request.urlopen(file_path)


#             self.name = os.path.basename(file_path)
#             self.url = os.path.dirname(file_path) + "/"
#             self.extention = os.path.splitext(file_path)[1]
#             self.size = file.length

#         else:
#             # Get stats from local location
#             try:
#                 self.name = os.path.basename(file_path)
#                 self.url = os.path.dirname(file_path) + "/"
#                 self.extention = os.path.splitext(file_path)[1]
#                 self.size = os.path.getsize(file_path)
#             except:
#                 print ("FATAL ERROR ::")
#                 print (file_path)
#                 print ("Is neither a valid URL or local file")
#                 exit (EXIT_FAILURE)

def compute_ratio (score):
    return ((256.0 - (128.0 - score)) / 256.0)

def get_adviced_method (adjacency_matrix):
    adviced_methods = []
    for icouple in adjacency_matrix:

        # Guessing the file type based on its extension

        # NPZ
        if icouple[0].extention == ".npz" and icouple[1].extention == ".npz":
            adviced_methods.append ("npz")
            continue

        # NEO
        try:
            neo_reader1 = neo.io.get_io(icouple[0].url + icouple[0].name)
            neo_reader2 = neo.io.get_io(icouple[1].url + icouple[1].name)
            adviced_methods.append ("neo")
            continue

        # except IOError as e:
        #     print ("Warning :: NEO :: " + icouple[0].url + icouple[0].name + " :: " + str(e))
        #     print (icouple[0].url + icouple[0].name + "\n")

        except Exception  as e:
            print ("\nError :: NEO ::" + str(type(e).__name__) + " " + str(e))
            print (icouple[0].url + icouple[0].name + "\n")

        adviced_methods.append ("byte")

    print ("\nAdviced Methods ::")
    print (adviced_methods)
    return adviced_methods


# def get_files_from_watchdog_log (watchdog_file, is_hex=1):
#     list_of_files = []
#     print ("Is HEX ? " + str(is_hex))

#     with open (watchdog_file, 'r') as f1:
#         lines = f1.readlines()
#         for irawline in lines :
#             iline = irawline.split('\n')[0]
#             src_dest = iline.split()
#             for ifile in src_dest:
#                 finfo = FileInfo (ifile)
#                 ifilehex = finfo.name

#                 if is_hex:
#                     ifilehex = str(hashlib.md5(bytes(finfo.name + str(finfo.size), encoding='utf-8')).hexdigest())
#                 print ("IFileName = " + finfo.url + "/" + finfo.name)
#                 list_of_files.append(finfo)

#     return list_of_files

def find_bijective (f1, f2, hex=1):

    # Check hexadigest file format
    # list_of_files_rows = []
    # list_of_files_cols = []

    # if hex==1:
    #     # Read files from watchdog logs
    #     # The produced files
    #     print ("L1:")
    #     adjacent_matrix_list1 = get_files_from_watchdog_log (f1, True)
    #     print ("L2:")
    #     adjacent_matrix_list2 = get_files_from_watchdog_log (f2, False)

    # elif hex==2:
    #     # Read files from watchdog logs
    #     print ("L1:")
    #     adjacent_matrix_list1 = get_files_from_watchdog_log (f1, True)
    #     print ("L2:")
    #     adjacent_matrix_list2 = get_files_from_watchdog_log (f2, True)
    # else:
    #     # Read files from watchdog logs
    #     print ("L1:")
    #     adjacent_matrix_list1 = get_files_from_watchdog_log (f1, False)
    #     print ("L2:")
    #     adjacent_matrix_list2 = get_files_from_watchdog_log (f2, False)



    # print ("\n")
    # print ("adjacent_matrix_list1")
    # print (adjacent_matrix_list1)
    # print ("\n")
    # print ("adjacent_matrix_list1")
    # print (adjacent_matrix_list2)
    # print ("\n")

    # Score Matrix
    score_matrix = []

    # # Loop over all files in list01 and list02 and compute a score for each write_code_location
    for ifile in adjacent_matrix_list1:
        # Gives the first row
        irow = []
        for jfile in adjacent_matrix_list2:
            try:
                irow.append (hash_from_file_metadata(ifile, jfile))
                # irow.append (hash_from_file_info(ifile, jfile))
            except FileNotFoundError as e:
                print (e)
                print("Does File exist ?")
                irow.append(0.)
            except KeyError as e:
                print(e)
                print("Does file hash exist ?")
                irow.append(0.)
            except Exception as e:
                print(e)
                print("Unsupported error")
                irow.append (0.)
        score_matrix.append(irow)

    pairs = []

    # Find best score per row
    # with open("list1.txt", 'w') as f_rows:
    #     with open("list2.txt", 'w') as f_cols:
    for irow in range(len(score_matrix)):
        # Find the couples that match the most according to the scores
        max_score = max(score_matrix[irow])
        max_idx_list = [i for i, j in enumerate(score_matrix[irow]) if j == max_score]

        if max_score > 0.:
            for iidx in max_idx_list:
                # print (list(adjacent_matrix_list1.values())[irow])
                # f_rows.write(str(list(adjacent_matrix_list1.values())[irow]) + "\n")
                # f_cols.write(str(list(adjacent_matrix_list2.values())[iidx]) + "\n")
                ituple = tuple ((adjacent_matrix_list1[irow], adjacent_matrix_list2[iidx]))
                pairs.append (ituple)

    return pairs


# Determine and return the name of the file and the size in two classes
# 1. The file is a local path location
# 2. The file is remote URL
# def get_file_info (file_path):
#
#     finfo = FileInfo ()
#
#     # Determine URL or local path ?
#     if validator.url (filepath):
#         # the file location is an URL
#         site = urllib.urlopen(file_path)
#         meta = site.info()
#
#         finfo = FileInfo (os.path.basename(file_path), os.path.dirname(file_path), os.path.splitext(file_path)[1], meta.getheaders("Content-Length")[0])
#
#     else:
#         # Get stats from local location
#         try:
#             finfo = FileInfo (os.path.basename(file_path), os.path.dirname(file_path), os.path.basename(file_path), os.path.splitext(file_path)[1], os.path.getsize(file_path))
#         except:
#             print ("FATAL ERROR ::")
#             print (file_path)
#             print ("Is neither a valid URL or local file")
#             exit (EXIT_FAILURE)
#
#     return finfo

##
# Parameters are pairs (arrays of 2 items)
# array[0] : original url of the file, original name
# array[1] : true path of the file on disk (hashed, moved or transformed name)
def hash_from_file_info (file1_info, file2_info):
    ## Hash file informations
    #   * file name
    #   * file size
    #   * file path
    # url1 = f1_pair["url"]
    # path1 = f1_pair["file"]
    # url2 = f2_pair["url"]
    # path2 = f2_pair["file"]
    #
    # file1_info = get_file_info (f1_pair["url"])
    # file2_info = get_file_info (f2_pair["url"])

    print ("\nDirname f1= " + file1_info.url)
    print ("Basename f1= " + file1_info.name)
    print ("Size f1 = " + str(file1_info.size))
    print ("Dirname f2= " + file2_info.url)
    print ("Basename f2= " + file2_info.name)
    print ("Size f2 = " + str(file2_info.size))
    all_info_f1 = file1_info.name + str(file1_info.size)
    all_info_f2 = file2_info.name + str(file2_info.size)
    print (all_info_f1)
    print (Nilsimsa(all_info_f1))
    print (all_info_f2)
    print (Nilsimsa(all_info_f2))
    ratio = compute_ratio (compare_digests (Nilsimsa(all_info_f1).hexdigest(), Nilsimsa(all_info_f2).hexdigest()))
    print ("FINFO Ratio = " + str(ratio*100) + "\n")
    return (ratio*100)
    ## Hash is done using Nilsimsa algorithm to get strong colisions
    # f1_hash = Nilsimsa (bytes(os.path.dirname + ))

def hash_from_file_metadata (file1:dict, file2:dict) -> float:
    ratio = compute_ratio (compare_digests (file1["hash"], file2["hash"]))
    return ratio*100

# def advice_method (adjacency_matrix)


