"""
Given a set of clusters, generate a dataset with a specified number of true or false labels.
"""

import os
import argparse
import csv
import random
import math

def generate(input_data, mapping, ratio=0.5, max_number=None, hard_negative=None, translations=None):
    print("Starting generation")

    # use first id
    inverse_mapping = {value[0]: key for (key, value) in mapping.items()}

    if translations is not None:
        print("Cleaning from questions without translation")
        tmp = []
        for split in input_data:
            tmp_split = []
            for cluster in split:
                tmp_cluster = []
                for qid in cluster:
                    all_ids = mapping[inverse_mapping[qid]]   
                    if any([x in translations for x in all_ids]):
                        tmp_cluster.append(qid)
                if len(tmp_cluster) > 0:
                    tmp_split.append(tmp_cluster)
            if len(tmp_split) > 0:
                tmp.append(tmp_split)
        input_data = tmp

    if max_number is None or len(max_number) == 0:
        max_number = [None] * len(input_data)

    res = [_generate(data, inverse_mapping, ratio=ratio, hard_negative=hard_negative, max_number=max_n) for data, max_n in zip(input_data, max_number)]
    print("Generation done!")
    return res


def _generate(input_data, inverse_mapping, ratio=0.5, hard_negative=None, max_number=None):

    res = []

    if hard_negative is None:
        # adding positive candidates
        for cluster in input_data:
            if len(cluster) > 1:
                for i in range(len(cluster)):
                    for j in range(i+1, len(cluster)):
                        res.append([cluster[i], cluster[j], inverse_mapping[cluster[i]], inverse_mapping[cluster[j]], True])

        false_needed = int(len(res) / ratio)
        
        # adding negative candidates
        for i in range(false_needed):

            cluster1, cluster2 = random.sample(input_data, 2)
            qid1 = random.choice(cluster1)
            qid2 = random.choice(cluster2)
            res.append(
                [qid1, qid2, inverse_mapping[qid1], inverse_mapping[qid2], False]
            )
        random.shuffle(res)

        if max_number is not None:
            res = res[:min(max_number, len(res))]

    else:
        for cluster in input_data:
            if len(cluster) > 1:
                for i in range(len(cluster)):
                    for j in range(i+1, len(cluster)):
                        tmp = []
                        tmp.append(
                            [cluster[i], cluster[j], inverse_mapping[cluster[i]], inverse_mapping[cluster[j]], True]
                        )
                        for cc in random.sample(input_data, hard_negative - 1):
                            qid = random.choice(cc)
                            tmp.append(
                                [cluster[i], qid, inverse_mapping[cluster[i]], inverse_mapping[qid], False]
                            )
                        res.append(tmp)
        random.shuffle(res)
        res = [item for sublist in res for item in sublist]
    
        # if specified N is bigger than available data, keep actual size
        if max_number is not None:
            if max_number % hard_negative != 0:
                max_number = math.ceil(max_number / hard_negative) * hard_negative 
            res = res[:min(max_number, len(res))] 
    
    return res
    
    
