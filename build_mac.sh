#!/bin/bash
set -e

VERSION="${1:-1.0.0}"
DIST="dist/R16_AudioTool"

echo "Building R16 AudioTool $VERSION for macOS..."

# Clean previous build
rm -rf build dist

# Build onedir bundle (no .app wrapper)
pyinstaller R16_AudioTool.spec

# Copy macOS starter script and make executable
cp start_mac.command "$DIST/start_mac.command"
chmod +x "$DIST/start_mac.command"
chmod +x "$DIST/R16_AudioTool"

# Create release zip
ZIP="R16_AudioTool_${VERSION}_macOS.zip"
cd dist
zip -r "../$ZIP" R16_AudioTool/
cd ..

echo ""
echo "Done: $ZIP"
echo ""
echo "To release:"
echo "  gh release create v$VERSION $ZIP --title 'v$VERSION' --notes ''"
