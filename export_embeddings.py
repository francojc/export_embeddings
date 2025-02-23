#!/usr/bin/env python

import argparse
import fasttext
import os
from tqdm import tqdm

def convert_fasttext_to_embedding_projector(bin_file, output_dir=None, limit=None, dimensions=None):
    """
    Converts a FastText .bin file to vectors.tsv and metadata.tsv files
    suitable for the TensorFlow Embedding Projector.

    Args:
        bin_file: Path to the FastText .bin file (model.bin).
        output_dir: Path to the output directory. If None, use current directory.
        limit: Optional.  Only process the top 'limit' most frequent words.
               If None, process all words in the model.
        dimensions: Optional.  Downscale embeddings to this dimension.
                    If None, keep original dimensions.
    """

    model = fasttext.load_model(bin_file)
    dimensions = dimensions or model.get_dimension()

    words = model.get_words()
    if limit is not None:
        words = words[:limit]

    vectors_file = os.path.join(output_dir if output_dir else '.', 'vectors.tsv')
    metadata_file = os.path.join(output_dir if output_dir else '.', 'metadata.tsv')
    with open(vectors_file, 'w') as f_vec, open(metadata_file, 'w', encoding='utf-8') as f_meta:
        readme_file = os.path.join(output_dir if output_dir else '.', 'README.md')
        with open(readme_file, 'w') as f_readme:
            f_readme.write("# Embedding Projector Files\n\n")
            f_readme.write("These files (`vectors.tsv` and `metadata.tsv`) are generated for use with the [TensorFlow Embedding Projector](https://projector.tensorflow.org/).\n\n")

        # Write header to metadata file
        f_meta.write("Word\n")  # Header is required by the Embedding Projector

        for word in tqdm(words, desc="Processing words"):
            vector = model.get_word_vector(word)  # type: ignore (fasttext stubs incomplete)
            if dimensions is not None and dimensions < len(vector):
                vector_downscaled = vector[:dimensions]
                vector_str = '\t'.join(map(str, vector_downscaled))
            else:
                vector_str = '\t'.join(map(str, vector))
            f_vec.write(f"{vector_str}\n")
            f_meta.write(f"{word}\n")

        num_vectors = len(words)
        with open(readme_file, 'a') as f_readme:
            f_readme.write("## Statistics\n\n")
            f_readme.write(f"- Number of vectors: {num_vectors}\n")
            f_readme.write(f"- Vector dimension: {dimensions}\n")
            f_readme.write(f"- Number of unique words: {num_vectors}\n\n")
            f_readme.write(f"Vectors saved to `{vectors_file}`.\n")
            f_readme.write(f"Metadata saved to `{metadata_file}`.\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert FastText .bin model to Embedding Projector files.')
    parser.add_argument('bin_file', help='Path to the FastText .bin file (model.bin)')
    parser.add_argument('--limit', type=int, help='Limit the number of words to process (optional)')
    parser.add_argument('--dimensions', type=int, default=None, help='Downscale embeddings to this dimension (optional)')
    parser.add_argument('--output_dir', '-o', type=str, default=None, help='Path to the output directory (optional, default: current directory)')

    args = parser.parse_args()

    convert_fasttext_to_embedding_projector(
        bin_file=args.bin_file,
        output_dir=args.output_dir,
        limit=args.limit,
        dimensions=args.dimensions
    )
