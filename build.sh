#!/bin/bash

# Build script for fireblocks-cli using PyInstaller + git describe + upx
# Usage: ./build.sh

set -e

APP_NAME="fireblocks-cli"
ENTRYPOINT="fireblocks_cli/main.py"
DIST_DIR="dist"
BUILD_DIR="build"

# Get version from git
echo "📦 Extracting version..."
VERSION=$(git describe --tags --always)
echo "$VERSION" > VERSION.txt
echo "🔖 Version: $VERSION"

# Cleanup old builds
echo "🔄 Cleaning previous builds..."
rm -rf $DIST_DIR $BUILD_DIR __pycache__

# Build with PyInstaller (embed version)
echo "🔧 Building $APP_NAME for $(uname)..."
pyinstaller \
  --onefile \
  --name $APP_NAME \
  --hidden-import=fireblocks_cli.commands.configure \
  --add-data "VERSION.txt:." \
  --clean \
  $ENTRYPOINT

# Add version file manually (for reference or embedding)
echo "$VERSION" > VERSION.txt

# Rename output binary
PLATFORM=$(uname | tr '[:upper:]' '[:lower:]')
OUTPUT="$DIST_DIR/${APP_NAME}-$PLATFORM"
mv $DIST_DIR/$APP_NAME $OUTPUT

# Optional UPX compression
if command -v upx &> /dev/null; then
  echo "📦 Compressing binary with UPX..."
  upx --best --lzma $OUTPUT
else
  echo "⚠️ UPX not found. Skipping compression."
fi

# Show result
echo "✅ Built binary: $OUTPUT"
ls -lh $OUTPUT
