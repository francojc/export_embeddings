#!/usr/bin/env bash

# download_model_files.sh - Downloads and extracts archived model files
# Usage: ./download_model_files.sh -h <url> -d <target_directory>

set -e

# Initialize variables
URL=""
TARGET_DIR=""

# Parse command line options
while getopts "h:d:" opt; do
  case $opt in
    h) URL="$OPTARG" ;;
    d) TARGET_DIR="$OPTARG" ;;
    \?) echo "Invalid option -$OPTARG" >&2; exit 1 ;;
  esac
done

# Check if required arguments are provided
if [ -z "$URL" ] || [ -z "$TARGET_DIR" ]; then
    echo "Usage: $0 -h <url> -d <target_directory>"
    echo "Example: $0 -h https://example.com/model.zip -d ./models/english"
    exit 1
fi

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
