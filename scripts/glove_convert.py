#!/usr/bin/env python

import numpy as np
import argparse
import os

def convert_glove_to_projector(glove_input_path, vector_output_path='vectors.tsv',
                                metadata_output_path='metadata.tsv',
                                encoding='utf-8',
                                limit=None):
    """
    Convert GloVe text format embeddings to TensorFlow Embedding Projector format.

    Parameters:
    - glove_input_path: Path to the input GloVe text file
    - vector_output_path: Path to save vector TSV file
    - metadata_output_path: Path to save metadata TSV file
    - encoding: File encoding (default: utf-8)
    - limit: Optional limit on number of words to convert
    """
    print(f"Converting GloVe model from {glove_input_path}...")

    # Track vocabulary and dimension
    words = []
    vectors = []

    # Read the GloVe file
    with open(glove_input_path, 'r', encoding=encoding) as f:
        for line_num, line in enumerate(f):
            # Skip limit if specified
            if limit and line_num >= limit:
                break

            try:
                # Split line: first item is word, rest are vector values
                parts = line.strip().split()
                word = parts[0]
                vector = np.array([float(x) for x in parts[1:]])

                words.append(word)
                vectors.append(vector)

            except (ValueError, IndexError) as e:
                print(f"Warning: Skipping invalid line {line_num}: {line.strip()}")
                continue

    # Validate vector dimensions
    if len(set(len(v) for v in vectors)) > 1:
        print("Warning: Inconsistent vector dimensions found!")

    # Print conversion info
    print(f"Converted {len(words)} words")
    print(f"Vector dimension: {len(vectors[0])}")

    # Write vector TSV
    with open(vector_output_path, 'w', encoding=encoding) as vec_file:
        for vector in vectors:
            vec_file.write('\t'.join(map(str, vector)) + '\n')

    # Write metadata TSV
    with open(metadata_output_path, 'w', encoding=encoding) as meta_file:
        meta_file.write("word\n")  # Header
        for word in words:
            meta_file.write(f"{word}\n")

    print(f"Vectors saved to: {os.path.abspath(vector_output_path)}")
    print(f"Metadata saved to: {os.path.abspath(metadata_output_path)}")

def main():
    parser = argparse.ArgumentParser(description='Convert GloVe embeddings to Embedding Projector format')
    parser.add_argument('input_path', help='Path to input GloVe text file')
    parser.add_argument('--vectors', default='vectors.tsv',
                        help='Output path for vectors (default: vectors.tsv)')
    parser.add_argument('--metadata', default='metadata.tsv',
                        help='Output path for metadata (default: metadata.tsv)')
    parser.add_argument('--encoding', default='utf-8',
                        help='File encoding (default: utf-8)')
    parser.add_argument('--limit', type=int,
                        help='Limit number of words to convert')

    args = parser.parse_args()

    convert_glove_to_projector(
        args.input_path,
        args.vectors,
        args.metadata,
        args.encoding,
        args.limit
    )

if __name__ == '__main__':
    main()
