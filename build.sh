#!/bin/bash

# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

# Build script for fireblocks-cli using PyInstaller + bump-my-version + upx
# Usage: ./build.sh [major|minor|patch]

set -e

APP_NAME="fireblocks-cli"
ENTRYPOINT="fireblocks_cli/main.py"
DIST_DIR="dist"
BUILD_DIR="build"

# Handle version bump
BUMP_PART="$1"
if [[ "$BUMP_PART" =~ ^(major|minor|patch)$ ]]; then
  echo "🔧 Bumping version: $BUMP_PART"

  case "$BUMP_PART" in
    major)
      if [[ -n "$(git status --porcelain)" ]]; then
        echo "🚫 Cannot bump major version in a dirty working directory."
        echo "💡 Please commit or stash your changes first."
        exit 1
      fi
      ;;
    minor|patch)
      echo "⚠️ Allowing dirty working tree for $BUMP_PART bump"
      ;;
  esac

  bump-my-version bump $BUMP_PART --allow-dirty
else
  echo "⚠️ No valid bump type provided. Skipping version bump."
fi

# Read version from fireblocks_cli/__init__.py
VERSION=$(grep -oE '__version__ = "[^"]+"' fireblocks_cli/__init__.py | cut -d '"' -f2)
echo "🔖 Using version: $VERSION"

# Cleanup old builds
echo "🔄 Cleaning previous builds..."
rm -rf $DIST_DIR $BUILD_DIR __pycache__

# Build with PyInstaller
echo "🔧 Building $APP_NAME for $(uname)..."
pyinstaller \
  --onefile \
  --name $APP_NAME \
  --hidden-import=fireblocks_cli.commands.configure \
  --clean \
  $ENTRYPOINT

# Rename output binary
PLATFORM=$(uname | tr '[:upper:]' '[:lower:]')
OUTPUT="$DIST_DIR/${APP_NAME}-${PLATFORM}-v${VERSION}"
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
