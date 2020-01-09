"""
Given a set of clusters, generate a dataset with a specified number of true or false labels.
"""

import os
import argparse
import csv
import random

def generate(input_data, mapping, ratio=0.5, max_number=None):
    print("Starting generation")
    # use first id
    mapping = {value[0]: key for (key, value) in mapping.items()}
    if max_number is None or len(max_number) == 0:
        max_number = [None] * len(input_data)

    res = [_generate(z[0], mapping, ratio=ratio, max_number=z[1]) for z in zip(input_data, max_number)]
    print("Generation done!")
    return res


def _generate(input_data, mapping, ratio=0.5, max_number=None):
        
    res = []
    # adding positive candidates
    for cluster in input_data:
        if len(cluster) > 1:
            for i in range(len(cluster)):
                for j in range(i+1, len(cluster)):
                    res.append([cluster[i], cluster[j], mapping[cluster[i]], mapping[cluster[j]], True])

    false_needed = int(len(res) / ratio)
    
    # adding negative candidates
    for i in range(false_needed):

        cluster1, cluster2 = random.sample(input_data, 2)
        qid1 = random.choice(cluster1)
        qid2 = random.choice(cluster2)
        res.append(
            [qid1, qid2, mapping[qid1], mapping[qid2], False]
        )

    random.shuffle(res)
    # if specified N is bigger than available data, keep actual size
    if max_number is not None:
        res = res[:min(max_number, len(res))]    
    
    return res
    
    
