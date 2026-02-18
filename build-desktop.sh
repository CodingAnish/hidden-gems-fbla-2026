#!/bin/bash

# This script prepares the Flask backend for bundling with the Tauri desktop app

set -e

echo "🔧 Preparing Hidden Gems for Desktop Distribution..."
echo ""

# Step 1: Create dist directory structure
echo "📁 Creating distribution structure..."
mkdir -p dist/Hidden\ Gems.app/Contents/Resources
mkdir -p dist/Hidden\ Gems.app/Contents/MacOS
mkdir -p dist/Hidden\ Gems.app/Contents/Frameworks

# Step 2: Copy Flask backend
echo "📦 Bundling Flask backend..."
cp -r web dist/Hidden\ Gems.app/Contents/Resources/
cp -r src dist/Hidden\ Gems.app/Contents/Resources/
cp -r .venv dist/Hidden\ Gems.app/Contents/Resources/ 2>/dev/null || echo "⚠️  .venv not found, will be installed at runtime"
cp hidden_gems.db dist/Hidden\ Gems.app/Contents/Resources/ 2>/dev/null || echo "ℹ️  Database will be created on first run"
cp .env dist/Hidden\ Gems.app/Contents/Resources/ 2>/dev/null || echo "⚠️  .env file not found, configure secrets before distribution"

# Step 3: Create launcher script
echo "🚀 Creating app launcher..."
cat > dist/Hidden\ Gems.app/Contents/MacOS/hidden-gems-launcher << 'EOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_DIR="$SCRIPT_DIR/../Resources"

cd "$APP_DIR"
.venv/bin/python -m web.app &
sleep 3
open "http://localhost:5001"
EOF

chmod +x dist/Hidden\ Gems.app/Contents/MacOS/hidden-gems-launcher

# Step 4: Create macOS Info.plist
echo "📄 Creating macOS app configuration..."
cat > dist/Hidden\ Gems.app/Contents/Info.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>Hidden Gems</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleIdentifier</key>
    <string>com.fbla.hiddengems</string>
    <key>CFBundleExecutable</key>
    <string>hidden-gems-launcher</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

echo ""
echo "✅ Desktop app prepared!"
echo ""
echo "📍 Location: dist/Hidden\ Gems.app"
echo ""
echo "🚀 To run the app:"
echo "   open dist/Hidden\ Gems.app"
echo ""
echo "📦 To distribute:"
echo "   1. Code sign the app (macOS): codesign -s - dist/Hidden\\ Gems.app"
echo "   2. Create DMG: hdiutil create -volname 'Hidden Gems' -srcfolder dist -ov -format UDZO Hidden-Gems.dmg"
