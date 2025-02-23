import fasttext
import numpy as np

def convert_fasttext_to_embedding_projector(bin_file, vectors_file, metadata_file, limit=None):
    """
    Converts a FastText .bin file to vectors.tsv and metadata.tsv files
    suitable for the TensorFlow Embedding Projector.

    Args:
        bin_file: Path to the FastText .bin file (model.bin).
        vectors_file: Path to output vectors.tsv file.
        metadata_file: Path to output metadata.tsv file.
        limit: Optional.  Only process the top 'limit' most frequent words.
               If None, process all words in the model.
    """

    try:
        model = fasttext.load_model(bin_file)
    except ValueError as e:
        print(f"Error loading FastText model: {e}")
        print("Make sure the '.bin' file is a valid FastText model.")
        return

    words = model.words
    if limit is not None:
        words = words[:limit]

    with open(vectors_file, 'w') as f_vec, open(metadata_file, 'w', encoding='utf-8') as f_meta:
        # Write header to metadata file
        f_meta.write("Word\n")  # Header is required by the Embedding Projector

        for word in words:
            vector = model.get_word_vector(word)  # type: ignore (fasttext stubs incomplete)
            vector_str = '\t'.join(map(str, vector))
            f_vec.write(f"{vector_str}\n")
            f_meta.write(f"{word}\n")

    print(f"Vectors saved to {vectors_file}")
    print(f"Metadata saved to {metadata_file}")

if __name__ == '__main__':
    # Example usage
    bin_file = 'your_fasttext_model.bin'  # Replace with your .bin file
    vectors_file = 'vectors.tsv'
    metadata_file = 'metadata.tsv'
    limit = 10000  # Process only the top 10,000 words (optional)

    convert_fasttext_to_embedding_projector(bin_file, vectors_file, metadata_file, limit)
