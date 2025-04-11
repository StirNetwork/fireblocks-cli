#!/bin/bash

# Build script for fireblocks-cli using PyInstaller
# Usage: ./build.sh

set -e

APP_NAME="fireblocks-cli"
ENTRYPOINT="fireblocks_cli/main.py"
DIST_DIR="dist"
BUILD_DIR="build"

# Cleanup old builds
echo "🔄 Cleaning previous builds..."
rm -rf $DIST_DIR $BUILD_DIR __pycache__

# Build for current OS
echo "🔧 Building $APP_NAME for $(uname)..."
pyinstaller \
  --onefile \
  --name $APP_NAME \
  --hidden-import=fireblocks_cli.commands.configure \
  $ENTRYPOINT

# Move binary to platform-specific name (optional)
PLATFORM=$(uname | tr '[:upper:]' '[:lower:]')
OUTPUT="$DIST_DIR/${APP_NAME}-$PLATFORM"
mv $DIST_DIR/$APP_NAME $OUTPUT

# Show result
echo "✅ Built binary: $OUTPUT"
ls -lh $OUTPUT

