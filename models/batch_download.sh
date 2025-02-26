#!/usr/bin/env bash

# batch_download.sh - Downloads multiple model files using download_model_files.sh
# Usage: ./batch_download.sh <url_file>
#        where <url_file> is a file containing a list of URLs, one URL per line

set -e

# Check if a URL file is provided as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <url_file>"
    echo "       <url_file> is a file containing a list of URLs, one URL per line"
    echo "Example: $0 urls.txt"
    exit 1
fi

URL_FILE="$1"

# Check if the URL file exists and is readable
if [ ! -r "$URL_FILE" ]; then
    echo "Error: URL file '$URL_FILE' not found or not readable."
    exit 1
fi

# Read URLs from the file and process each URL
while IFS= read -r URL; do
    # Skip empty lines and lines starting with '#' (comments)
    if [[ -z "$URL" ]] || [[ "$URL" == \#* ]]; then
        continue
    fi

    # Extract filename from URL to use as directory name
    MODEL_DIR_NAME=$(basename "$URL" | sed 's/\.[^.]*$//') # Remove extension
    TARGET_DIR="./models/${MODEL_DIR_NAME}"

    echo "Processing URL: $URL"
    echo "Target directory: $TARGET_DIR"

    # Execute download_model_files.sh for each URL and target directory
    ./scripts/download_model_files.sh -h "$URL" -d "$TARGET_DIR"

    echo "-------------------------"
done < "$URL_FILE"

echo "Batch download process completed."
