# Method class
import numpy
import neo

from sklearn.metrics import mean_squared_error
from math import sqrt

import file_comparison.neo
import file_comparison.npz
import file_comparison.text
# Nilsimsa
import file_comparison.nilsimsa
from nilsimsa import Nilsimsa, compare_digests

import file_comparison.error_handler as error_handler


class Method:

    __name__ = ""
    __difference_methods__ = {"neo": file_comparison.neo.compute_differences_report, "npz": file_comparison.npz.compute_differences_report, "byte": file_comparison.nilsimsa.compute_differences_report, "txt": file_comparison.text.compute_differences_report}
    __score_methods__ = {"neo": file_comparison.neo.compute_score, "npz": file_comparison.npz.compute_score, "byte": file_comparison.nilsimsa.compute_score, "txt": file_comparison.text.compute_score}
    __check_methods__ = {"neo": file_comparison.neo.check_file_formats, "npz": file_comparison.npz.check_file_formats, "byte": file_comparison.nilsimsa.check_file_formats, "txt": file_comparison.text.check_file_formats}

    # File containing known/expected results
    original_file = None

    # File containing simulated/produced results
    new_file = None

    # Global score of file
    score = 0.

    # Number of different values
    ndiff = 0
    # Total number of values in dataset
    number_of_values = 0
    # Ratio between number of different values and total values: quantity_score = ndiff/number_of_values
    quantity_score = 0.

    # Complete list of datasets containing values and local scores
    differences_report = []
    
    # Global Mean MSE value
    rmse_score = 0.

    # Global Mean MSE value
    mse_score = 0.

    # Global MAPE score
    mape_score = 0.

    # Hash score calculated between the two files
    hash_score = 0.

    # Global MRPD score
    mrpd_score = 0.

    # Global MPE score
    mpe_score = 0.

    # Global MSPE score
    mspe_score = 0.

    # Global RMSPE score
    rmspe_score = 0.

    # Global Levenshtein score
    levenshtein_score = 0.

    # Global Mean Nilsimsa score
    nilsimsa_score = 0.

    # Global Maximum absolute difference
    max_delta = 0.

    # Global Mean absolute difference
    delta = 0.

    # Total list of critical errors raised during score computation
    errors = []

    # Total list of logs raised during score computation
    log = []

    # Total list of advices raised during score computation
    advices = []

    # 1.1
    def __init__ (self, ipair: dict):

        self.__name__ = ipair["method"]
        # TODO: Replace assert by Exception
        assert self.__name__ in self.__difference_methods__, "Method \"" + self.__name__ + "\" unsupported. Method should be \"npz\", \"neo\", \"txt\" or \"byte\""
        self.original_file = ipair["Origin"]
        self.new_file = ipair["New"]

    # 2
    def check_file_formats (self):
        check1 = False
        check2 = False
        error1 = None
        error2 = None

        if not (self.original_file or self.new_file):
            return False, "Method.check_file_formats: Unknown files"
        else:
            try:
                check1, error1 = self.__check_methods__[self.__name__](self.original_file["path"])
            except Exception as e:
                check1 = False
                error1 = "Method.check_file_formats: " + str(error_handler.get_traceback(e))
            try:
                check2, error2 = self.__check_methods__[self.__name__](self.new_file["path"])
            except Exception as e:
                check2 = False
                error2 = "Method.check_file_formats: " + str(error_handler.get_traceback(e))
                # self.differences_report = [{"Fatal Error": "check_file_formats FAIL " + str(type(e)) + ": file have Unknown or different file formats -- " + str(e)}]
                # return False, file_comparison.report_generator.generate_report_1_file (self.original_file, self.new_file, self.__name__, self.score, self.differences_report)
        check = check1 and check2
        error = [error1,  error2] if error1 and error2 else []
        return check, error 
    
    # Compare the two file's hash
    def compare_hash (self):

        try:
            with open(self.original_file["path"], "rb") as foriginal, open(self.new_file["path"], "rb") as fnew:
                original_hash = Nilsimsa (foriginal.read())
                new_hash = Nilsimsa (fnew.read())
                score_nilsimsa = compare_digests (original_hash.hexdigest(), new_hash.hexdigest())
                ratio = file_comparison.nilsimsa.compute_ratio (score_nilsimsa)
                self.hash_score = ratio*100.
        except Exception as e:
            self.errors.append("compare_hash error: " + str(error_handler.get_traceback(e)))
            self.log.append("compare_hash error: " + str(error_handler.get_traceback(e)))

    # 2.pair
    def check_file_formats_pair (self):
        try:
            return self.__check_methods__[self.__name__](self.original_file, self.new_file), {}
        except Exception as e:
            self.differences_report = [{"Fatal Error": "check_file_formats FAIL " + str(type(e)) + ": file have Unknown or different file formats -- " + str(error_handler.get_traceback(e))}]
            return False, file_comparison.report_generator.generate_report_1_file (self.original_file, self.new_file, self.__name__, self.score, self.differences_report)

    # 4
    def compute_score (self):
        ### Initialized all scores
        self.levenshtein_score = 0.
        self.nilsimsa_score = 0.
        self.rmspe_score = 0.
        self.mspe_score = 0.
        self.mape_score = 0.
        self.mpe_score = 0.
        self.mrpd_score = 0.
        self.max_delta = 0.
        self.delta = 0.
        self.ndiff = 0
        self.score = 0.
           
        ### Sum for all datasets the scores
        for idataset in self.differences_report:
            if idataset["levenshtein"]: self.levenshtein_score += 100. - idataset["levenshtein"]
            if idataset["nilsimsa"]: self.nilsimsa_score += idataset["nilsimsa"]
            if idataset["rmspe"]: self.rmspe_score += 100 - idataset["rmspe"]
            if idataset["mspe"]: self.mspe_score += 100 - idataset["mspe"]
            if idataset["mape"]: self.mape_score += 100 - idataset["mape"]
            if idataset["mpe"]: self.mpe_score += 100 - idataset["mpe"]
            if idataset["rpd"]: self.mrpd_score += 100 - idataset["rpd"]
            if idataset["max delta"]: self.max_delta = max(self.max_delta, idataset["max delta"])
            if idataset["delta"]: self.delta += idataset["delta"]
            if idataset["ndiff"]: self.ndiff += idataset["ndiff"]

        if not self.number_of_values:
            self.errors.append("Method.compute_score: No values to compute score")
            return

        self.levenshtein_score += 100. * (self.number_of_values - self.ndiff)
        self.levenshtein_score = self.levenshtein_score / self.number_of_values

        self.nilsimsa_score += 100. * (self.number_of_values - self.ndiff)
        self.nilsimsa_score = self.nilsimsa_score/self.number_of_values

        self.rmspe_score += 100. * (self.number_of_values - self.ndiff)
        self.rmspe_score = self.rmspe_score / self.number_of_values

        self.mspe_score += 100. * (self.number_of_values - self.ndiff)
        self.mspe_score = self.mspe_score / self.number_of_values

        self.mape_score += 100. * (self.number_of_values - self.ndiff)
        self.mape_score = self.mape_score / self.number_of_values

        self.mpe_score += 100. * (self.number_of_values - self.ndiff)
        self.mpe_score = self.mpe_score / self.number_of_values

        self.mrpd_score += 100. * (self.number_of_values - self.ndiff)
        self.mrpd_score = self.mrpd_score / self.number_of_values

        self.quantity_score = 100. - (self.ndiff/self.number_of_values * 100.)
        
        self.delta = self.delta/self.number_of_values
            
        # # # Calculate MSE
        # squared_deltas = [ipair["delta"]*ipair["delta"] for ipair in self.differences_report if ipair["delta"]]
        # if squared_deltas:
        #     self.mse_score = sum(squared_deltas)/self.number_of_values

        # # Calculate RMSE
        # if self.mse_score:
        #     self.rmse_score = sqrt(self.mse_score)

        # # # try:
        # # #     self.score = self.__score_methods__[self.__name__](self.number_of_errors, self.number_of_values)
        # # # except Exception as e:
        # # #     print (e)
        # # # return self.score

        ## Compute MAIN Score
        nscore_method_used = 0
        for iscore in [self.levenshtein_score, self.nilsimsa_score, self.rmspe_score, self.mspe_score, self.mape_score, self.mpe_score, self.mrpd_score, self.quantity_score]:
            if iscore:
                self.score += iscore
                nscore_method_used += 1

        if self.score:
            self.score = self.score/nscore_method_used

    # 3
    def compute_differences (self):
        if not (self.original_file or self.new_file):
            self.errors.append("Method.compute_differences: Unknown files")
        
        try:
            # TODO
            block_diff = self.__difference_methods__[self.__name__](self.original_file, self.new_file)
            # print (block_diff)
            if block_diff["report"]: self.differences_report = block_diff["report"]
            self.number_of_values = block_diff["nvalues"]
            self.ndiff = block_diff["ndiff"]
            if block_diff["log"]: self.log = block_diff["log"]
            if block_diff["error"]: self.errors += block_diff["error"]
            if block_diff["advice"]: self.advices += block_diff["advice"]
            
            
        except Exception as e:
            self.log.append ("Method.compute_differences: " + str(error_handler.get_traceback(e)))
            self.errors.append ("Method.compute_differences: " + str(error_handler.get_traceback(e)))

    def topair (self, ipair):
        ipair["method"] = self.__name__
        ipair["error"] = self.errors
        ipair["log"] = self.log
        ipair["advice"] = self.advices
        ipair["score"] = self.score
        ipair["differences"] = self.differences_report
        ipair["number_of_errors"] = len(self.errors)
        ipair["number_of_values"] = self.number_of_values
        ipair["ndiff"] = self.ndiff
        
        ipair["mape_score"] = self.mape_score
        # ipair["rmse_score"] = self.rmse_score
        ipair["rmspe_score"] = self.rmspe_score
        ipair["levenshtein_score"] = self.levenshtein_score
        ipair["mspe_score"] = self.mspe_score
        ipair["mpe_score"] = self.mpe_score
        ipair["mrpd_score"] = self.mrpd_score
        
        ipair["max_delta"] = self.max_delta
        ipair["delta"] = self.delta
        # ipair["mse_score"] = self.mse_score
        ipair["quantity score"] = self.quantity_score
        ipair["hash score"] = self.hash_score
        
        
        
        return ipair

def get_adviced_method (ipair):
    
    # Guessing the file
    
    ########## NUMPY ##########
    # allow_pickle, bytes encoded
    try:
        data1 = numpy.load(ipair["Origin"]["path"], allow_pickle=True, encoding='bytes')
        data2 = numpy.load(ipair["New"]["path"], allow_pickle=True, encoding='bytes')

        ipair["method"] = "npz"
        ipair["Origin"]["encoding"] = "bytes"
        ipair["New"]["encoding"] = "bytes"
        ipair["Origin"]["allow_pickle"] = True
        ipair["New"]["allow_pickle"] = True
        return ipair
    except Exception as e:
        pass

    # allow_pickle, ascii encoded
    try:
        data1 = numpy.load(ipair["Origin"]["path"], allow_pickle=True, encoding='ASCII')
        data2 = numpy.load(ipair["New"]["path"], allow_pickle=True, encoding='ASCII')

        ipair["method"] = "npz"
        ipair["Origin"]["encoding"] = "ASCII"
        ipair["New"]["encoding"] = "ASCII"
        ipair["Origin"]["allow_pickle"] = True
        ipair["New"]["allow_pickle"] = True
        return ipair
    except Exception as e:
        pass

        ########## NEO ##########
    try:
        neo_reader1 = neo.io.get_io(ipair["Origin"]["path"])
        neo_reader2 = neo.io.get_io(ipair["New"]["path"])
        ipair["method"] =  "neo"
        ipair["Origin"]["encoding"] = None
        ipair["New"]["encoding"] = None
        ipair["Origin"]["allow_pickle"] = None
        ipair["New"]["allow_pickle"] = None
        return ipair

    except Exception as eneo:
        pass

        ########## TXT READABLE ##########
    try:
        f1 = open (ipair["Origin"]["path"], mode="r", encoding="utf-8")
        f2 = open (ipair["New"]["path"], mode="r", encoding="utf-8")
        ipair["method"] =  "txt"
        ipair["Origin"]["encoding"] = None
        ipair["New"]["encoding"] = None
        ipair["Origin"]["allow_pickle"] = None
        ipair["New"]["allow_pickle"] = None
        return ipair

    except Exception as etxt:
        pass

    ########## BYTES ##########
    ipair["method"] = "byte"
    ipair["Origin"]["encoding"] = None
    ipair["New"]["encoding"] = None
    ipair["Origin"]["allow_pickle"] = None
    ipair["New"]["allow_pickle"] = None

    return ipair