#!/usr/bin/env bash

# This script runs the various *_convert.py scripts for the given input files and directories
#
# Usage: ./scripts/batch_convert.sh


# FastText models
./scripts/fasttext_convert.py ./models/English/cc.en.300.bin  --output_dir ./output/English/ --limit 100000
./scripts/fasttext_convert.py ./models/Dutch/cc.nl.300.bin  --output_dir ./output/Dutch/ --limit 100000
./scripts/fasttext_convert.py ./models/Swedish/cc.sv.300.bin  --output_dir ./output/Swedish/ --limit 100000
./scripts/fasttext_convert.py ./models/Arabic/cc.ar.300.bin  --output_dir ./output/Arabic/ --limit 100000

# GloVe models
./scripts/glove_convert.py


# Word2Vec models
./scripts/gensim_convert.py
