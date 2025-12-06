#!/bin/bash

# Script to install custom integration icons to Home Assistant brands directory
# This allows locally installed custom integrations to show custom icons

set -e

echo "=== Villages Events Icon Installer ==="
echo ""

# Detect Home Assistant configuration directory
if [ -d "/config" ]; then
    CONFIG_DIR="/config"
elif [ -d "$HOME/.homeassistant" ]; then
    CONFIG_DIR="$HOME/.homeassistant"
elif [ -d "$HOME/homeassistant" ]; then
    CONFIG_DIR="$HOME/homeassistant"
else
    echo "Error: Could not find Home Assistant configuration directory"
    echo "Please set CONFIG_DIR manually:"
    echo "  export CONFIG_DIR=/path/to/config"
    echo "  ./install_icons.sh"
    exit 1
fi

echo "Home Assistant config directory: $CONFIG_DIR"
echo ""

# Create brands directory structure
BRANDS_DIR="$CONFIG_DIR/custom_components/brands"
INTEGRATION_DIR="$BRANDS_DIR/custom_integrations/villages_events"

echo "Creating brands directory structure..."
mkdir -p "$INTEGRATION_DIR"

# Copy icon files
echo "Copying icon files..."
cp icon.png "$INTEGRATION_DIR/icon.png"
cp icon@2x.png "$INTEGRATION_DIR/icon@2x.png"
cp logo.png "$INTEGRATION_DIR/logo.png"
cp logo@2x.png "$INTEGRATION_DIR/logo@2x.png"

echo ""
echo "✓ Icons installed successfully!"
echo ""
echo "Icon files installed to:"
echo "  $INTEGRATION_DIR"
echo ""
echo "Next steps:"
echo "  1. Restart Home Assistant"
echo "  2. Clear your browser cache (Ctrl+Shift+R)"
echo "  3. Go to Settings → Devices & Services"
echo "  4. Your custom icon should now appear!"
echo ""
echo "Note: This is a workaround for locally installed integrations."
echo "For HACS installations, icons must be in the GitHub repository."
