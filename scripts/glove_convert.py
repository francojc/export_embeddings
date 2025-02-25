#!/usr/bin/env python

import numpy as np
import argparse
import os
from tqdm import tqdm

def convert_glove_to_embedding_projector(glove_file, output_dir=None, limit=None, dimensions=None, encoding='utf-8'):
    """
    Converts a GloVe text file to vectors.tsv and metadata.tsv files
    suitable for the TensorFlow Embedding Projector.

    Args:
        glove_file: Path to the GloVe text file.
        output_dir: Path to the output directory. If None, use current directory.
        limit: Optional. Only process the top 'limit' words.
               If None, process all words in the file.
        dimensions: Optional. Downscale embeddings to this dimension.
                    If None, keep original dimensions.
        encoding: File encoding (default: utf-8)
    """
    # Create output directory if it doesn't exist
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_dir = output_dir if output_dir else '.'

    # Track vocabulary and dimension
    words = []
    vectors = []

    # Read the GloVe file
    with open(glove_file, 'r', encoding=encoding) as f:
        lines = f.readlines()
        if limit:
            lines = lines[:limit]
            
        for line in tqdm(lines, desc="Processing words"):
            try:
                # Split line: first item is word, rest are vector values
                parts = line.strip().split()
                word = parts[0]
                vector = np.array([float(x) for x in parts[1:]])
                
                # Downscale if needed
                if dimensions is not None and dimensions < len(vector):
                    vector = vector[:dimensions]
                    
                words.append(word)
                vectors.append(vector)
            except (ValueError, IndexError) as e:
                print(f"Warning: Skipping invalid line: {line.strip()}")
                continue

    # Validate vector dimensions
    if len(vectors) > 0 and len(set(len(v) for v in vectors)) > 1:
        print("Warning: Inconsistent vector dimensions found!")
        
    vector_size = len(vectors[0]) if vectors else 0

    vectors_file = os.path.join(output_dir, 'vectors.tsv')
    metadata_file = os.path.join(output_dir, 'metadata.tsv')
    
    # Create README file
    readme_file = os.path.join(output_dir, 'README.md')
    with open(readme_file, 'w') as f_readme:
        f_readme.write("# Embedding Projector Files\n\n")
        f_readme.write("These files (`vectors.tsv` and `metadata.tsv`) are generated for use with the [TensorFlow Embedding Projector](https://projector.tensorflow.org/).\n\n")

    # Write vector TSV
    with open(vectors_file, 'w', encoding=encoding) as vec_file:
        for vector in vectors:
            vec_file.write('\t'.join(map(str, vector)) + '\n')

    # Write metadata TSV
    with open(metadata_file, 'w', encoding=encoding) as meta_file:
        meta_file.write("Word\n")  # Header required by Embedding Projector
        for word in words:
            meta_file.write(f"{word}\n")

    num_vectors = len(words)
    with open(readme_file, 'a') as f_readme:
        f_readme.write("## Statistics\n\n")
        f_readme.write(f"- Number of vectors: {num_vectors}\n")
        f_readme.write(f"- Vector dimension: {vector_size}\n")
        f_readme.write(f"- Number of unique words: {num_vectors}\n\n")
        f_readme.write(f"Vectors saved to `{vectors_file}`.\n")
        f_readme.write(f"Metadata saved to `{metadata_file}`.\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert GloVe embeddings to Embedding Projector format')
    parser.add_argument('glove_file', help='Path to input GloVe text file')
    parser.add_argument('--limit', type=int, help='Limit number of words to process (optional)')
    parser.add_argument('--dimensions', type=int, default=None, help='Downscale embeddings to this dimension (optional)')
    parser.add_argument('--output_dir', '-o', type=str, default=None, help='Path to the output directory (optional, default: current directory)')
    parser.add_argument('--encoding', default='utf-8', help='File encoding (default: utf-8)')

    args = parser.parse_args()

    convert_glove_to_embedding_projector(
        glove_file=args.glove_file,
        output_dir=args.output_dir,
        limit=args.limit,
        dimensions=args.dimensions,
        encoding=args.encoding
    )
