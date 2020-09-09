"""
Given a dataset of question pairs, create a list of clusters such that
questions in the same cluster are labelled as duplicates (have the same meaning).
"""

import os
import argparse
import csv
import tqdm

# for testing purposes
def all_disjoint(sets):
    union = set()
    for s in sets:
        for x in s:
            if x in union:
                return False
            union.add(x)
    return True


class ClusterList:
    """
    Manage a list with possible "holes" for efficiency
    """
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
        self.free_indexes.append(idx)

    def __len__(self):
        return len(self.list)

    def clean(self):
        self.list = [x for x in self.list if x is not None]
        self.free_indexes = []

    def __getitem__(self, index):
        return self.list[index]

    def __str__(self):
        return str(self.list)


def cluster(input_data):

    print("Starting clustering...")

    # Read CSV file
    mapping = dict()
    questions = dict()
    clusters = ClusterList()
        
    for i, row in tqdm.tqdm(enumerate(input_data), desc="Clustering"):  

        # Extract data
        qid_1 = int(row[1])
        qid_2 = int(row[2])
        question_1 = row[3].strip()
        question_2 = row[4].strip()
        is_duplicate = bool(int(row[5].strip()))

        # If the questions are the same
        if question_1 == question_2:

            # Save question text, use map from text to ids to find questions with more than 1 id
            if question_1 not in questions:
                questions[question_1] = [qid_1]
            else:
                if qid_1 not in questions[question_1]:
                    questions[question_1].append(qid_1)
                if qid_2 not in questions[question_1]:
                    questions[question_1].append(qid_2)
                # Use first id found for each question
                qid_1 = questions[question_1][0]

            # Get eventual cluster of the question
            cluster_1 = mapping[qid_1] if qid_1 in mapping else None

            # if both are not contained in some cluster
            if cluster_1 is None:
                new_cluster = set([qid_1])
                clusters.add(new_cluster)
                mapping[qid_1] = new_cluster

        else:
            # Save question text, use map from text to ids to find questions with more than 1 id
            if question_1 not in questions:
                questions[question_1] = [qid_1]
            else:
                if qid_1 not in questions[question_1]:
                    questions[question_1].append(qid_1)
                # Use first id found for each question
                qid_1 = questions[question_1][0]
            
            if question_2 not in questions:
                questions[question_2] = [qid_2]
            else:
                if qid_2 not in questions[question_2]:
                    questions[question_2].append(qid_2)
                # Use first id found for each question
                qid_2 = questions[question_2][0]
                
            # Get eventual cluster of each question
            cluster_1 = mapping[qid_1] if qid_1 in mapping else None
            cluster_2 = mapping[qid_2] if qid_2 in mapping else None
                
            # if both are not contained in some cluster
            if (cluster_1 is None) and (cluster_2 is None):
                if is_duplicate:
                    new_cluster = set([qid_1, qid_2])
                    clusters.add(new_cluster)
                    mapping[qid_1] = new_cluster
                    mapping[qid_2] = new_cluster
                else:
                    new_cluster = set([qid_1])
                    clusters.add(new_cluster)
                    mapping[qid_1] = new_cluster
                    
                    new_cluster = set([qid_2])
                    clusters.add(new_cluster)
                    mapping[qid_2] = new_cluster

            # both are already in some cluster
            elif (cluster_1 is not None) and (cluster_2 is not None):
                if is_duplicate and (cluster_1 is not cluster_2):
                    clusters.remove(cluster_1)
                    clusters.remove(cluster_2)
                    new_cluster = cluster_1.union(cluster_2)
                    for qid in new_cluster:
                        mapping[qid] = new_cluster
                    clusters.add(new_cluster)

            # first is in some cluster and second is not
            elif (cluster_1 is not None) and (cluster_2 is None):
                if is_duplicate:
                    cluster_1.add(qid_2)
                    mapping[qid_2] = cluster_1
                else:
                    new_cluster = set([qid_2])
                    clusters.add(new_cluster)
                    mapping[qid_2] = new_cluster

            # second is in some cluster and first is not
            elif (cluster_1 is None) and (cluster_2 is not None):
                if is_duplicate:
                    cluster_2.add(qid_1)
                    mapping[qid_1] = cluster_2
                else:
                    new_cluster = set([qid_1])
                    clusters.add(new_cluster)
                    mapping[qid_1] = new_cluster
            
            else:
                print(cluster_1, cluster_2)
                raise ValueError("There is some problem...")
        
    clusters.clean()
    clusters = [list(x) for x in clusters]
    
    print("Clusters are all disjoint: {}".format(all_disjoint(clusters)))
    print("There are {} unique questions divided in {} clusters".format(len(questions), len(clusters)))
    print("Clustering done!")

    return clusters, questions

