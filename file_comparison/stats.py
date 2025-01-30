# Statistics routines
import os
from nltk.metrics import edit_distance
import sklearn.metrics
import numpy as np
from file_comparison.nilsimsa import nilsimsa_str
import traceback
# import nltk.metrics.distance

error_diff_types = ["type", "len"]

# (origin - new) / origin
def core (origin, new):
    res = 0.
    try:
        res = (origin - new)/origin
    except Exception as e:
        print ("Core:")
        print(str("".join(traceback.format_exception(e))))
        if origin == 0. and origin == new:
            res = 0.
    return res

# (origin - new) / origin
def vcore (origin:np.ndarray, new:np.ndarray):
    
    res = np.divide (origin.astype(np.float64)-new.astype(np.float64), origin.astype(np.float64), out=np.full_like(origin.astype(np.float64), np.nan), where=origin!=0)

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
    return np.sqrt(mean_squared_percentage_error(origin=origin.astype(np.float64), new=new.astype(np.float64))/100.)*100.

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
def mean_relative_percentage_difference(origin:np.ndarray, new:np.ndarray):

    core = np.divide (np.abs(origin.astype(np.float64) - new.astype(np.float64), dtype=np.float64), ((origin.astype(np.float64) + new.astype(np.float64)).astype(np.float64)/2.), out=np.full_like(origin, np.nan), where=(((origin.astype(np.float64) + new.astype(np.float64))/2.)!=0))
    return np.nanmean (core)*100.
    

# Compute mean difference between two datasets
def delta (origin:np.ndarray, new:np.ndarray):
    return np.mean(np.absolute(origin.astype(np.float64) - new.astype(np.float64)))

# Compute maximum difference between two datasets
def maximum_delta (origin:np.ndarray, new:np.ndarray):
    return np.max(np.absolute(origin.astype(np.float64) - new.astype(np.float64)))

def mean_nilsimsa_distance(origin:np.ndarray, new:np.ndarray):
    nilsimsa_scores = np.full_like(origin, np.nan)
    for iel in range(min(len(origin), len(new))):
        nilsimsa_scores[iel] = nilsimsa_str(origin=str(origin[iel]), new=str(new[iel]))

    return np.nanmean(nilsimsa_scores)
        