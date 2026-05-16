#!/bin/bash
# Double-click this file to start R16 AudioTool on macOS.
# On first run it removes the quarantine flag macOS sets on downloaded files.

DIR="$(cd "$(dirname "$0")" && pwd)"

# Remove quarantine from the entire folder (needed for unsigned apps on macOS)
xattr -dr com.apple.quarantine "$DIR" 2>/dev/null

exec "$DIR/R16_AudioTool" "$@"
