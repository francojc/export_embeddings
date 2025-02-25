#!/usr/bin/env python

import argparse
import os
from gensim.models import KeyedVectors
from tqdm import tqdm


def convert_gensim_to_embedding_projector(model_file, output_dir=None, limit=None, dimensions=None):
    """
    Converts a Gensim model file to vectors.tsv and metadata.tsv files
    suitable for the TensorFlow Embedding Projector.

    Args:
        model_file: Path to the Gensim model file (.model, .kv, or word2vec format).
        output_dir: Path to the output directory. If None, use current directory.
        limit: Optional. Only process the top 'limit' most frequent words.
               If None, process all words in the model.
        dimensions: Optional. Downscale embeddings to this dimension.
                    If None, keep original dimensions.
    """

    # Load the model
    model = KeyedVectors.load_word2vec_format(model_file) if model_file.endswith(('.txt', '.vec', '.bin')) else KeyedVectors.load(model_file)

    # If model is Word2Vec, get its word vectors
    if hasattr(model, 'wv'):
        model = model.wv

    # Create output directory if it doesn't exist
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_dir = output_dir if output_dir else '.'

    # Get all words from the model (compatible with both Gensim 3.x and 4.x)
    if hasattr(model, 'key_to_index'):
        # Gensim 4.x
        words = list(model.key_to_index.keys())
    elif hasattr(model, 'vocab'):
        # Gensim 3.x
        words = list(model.vocab.keys())
    else:
        raise ValueError("Cannot determine vocabulary structure of the model")

    # Sort words by frequency if available, otherwise keep as is
    try:
        if hasattr(model, 'get_vecattr'):
            # Gensim 4.x approach
            try:
                words = sorted(words, key=lambda w: model.get_vecattr(w, 'count'), reverse=True)
            except KeyError:
                pass
        elif hasattr(model, 'vocab'):
            # Gensim 3.x approach
            words = sorted(words, key=lambda w: model.vocab[w].count, reverse=True)
    except (AttributeError, KeyError):
        # If sorting fails for any reason, keep original order
        pass

    # Apply limit if specified
    if limit is not None:
        words = words[:limit]

    # Get vector dimension
    vector_size = dimensions or model.vector_size

    vectors_file = os.path.join(output_dir, 'vectors.tsv')
    metadata_file = os.path.join(output_dir, 'metadata.tsv')

    with open(vectors_file, 'w') as f_vec, open(metadata_file, 'w', encoding='utf-8') as f_meta:
        readme_file = os.path.join(output_dir, 'README.md')
        with open(readme_file, 'w') as f_readme:
            f_readme.write("# Embedding Projector Files\n\n")
            f_readme.write("These files (`vectors.tsv` and `metadata.tsv`) are generated for use with the [TensorFlow Embedding Projector](https://projector.tensorflow.org/).\n\n")

        # Write header to metadata file
        f_meta.write("Word\n")  # Header is required by the Embedding Projector

        for word in tqdm(words, desc="Processing words"):
            vector = model[word]  # Get the word vector

            # Downscale if needed
            if dimensions is not None and dimensions < len(vector):
                vector = vector[:dimensions]

            vector_str = '\t'.join(map(str, vector))
            f_vec.write(f"{vector_str}\n")
            f_meta.write(f"{word}\n")

        num_vectors = len(words)
        with open(readme_file, 'a') as f_readme:
            f_readme.write("## Statistics\n\n")
            f_readme.write(f"- Number of vectors: {num_vectors}\n")
            f_readme.write(f"- Vector dimension: {vector_size}\n")
            f_readme.write(f"- Number of unique words: {num_vectors}\n\n")
            f_readme.write(f"Vectors saved to `{vectors_file}`.\n")
            f_readme.write(f"Metadata saved to `{metadata_file}`.\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Gensim model to Embedding Projector files.')
    parser.add_argument('model_file', help='Path to the Gensim model file (.model, .kv, or word2vec format)')
    parser.add_argument('--limit', type=int, help='Limit the number of words to process (optional)')
    parser.add_argument('--dimensions', type=int, default=None, help='Downscale embeddings to this dimension (optional)')
    parser.add_argument('--output_dir', '-o', type=str, default=None, help='Path to the output directory (optional, default: current directory)')

    args = parser.parse_args()

    convert_gensim_to_embedding_projector(
        model_file=args.model_file,
        output_dir=args.output_dir,
        limit=args.limit,
        dimensions=args.dimensions
    )
