#!/usr/bin/env python

import argparse
import csv
import os

def add_translation(metadata_file, translation_file, output_file):
    """
    Adds a translation column to the metadata file.

    Args:
        metadata_file: Path to the metadata file.
        translation_file: Path to the translation file.
        output_file: Path to the output file.
    """

    with open(metadata_file, 'r') as f_meta, open(translation_file, 'r') as f_trans, open(output_file, 'w') as f_out:
        reader_meta = csv.reader(f_meta, delimiter='\t')
        reader_trans = csv.reader(f_trans, delimiter='\t')

        # Write header to output file
        f_out.write("Word\tTranslation\n")

        for row_meta, row_trans in zip(reader_meta, reader_trans):
            word = row_meta[0]
            translation = row_trans[0]
            f_out.write(f"{word}\t{translation}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add a translation column to the metadata file.')
    parser.add_argument('metadata_file', help='Path to the metadata file.')
    parser.add_argument('translation_file', help='Path to the translation file.')
    parser.add_argument('output_file', help='Path to the output file.')

    args = parser.parse_args()

    add_translation(
        metadata_file=args.metadata_file,
        translation_file=args.translation_file,
        output_file=args.output_file
    )

