"""
Given a file containing a list of clusters, split them in different files with the
given size such that a question appears only in a cluster.
"""

import os
import argparse
import csv
import random
import shutil

def split(clusters, min_cluster_size=2, splits=[50,30,20]):
    
    print("Starting splitting...")
    filtered = 0
    tot = 0
    new_clusters = []

    for i, row in enumerate(clusters):
        if len(row) >= min_cluster_size:
            new_clusters.append(row)
        else:
            filtered += 1  
        tot += 1

    clusters = new_clusters

    print("Filtered {} out of {} clusters because of size smaller than {}".format(filtered, tot, min_cluster_size))
            
    # shuffle dataset on the first row
    random.shuffle(clusters)

    last_index = 0
    splitted = []
    for i, s in enumerate(splits): 
        if i == len(splits) - 1:
            data = clusters[last_index:]
        else:
            split_len = s * len(clusters) // 100
            last_index += split_len
            data = clusters[last_index: last_index + split_len]
        splitted.append(data)
    
    print("Created {} splits with size {}".format(len(splitted), [len(x) for x in splitted]))
    print("Splitting done!")

    return splitted

    
