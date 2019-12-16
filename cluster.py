import os
import argparse
import csv

"""
Manage a list with possible "holes" for efficiency
"""
class ClusterList:
    def __init__(self):
        self.list = []
        self.free_indexes = []

    def add(self, s):
        if len(self.free_indexes) == 0:
            self.list.append(s)
        else:
            self.list[self.free_indexes[0]] = s
            self.free_indexes = self.free_indexes[1:]
    
    def remove(self, s):
        idx = self.list.index(s)
        self.list[idx] = None
        self.free_indexes += [idx]

    def __len__(self):
        return len(self.list)

    def clean(self):
        self.list = [x for x in self.list if x is not None]

    def __getitem__(self, index):
        return self.list[index]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split Quora Pair Question dataset in clusters')
    parser.add_argument("-i", "--input_file", required=True, type=str,
                        help="Quora dataset in CSV format")
    parser.add_argument("-o", "--output_clusters", required=True, type=str,
                        help="Output file in which each cluster will be saved, line by line")
    parser.add_argument("-q", "--output_question", required=True, type=str,
                        help="Output file in which the pair id-question will be saved")
    parser.add_argument("-f", "--force_overwrite", action="store_true",
                        help="Output files are overwritten if they already exists")
     
    args = parser.parse_args()

    input_file = args.input_file
    output_clusters = args.output_clusters
    output_question = args.output_question
    force = args.force_overwrite

    if not os.path.exists(input_file):
        print("Input file {} does not exists".format(input_file))
        exit(1)

    if os.path.exists(output_clusters):
        if force:
            os.remove(output_clusters)
        else:
            print("{} does already exists. Use -f option to overwrite it".format(output_clusters))
            exit(1)

    if os.path.exists(output_question):
        if force:
            os.remove(output_question)
        else:
            print("{} does already exists. Use -f option to overwrite it".format(output_question))
            exit(1)


    # Read CSV file
    mapping = dict()
    questions = dict()
    clusters = ClusterList()

    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)
        
        for i, row in enumerate(csv_reader):
            print("Elaborating line {}".format(i), end='\r')    
            
            # Extract data
            pair_id = int(row[0])
            qid_1 = int(row[1])
            qid_2 = int(row[2])
            question_1 = row[3]
            question_2 = row[4]
            is_duplicate = bool(int(row[5]))

            # Save question text
            if qid_1 not in questions:
                questions[qid_1] = question_1
            if qid_2 not in questions:
                questions[qid_2] = question_2

            # Get eventual cluster of each question
            cluster_1 = mapping[qid_1] if qid_1 in mapping else None
            cluster_2 = mapping[qid_2] if qid_2 in mapping else None

            # if both are not contained in some cluster
            if cluster_1 is None and cluster_2 is None:
                if is_duplicate:
                    new_cluster = set([qid_1, qid_2])
                    clusters.add(new_cluster)
                    mapping[qid_1] = new_cluster
                    mapping[qid_2] = new_cluster
                else:
                    new_cluster = set([qid_1])
                    clusters.add(new_cluster)
                    mapping[qid_1] = new_cluster
                    ####
                    new_cluster = set([qid_2])
                    clusters.add(new_cluster)
                    mapping[qid_2] = new_cluster

            # both are already in some cluster
            elif cluster_1 is not None and cluster_2 is not None:
                if is_duplicate and cluster_1 is not cluster_2:
                    clusters.remove(cluster_1)
                    clusters.remove(cluster_2)
                    new_cluster = cluster_1.union(cluster_2)
                    for qid in new_cluster:
                        mapping[qid] = new_cluster
                    clusters.add(new_cluster)

            # first is in some cluster and second is not
            elif cluster_1 is not None and cluster_2 is None:
                if is_duplicate:
                    cluster_1.add(qid_2)
                    mapping[qid_2] = cluster_1
                else:
                    new_cluster = set([qid_2])
                    clusters.add(new_cluster)

            # second is in some cluster and first is not
            elif cluster_1 is None and cluster_2 is not None:
                if is_duplicate:
                    cluster_2.add(qid_1)
                    mapping[qid_1] = cluster_2
                else:
                    new_cluster = set([qid_1])
                    clusters.add(new_cluster)
            
            else:
                print(cluster_1, cluster_2)
                raise ValueError("There is some problem")

    clusters.clean()

    with open(output_clusters, "w") as f:
        for c in clusters:
            f.write(",".join([str(x) for x in c]) + "\n")

    with open(output_question, "w") as f:
        for key, value in questions.items():
            f.write("{},{}\n".format(key, value))

    print()
    print("There are {} question divided in {} clusters".format(len(questions), len(clusters)))

