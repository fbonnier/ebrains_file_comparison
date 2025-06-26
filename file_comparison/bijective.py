# List of comparison methods to compare two files and retrieve closest ones

# Nilsimsa
from nilsimsa import Nilsimsa, compare_digests

# Magic - determine file formats of outputs
import magic

# Determine if file1 and file2 are the same format
#   file1, file2: {"url", "path", "hash"}
def are_same_file_format (file1, file2):
    file1_format = magic.from_file(file1["path"], mime = True)
    file2_format = magic.from_file(file2["path"], mime = True)

    block = {"format": [],"format score": None, "format error": None}
    if file1_format == file2_format:
        block["format score"] = True
        block["format"].append (file1_format)
    else:
        block["format score"] = False
        block["format"].append (file1_format)
        block["format"].append (file2_format)
        block["format error"] = "Error: " + file1["path"] + " is " + str(file1_format) + " | " + file2["path"] + " is " + str(file2_format)

    return block

def compute_ratio (score):
    return ((256.0 - (128.0 - score)) / 256.0)

def find_bijective (produced_outputs, expected_outputs):

    # All files scores
    all_file_scores = [[{"partner": None, "score": 0} for _ in expected_outputs] for _ in produced_outputs]

    # Compute scores for all pairs of files
    for ifile1 in produced_outputs:
        for ifile2 in expected_outputs:
            all_file_scores[produced_outputs.index(ifile1)][expected_outputs.index(ifile2)]["score"] = compute_ratio(compare_digests(Nilsimsa(ifile1["filename"] + str(ifile1["size"])).hexdigest(), Nilsimsa(ifile2["filename"] + str(ifile2["size"])).hexdigest()))
            all_file_scores[produced_outputs.index(ifile1)][expected_outputs.index(ifile2)]["partner"] = ifile2

    # List of pairs of files to return
    blocks_of_pairs = []

    # Compute the maximum score for each produced file
    for ifile1 in produced_outputs:
        iproduced_max_score = {"partner": None, "score": 0}
        # Search for the nearest partner
        for ifile2 in expected_outputs:
            new_score = all_file_scores[produced_outputs.index(ifile1)][expected_outputs.index(ifile2)]["score"]
            if iproduced_max_score["score"] < new_score:
                iproduced_max_score["partner"] = ifile2
                iproduced_max_score["score"] = new_score

        ipartner_max_score = {"partner": None, "score": 0}
        # Search for the nearest of the nearest
        for ipartner in produced_outputs:
            best_score_ipartner = all_file_scores[produced_outputs.index(ipartner)][expected_outputs.index(iproduced_max_score["partner"])]["score"]
            if ipartner_max_score["score"] < best_score_ipartner:
                ipartner_max_score["partner"] = ipartner
                ipartner_max_score["score"] = best_score_ipartner

        # If the maximum score is the same for both produced and expected files, then we have a bijective pair
        # and we can build a block of pairs
        if ipartner_max_score["score"] == iproduced_max_score["score"] and ipartner_max_score["partner"] == ifile1:
            block = {"Origin": None, "New": None, "hash score": None, "format": None, "error": [], "method": None, "log":[], "advice": [], "score": []}
            block["Origin"] = iproduced_max_score["partner"]
            block["Origin"]["origin"] = "expected"
            block["New"] = ifile1
            block["New"]["origin"] = "produced"
            block["bijective score"] = ipartner_max_score["score"]*100
            print("Found bijective pair: " + str(block["Origin"]["filename"]) + " <-> " + str(block["New"]["filename"]) + " with score: " + str(block["bijective score"]))
            
            # Compare file formats
            
            format_block = are_same_file_format (ifile1, ipartner_max_score["partner"])
            if format_block["format score"]:
                block["format"] = format_block["format"][0]
            else:
                block["format"] = format_block["format"]
                block["error"].append(format_block["format error"])

            blocks_of_pairs.append(block)
        else:
            print("No bijective pair found for: " + str(ifile1["filename"]) + " partnered with " + str(iproduced_max_score["partner"]["filename"]) + " has better candidate")
  
  ################################################################################################

    # # Walk the files and build blocks of pairs
    # blocks_of_pairs = [] 
    # for ifile1 in produced_outputs:
    #     partner = {"ifile2": None, "score": 0}
    #     # Search for nearest partner
    #     for ifile2 in expected_outputs:
    #         new_score = compute_ratio(compare_digests(Nilsimsa(ifile1["filename"] + str(ifile1["size"])).hexdigest(), Nilsimsa(ifile2["filename"] + str(ifile2["size"])).hexdigest()))
    #         if partner["score"] < new_score:
    #             partner["ifile2"] = ifile2
    #             partner["score"] = new_score
    #     block = {"Origin": None, "New": None, "hash score": None, "format": None, "error": [], "method": None, "log":[], "advice": [], "score": []}
    #     block["Origin"] = partner["ifile2"]
    #     block["Origin"]["origin"] = "expected"
    #     block["New"] = ifile1
    #     block["New"]["origin"] = "produced"
    #     block["bijective score"] = partner["score"]*100

    #     # Compare file formats
    #     format_block = are_same_file_format (ifile1, partner["ifile2"])
    #     if format_block["format score"]:
    #         block["format"] = format_block["format"][0]
    #     else:
    #         block["format"] = format_block["format"]
    #         block["error"].append(format_block["format error"])

    #     blocks_of_pairs.append(block)

    return blocks_of_pairs