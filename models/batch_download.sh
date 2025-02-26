#!/usr/bin/env bash

# batch_download.sh - Downloads multiple model files using download_model_files.sh
# Usage: ./batch_download.sh <tsv_file>
#        where <tsv_file> is a TSV file containing URLs and target directories
#        - Column 1: URL of the model file
#        - Column 2: Target directory

set -e

# Check if a TSV file is provided as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <tsv_file>"
    echo "       <tsv_file> is a TSV file with URLs (col 1) and target directories (col 2)"
    echo "Example: $0 urls_and_dirs.tsv"
    exit 1
fi

TSV_FILE="$1"

# Check if the TSV file exists and is readable
if [ ! -r "$TSV_FILE" ]; then
    echo "Error: TSV file '$TSV_FILE' not found or not readable."
    exit 1
fi

# Read TSV file and process each line
while IFS=$'\t' read -r URL TARGET_DIR; do
    # Skip empty lines and lines starting with '#' (comments)
    if [[ -z "$URL" ]] || [[ "$URL" == \#* ]]; then
        continue
    fi

    echo "Processing URL: $URL"
    echo "Target directory: $TARGET_DIR"

    # Execute download_model_files.sh for each URL and target directory
    ./scripts/download_model_files.sh -h "$URL" -d "$TARGET_DIR"

    echo "-------------------------"
done < "$TSV_FILE"

echo "Batch download process completed."
