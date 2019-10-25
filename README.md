# Indexing, Querying, Inference and other stuff

### Dependencies
There are no dependencies to be downloaded, all libraries used are bundled in Python

### Build
To build and store the index on disk, please run the following commands:
- For uncompressed index
```
python run_indexer.py --compressed 0
```
- For compressed index
```
python run_indexer.py --compressed 1
```

### Evaluation
To run the evaluation and timing experiments, please run the following commands:
- For only uncompressed index
```
python evaluation.py --compressed 0 --uncompressed 1
```
- For only compressed index
```
python evaluation.py --compressed 1 --uncompressed 0
```
- For both
```
python evaluation.py --compressed 1 --uncompressed 1
OR
python evaluation.py
```

If running on Linux / MacOS, you may have to replace `python` with `python3`
