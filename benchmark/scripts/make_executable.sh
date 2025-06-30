#!/bin/bash

DIR="$1"

if [ -z "$DIR" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

echo "=> Making all .sh and .py files in $DIR executable..."
find "$DIR" -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod +x {} \;
echo "=> Finished making files executable."