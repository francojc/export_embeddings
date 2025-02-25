#!/bin/bash

# download_model_files.sh - Downloads and extracts archived model files
# Usage: ./download_model_files.sh <url> <target_directory>

set -e

# Check if required arguments are provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <url> <target_directory>"
    echo "Example: $0 https://example.com/model.zip ./models/english"
    exit 1
fi

URL=$1
TARGET_DIR=$2

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Get the base name of the target directory to use as the model name
MODEL_NAME=$(basename "$TARGET_DIR")
echo "Model name: $MODEL_NAME"

# Get the filename from the URL
FILENAME=$(basename "$URL")
echo "Downloading $FILENAME..."

# Download the file
curl -L "$URL" -o "/tmp/$FILENAME"
echo "Download complete."

# Determine the file type and extract accordingly
echo "Extracting to $TARGET_DIR..."
case "$FILENAME" in
    *.zip)
        unzip -o "/tmp/$FILENAME" -d "$TARGET_DIR"
        ;;
    *.tar.gz|*.tgz)
        tar -xzf "/tmp/$FILENAME" -C "$TARGET_DIR"
        ;;
    *.tar.bz2|*.tbz2)
        tar -xjf "/tmp/$FILENAME" -C "$TARGET_DIR"
        ;;
    *.tar)
        tar -xf "/tmp/$FILENAME" -C "$TARGET_DIR"
        ;;
    *.gz)
        gunzip -c "/tmp/$FILENAME" > "$TARGET_DIR/$(basename "$FILENAME" .gz)"
        ;;
    *.bz2)
        bunzip2 -c "/tmp/$FILENAME" > "$TARGET_DIR/$(basename "$FILENAME" .bz2)"
        ;;
    *)
        echo "Unsupported file format: $FILENAME"
        echo "Copying file to target directory without extraction"
        cp "/tmp/$FILENAME" "$TARGET_DIR/"
        ;;
esac

# Clean up
rm "/tmp/$FILENAME"
echo "Extraction complete. Files are available in $TARGET_DIR"
