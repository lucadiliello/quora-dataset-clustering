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
    new_clusters = [cluster for cluster in clusters if len(cluster) >= min_cluster_size]

    print("Filtered {} out of {} clusters because of size smaller than {}".format(
        len(clusters) - len(new_clusters), len(clusters), min_cluster_size))
    clusters = new_clusters
            
    # shuffle dataset on the first row
    random.shuffle(clusters)

    last_index = 0
    splitted = []
    for index, value in enumerate(splits): 
        if index == (len(splits) - 1):
            data = clusters[last_index:]
        else:
            split_len = value * len(clusters) // 100
            data = clusters[last_index: last_index + split_len]
            last_index += split_len
        splitted.append(data)
    
    print("Created {} splits with size {}".format(len(splitted), [len(x) for x in splitted]))
    print("Splitting done!")

    return splitted

    
