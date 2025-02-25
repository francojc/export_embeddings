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
                
                # Store original vector for dimension check
                words.append(word)
                vectors.append(vector)
            except (ValueError, IndexError) as e:
                print(f"Warning: Skipping invalid line: {line.strip()}")
                continue

    # Validate vector dimensions and ensure words and vectors stay in sync
    if len(vectors) > 0:
        # Check for inconsistent dimensions
        vector_lengths = [len(v) for v in vectors]
        if len(set(vector_lengths)) > 1:
            print("Warning: Inconsistent vector dimensions found in the input file!")
            # Use the most common dimension
            from collections import Counter
            dim_counts = Counter(vector_lengths)
            most_common_dim = dim_counts.most_common(1)[0][0]
            print(f"Using the most common dimension: {most_common_dim}")
            
            # Filter vectors and words to only include those with the most common dimension
            valid_pairs = [(w, v) for w, v in zip(words, vectors) if len(v) == most_common_dim]
            if not valid_pairs:
                raise ValueError("No vectors with consistent dimensions found!")
                
            # Unpack the filtered pairs
            words, vectors = zip(*valid_pairs)
            words = list(words)  # Convert back to list for later modification
            vectors = list(vectors)
            
            print(f"Kept {len(words)} vectors with consistent dimensions")
        
        # Apply dimension reduction if needed
        if dimensions is not None and vectors and dimensions < len(vectors[0]):
            vectors = [v[:dimensions] for v in vectors]
            vector_size = dimensions
        else:
            vector_size = len(vectors[0]) if vectors else 0
    else:
        print("Warning: No vectors were loaded!")
        vector_size = 0

    vectors_file = os.path.join(output_dir, 'vectors.tsv')
    metadata_file = os.path.join(output_dir, 'metadata.tsv')
    
    # Create README file
    readme_file = os.path.join(output_dir, 'README.md')
    with open(readme_file, 'w') as f_readme:
        f_readme.write("# Embedding Projector Files\n\n")
        f_readme.write("These files (`vectors.tsv` and `metadata.tsv`) are generated for use with the [TensorFlow Embedding Projector](https://projector.tensorflow.org/).\n\n")

    # Ensure we have the same number of words and vectors
    if len(words) != len(vectors):
        print(f"Warning: Mismatch between number of words ({len(words)}) and vectors ({len(vectors)})")
        # Truncate to the shorter length
        min_len = min(len(words), len(vectors))
        words = words[:min_len]
        vectors = vectors[:min_len]
        print(f"Truncated to {min_len} entries")

    # Write vector TSV
    with open(vectors_file, 'w', encoding=encoding) as vec_file:
        for vector in vectors:
            vec_file.write('\t'.join(map(str, vector)) + '\n')

    # Write metadata TSV
    with open(metadata_file, 'w', encoding=encoding) as meta_file:
        meta_file.write("Word\n")  # Header required by Embedding Projector
        for word in words:
            meta_file.write(f"{word}\n")
            
    # Double-check file lengths
    vec_lines = sum(1 for _ in open(vectors_file, 'r', encoding=encoding))
    meta_lines = sum(1 for _ in open(metadata_file, 'r', encoding=encoding)) - 1  # Subtract header
    
    if vec_lines != meta_lines:
        print(f"Warning: Final file length mismatch - vectors.tsv: {vec_lines}, metadata.tsv: {meta_lines}")

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
