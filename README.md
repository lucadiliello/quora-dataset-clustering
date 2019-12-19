# Description

This repo addresses the problem of the <a href="https://www.kaggle.com/quora/question-pairs-dataset/data">Quora Questions Pair Dataset</a> in which some questions may appear both in the training set and in the validation or test set.
By mean of the transitive property over pair of questions:
```
a == b , b == c => a == c
```
we create clusters containing questions that are equivalent.
With this clusters, is then easy to split the original dataset in chunks (train, valid, test, ...) that do not have questions in common.

## How to

- Download the original dataset from <a href="https://www.kaggle.com/quora/question-pairs-dataset/data">here</a>
- Extract it
- Divide questions in clusters with `python cluster.py -i <downloaded-file> -o <output-cluster-file> -m <question-id-mappings-file>`. `<output-clusters-file>` will contain a cluster on each line. Each cluster will be a comma separated list of question ids. `<question-id-mappings-file>` will instead contain the mappings between ids and questions, one per line and comma separated.
- Split the cluster dataset into chunks with, for example, `python split.py -i <clusters-file> -s 10 10 40 40 -u 2 -o <output_folder>`. This will create a folder called `<output-folder>` containing 4 files with, respectively, the `10%`, `10%`, `40%` and `40%` of the original clusters. This is done in a balanced way so that the average size of clusters in each chunk is pretty much the same. The `-u k` option filters away clusters with less than `k` questions.
- Use `python generate.py -i <split-file> -m <question-id-mappings-file> -o <output-file> -r <true-false-ratio> -n <number of entries>` to join the id contained in `<split-file>` with the respective questions (thanks to `<question-id-mappings-file>`) and save the results in `<output-file>`. `-r <true-false-ratio>` is a float in [0, 1] which specify the ratio between `True` and `False` pairs while `-n <number of entries>` specify the number of entries that should be generated. `<number of entries>` is automatically limited if there are not enough entries and, by default, it is the max number of entries generable respecting the `-r` option.
- Finally, to generate a custom mapping file for each split, use `python mappings.py -i <split-file> -m <question-id-mappings-file> -o <split-mappings-file>`.


## Example

Suppose downloaded dataset is called `questions.csv`. Create clusters:

```bash
python cluster.py -i questions.csv -o clusters.csv -m mappings.csv
```

Split dataset in 3 parts with size `50%` `30%` `20%`, considering only clusters containing at least 3 questions:

```bash
python split.py -i clusters.csv -s 50 30 20 -u 3 -o splits_folder
```

Create the real datasets files with a balanced number of True and False pairs and automatic lenght detection
```bash
python generate.py -i splits_folder/0-50-split.csv -m mappings.csv -r 0.5 -o train.csv
python generate.py -i splits_folder/0-30-split.csv -m mappings.csv -r 0.5 -o test.csv
python generate.py -i splits_folder/0-20-split.csv -m mappings.csv -r 0.5 -o valid.csv
```

Create custom mappings for 0-50-split.csv split file with
```bash
python mappings.py -i splits_folder/0-50-split.csv -m mappings.csv -o splits_folder/0.50-split-mappings.csv
```