#!/usr/bin/env python

import argparse
import csv
import os
from translate import Translator

def add_translations_to_metadata(metadata_file, output_file=None, source_lang='auto', target_lang='en'):
    """
    Adds English translations to a metadata.tsv file using an online translator.

    Args:
        metadata_file: Path to the metadata file.
        output_file: Path to the output file. If None, defaults to metadata_translated.tsv in the same directory.
        source_lang: Source language for translation (default: 'auto' to detect automatically).
        target_lang: Target language for translation (default: 'en' for English).
    """

    if output_file is None:
        output_file = os.path.join(os.path.dirname(metadata_file), 'metadata_translated.tsv')

    translator = Translator(to_lang=target_lang, from_lang=source_lang)

    with open(metadata_file, 'r', encoding='utf-8') as f_meta, open(output_file, 'w', encoding='utf-8') as f_out:
        reader_meta = csv.reader(f_meta, delimiter='\t')
        # Write header to output file
        header = next(reader_meta) # Read header
        f_out.write(f"{header[0]}\tEnglish\n") # Assume first column is 'Word'

        for row_meta in reader_meta:
            word = row_meta[0]
            translation = translator.translate(word).text
            f_out.write(f"{word}\t{translation}\n")

    print(f"Translated metadata saved to: {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add English translations to metadata.tsv file.')
    parser.add_argument('metadata_file', help='Path to the metadata file.')
    parser.add_argument('--output_file', '-o', type=str, default=None, help='Path to the output file (optional, default: metadata_translated.tsv in the same directory)')

    args = parser.parse_args()

    add_translations_to_metadata(
        metadata_file=args.metadata_file,
        output_file=args.output_file,
    )
