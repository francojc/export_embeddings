#!/usr/bin/env bash

# batch_download.sh - Downloads multiple model files using download_model_files.sh
# Usage: ./batch_download.sh <tsv_file>
#        where <tsv_file> is a TSV file containing download instructions
#        - Column 1: URL of the model file
#        - Column 2: Target directory
#        - Column 3: Force download (true/false)

set -e

# Check if a TSV file is provided as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <tsv_file>"
    echo "       <tsv_file> is a TSV file with URLs (col 1), target directories (col 2), and force flags (col 3)"
    echo "       Column 3 should be 'true' or 'false' to indicate force download."
    echo "Example: $0 urls_dirs_force.tsv"
    exit 1
fi

TSV_FILE="$1"

# Check if the TSV file exists and is readable
if [ ! -r "$TSV_FILE" ]; then
    echo "Error: TSV file '$TSV_FILE' not found or not readable."
    exit 1
fi

# Read TSV file and process each line
while IFS=$'\t' read -r URL TARGET_DIR FORCE; do
    # Skip empty lines and lines starting with '#' (comments)
    if [[ -z "$URL" ]] || [[ "$URL" == \#* ]]; then
        continue
    fi

    echo "Processing URL: $URL"
    echo "Target directory: $TARGET_DIR"

    # Determine if force download is requested
    FORCE_ARG=""
    if [[ "$FORCE" =~ ^(true|TRUE|True)$ ]]; then
        FORCE_ARG="--force true"
        echo "Force download: true"
    else
        echo "Force download: false (default)"
    fi

    # Execute download_model_files.sh for each URL and target directory
    ./download_model_files.sh -h "$URL" -d "$TARGET_DIR" $FORCE_ARG

    echo "-------------------------"
done < "$TSV_FILE"

echo "Batch download process completed."
