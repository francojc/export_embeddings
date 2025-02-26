#!/usr/bin/env bash

# batch_download.sh - Downloads multiple model files using download_model_files.sh
# Usage: ./batch_download.sh <url1> <url2> ...

set -e

# Check if at least one URL is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <url1> <url2> ..."
    echo "Example: $0 https://example.com/model1.zip https://example.com/model2.tar.gz"
    exit 1
fi

# Loop through each URL provided as an argument
for URL in "$@"; do
    # Extract filename from URL to use as directory name
    MODEL_DIR_NAME=$(basename "$URL" | sed 's/\.[^.]*$//') # Remove extension
    TARGET_DIR="./models/${MODEL_DIR_NAME}"

    echo "Processing URL: $URL"
    echo "Target directory: $TARGET_DIR"

    # Execute download_model_files.sh for each URL and target directory
    ./scripts/download_model_files.sh -h "$URL" -d "$TARGET_DIR"

    echo "-------------------------"
done

echo "Batch download process completed."
