import os
import argparse
import csv
from random import shuffle
import shutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split clusters generated with cluster.py in train/valid/test sets')
    parser.add_argument("-i", "--input_file", required=True, type=str,
                        help="Clusters dataset in CSV format")
    parser.add_argument("-s", "--splits", required=True, nargs='+', type=int,
                        help="List of splits in which the clusters should be divided in a balanced way"
                        "E.g. 10 10 40 40")
    parser.add_argument("-u", "--min_cluster_size", required=False, default=1, type=int,
                        help="Consider only clusters with a size >= than argument")
    parser.add_argument("-o", "--output_folder", type=str, required=True,
                        help="The folder in which results should be saved")
    parser.add_argument("-f", "--force_overwrite", action="store_true",
                        help="Output files are overwritten if they already exists")
     
    args = parser.parse_args()

    input_file = args.input_file
    splits = args.splits
    output_folder = args.output_folder
    force = args.force_overwrite
    min_cluster_size = args.min_cluster_size

    assert sum([int(x) for x in splits]) == 100, "Splits MUST sum to 100"

    if not os.path.exists(input_file):
        print("Input file {} does not exists".format(input_file))
        exit(1)

    if os.path.exists(output_folder):
        if force:
            shutil.rmtree(output_folder)
        else:
            print("{} does already exists. Use -f option to overwrite it".format(output_folder))
            exit(1)
    os.mkdir(output_folder)
    
    clusters = []
    filtered = 0
    tot = 0
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        for i, row in enumerate(csv_reader):
            if len(row) >= min_cluster_size:
                clusters.append(row)
            else:
                filtered += 1  
            tot += 1  

    print("Filtered {} out of {} clusters because of len size less than {}".format(filtered, tot, min_cluster_size))
            
    # shuffle dataset on the first row
    shuffle(clusters)

    last_index = 0
    for i, s in enumerate(splits):
        filepath = os.path.join(output_folder, "{}-{}-split.csv".format(i, s))

        split_len = s * len(clusters) // 100
        data = clusters[last_index : last_index + split_len]
        last_index += split_len

        with open(filepath, "w") as f:
            for c in data:
                f.write(",".join(c) + "\n")

    print("Done!")

    
