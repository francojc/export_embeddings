# Word Embedding Converter

A collection of Python scripts to convert various word embedding formats to the TensorFlow Embedding Projector format.

## Supported Formats

- **GloVe**: Convert GloVe text format embeddings
- **FastText**: Convert FastText binary (.bin) models
- **Gensim**: Convert Gensim Word2Vec models (.model, .kv, or word2vec format)

## Installation

```bash
# Install required dependencies
pip install numpy tqdm gensim fasttext
```

## Usage

### GloVe Conversion

```bash
python scripts/glove_convert.py path/to/glove/vectors.txt --output_dir output/glove --limit 10000 --dimensions 100
```

### FastText Conversion

```bash
python scripts/fasttext_convert.py path/to/fasttext/model.bin --output_dir output/fasttext --limit 10000 --dimensions 100
```

### Gensim Conversion

```bash
python scripts/gensim_convert.py path/to/gensim/model.kv --output_dir output/gensim --limit 10000 --dimensions 100
```

## Common Parameters

All conversion scripts support these parameters:

- `--output_dir`: Directory to save output files (default: current directory)
- `--limit`: Limit the number of words to process
- `--dimensions`: Downscale embeddings to this dimension

## Output

Each script generates:

1. `vectors.tsv`: Tab-separated file containing vector values
2. `metadata.tsv`: Tab-separated file containing word labels
3. `README.md`: Information about the conversion

## Visualizing Embeddings

Upload the generated files to the [TensorFlow Embedding Projector](https://projector.tensorflow.org/) to visualize your word embeddings.
