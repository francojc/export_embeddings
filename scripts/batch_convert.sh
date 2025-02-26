#!/usr/bin/env bash

# This script runs the various *_convert.py scripts for the given input files and directories
#
# Usage: ./scripts/batch_convert.sh


# FastText models
./scripts/fasttext_convert.py ./models/English/cc.en.300.bin  --output_dir ./output/English/ --limit 100000
./scripts/fasttext_convert.py ./models/Dutch/cc.nl.300.bin  --output_dir ./output/Dutch/ --limit 100000
./scripts/fasttext_convert.py ./models/Swedish/cc.sv.300.bin  --output_dir ./output/Swedish/ --limit 100000
./scripts/fasttext_convert.py ./models/Arabic/cc.ar.300.bin  --output_dir ./output/Arabic/ --limit 100000
./scripts/fasttext_convert.py ./models/Icelandic/cc.is.300.bin  --output_dir ./output/Icelandic/ --limit 100000

# GloVe models
./scripts/glove_convert.py ./models/Twitter/glove.twitter.27B.200d.txt  --output_dir ./output/Twitter/ --limit 100000 --dimensions 200


# Word2Vec models
./scripts/gensim_convert.py ./models/Icelandic/ICE/
