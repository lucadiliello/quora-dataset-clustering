"""
Given a set of clusters, generate a dataset with a specified number of true or false labels.
"""
#######################################
#TODOS
#####

import os
import argparse
import csv
import random

def translate(datasets, translation, mapping):
    print("Starting translation...")
    res = [_translate(x, translation, mapping) for x in datasets]
    print("Translation done!") 
    return res

def _translate(dataset, translation, mapping):
    # dataset: 3123, 5566, "Am I italian?", "Am I english?", False
    res = []
    for row in dataset:
        id_1, id_2 = None, None

        for alternative_id in mapping[row[2]]:
            if alternative_id in translation:
                id_1 = alternative_id
                break
        for alternative_id in mapping[row[3]]:
            if alternative_id in translation:
                id_2 = alternative_id
                break

        if id_1 is None:
            print("Warning: the sentence '{}' has no translation".format(row[2]))
            continue
        elif id_2 is None:
            print("Warning: the sentence '{}' has no translation".format(row[3]))
            continue
        else:
            res.append([row[0], row[1], translation[id_1], translation[id_2], row[4]])

    return res
    
