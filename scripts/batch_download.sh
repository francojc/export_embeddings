#!/usr/bin/env bash

# batch_download.sh - Downloads multiple model files using download_model_files.sh
# Usage: ./batch_download.sh <csv_file>
#        where <csv_file> is a CSV file containing download instructions
#        - Column 1: URL of the model file
#        - Column 2: Target directory
#        - Column 3: Force download (true/false)

set -e

# Check if a CSV file is provided as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <csv_file>"
    echo "       <csv_file> is a CSV file with URLs (col 1), target directories (col 2), and force flags (col 3)."
    echo "       Column 3 should be 'true' or 'false' to indicate force download."
    echo "Example: $0 urls_dirs_force.csv"
    exit 1
fi

CSV_FILE="$1"

# Check if the CSV file exists and is readable
if [ ! -r "$CSV_FILE" ]; then
    echo "Error: CSV file '$CSV_FILE' not found or not readable."
    exit 1
fi

# Read CSV file and process each line
while IFS=, read -r URL TARGET_DIR FORCE; do
    # Skip empty lines and lines starting with '#' (comments)
    if [[ -z "$URL" ]] || [[ "$URL" == \#* ]]; then
        continue
    fi

    echo "Processing URL: $URL"
    echo "Target directory: $TARGET_DIR"

    # Determine if force download is requested
    FORCE_VALUE=""
    if [[ "$FORCE" =~ ^(true|TRUE|True)$ ]]; then
        FORCE_VALUE="true"
        echo "Force download: true"
    else
        FORCE_VALUE="false"
        echo "Force download: false (default)"
    fi

    # Execute download_model_files.sh for each URL and target directory
    ./scripts/download_model_files.sh -h "$URL" -d "$TARGET_DIR" -f "$FORCE_VALUE"

    echo "-------------------------"
done < "$CSV_FILE"

echo "Batch download process completed."
