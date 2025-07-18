# Statistics routines
import os
from nltk.metrics import edit_distance
import sklearn.metrics
import numpy as np
from file_comparison.nilsimsa import nilsimsa_str
import file_comparison.error_handler as error_handler
# import nltk.metrics.distance

error_diff_types = ["type", "len"]

# (origin - new) / origin
def core (origin, new):
    res = 0.
    try:
        res = (origin - new)/origin
    except Exception as e:
        print ("Core:")
        print(str(error_handler.get_traceback(e)))
        if origin == 0. and origin == new:
            res = 0.
    return res

# (origin - new) / origin
def vcore (origin:np.ndarray, new:np.ndarray):
    
    res = np.divide (origin - new, origin, out=np.full_like(origin, np.nan), where=origin!=0)

    return res

def mean_levenshtein_distance_percentage (origin:np.ndarray, new:np.ndarray) -> float:
    n = min(len(origin), len(new))
    lev_max_scores = []
    # Compute Levenshtein maximum scores
    for iel in range(n):
        lev_max_scores.append(max(len(str(origin[iel])), len(str(new[iel]))))

    distance_percentage = 0.
    for iel in range(n):
        distance_percentage += edit_distance(str(origin[iel]), str(new[iel]))*100./lev_max_scores[iel]
    mean_distance_percentage = distance_percentage / n if n else None

    return mean_distance_percentage

# MAPE
# Compute Mean Absolute Percentage Error between two values
def mean_absolute_percentage_error(origin:np.ndarray, new:np.ndarray):
    # Can't use sklearn.metrics.mean_absolute_percentage_error because
    # zero division return random high number
    # return sklearn.metrics.mean_absolute_percentage_error(origin, new)*100.

    # MAPE Numpy implement instead
    core = np.absolute(vcore(origin=origin, new=new))
    return np.nanmean(core) * 100.


# MSPE
# Compute Mean Squared Percentage Error between two values
def mean_squared_percentage_error(origin:np.ndarray, new:np.ndarray):
    core = vcore(origin=origin, new=new)
    core = np.square(core, where=core!=np.nan, out=np.full_like(core, np.nan))
    return np.nanmean(core)*100.

# RMSPE
# Compute Root Mean Squared Percentage Error between two lists
def root_mean_squared_percentage_error(origin:np.ndarray, new:np.ndarray):
    return np.sqrt(mean_squared_percentage_error(origin=origin, new=new)/100.)*100.

# MSE  
# Compute Mean Squared Error between two lists
# def mean_squared_error(origin:np.ndarray, new:np.ndarray):
#     return np.mean(np.square(origin - new), axis=0)

# RMSE
# Compute Root Mean Squared Error between two lists
# def root_mean_squared_error(origin:np.ndarray, new:np.ndarray):
#     return np.sqrt(np.mean(np.square(origin - new), axis=0))

# MPE
# Compute Mean Percentage Error between two lists
def mean_percentage_error(origin:np.ndarray, new:np.ndarray):
    
    core = vcore(origin=origin, new=new)
    return np.nanmean(core)*100.

# MRPD
# Compute Mean Relative Percentage Difference between two lists
# TO FIX
def mean_relative_percentage_difference(origin:np.ndarray, new:np.ndarray):

    core = np.divide (np.abs(origin - new), ((origin + new)/2.), out=np.full_like(origin, np.nan), where=(((origin + new)/2.)!=0))
    
    return np.nanmean (core)*100.
    

# Compute mean difference between two datasets
def delta (origin:np.ndarray, new:np.ndarray):
    return np.mean(np.absolute(origin - new))

# Compute maximum difference between two datasets
def maximum_delta (origin:np.ndarray, new:np.ndarray):
    return np.max(np.absolute(origin - new))

# Compute nilsimsa distance between two strings
def mean_nilsimsa_distance(origin:np.ndarray, new:np.ndarray):
    nilsimsa_scores = np.full_like(origin, np.nan)
    for iel in range(min(len(origin), len(new))):
        nilsimsa_scores[iel] = nilsimsa_str(origin=str(origin[iel]), new=str(new[iel]))

    return np.nanmean(nilsimsa_scores)

# Count the number of value differences
def count_diffs (origin:np.ndarray, new:np.ndarray):
    ndiff = 0
    error = []
    for iel in range(min(len(origin), len(new))):
        try:
            if origin[iel] != new[iel]:
                ndiff += 1
        except Exception as e:
            error.append("report_generator - Count differences: " + str(type(origin[iel])) + " - " + str(type(new[iel])) + " " + str(error_handler.get_traceback(e)))

    return ndiff, error