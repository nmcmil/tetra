#!/bin/bash

# Define paths
INSTALL_DIR="$HOME/.local/share/tetra/app"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "Installing Tetra..."

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"

# Copy application files
cp main.py "$INSTALL_DIR/"
cp style.css "$INSTALL_DIR/"
cp -r assets "$INSTALL_DIR/"

# Create executable wrapper
cat > "$BIN_DIR/tetra" <<EOF
#!/bin/bash
exec python3 "$INSTALL_DIR/main.py" "\$@"
EOF

chmod +x "$BIN_DIR/tetra"

# Install Desktop file
cp tetra.desktop "$DESKTOP_DIR/"

echo "Installation complete!"
echo "Run 'tetra' from terminal or find 'Tetra' in your applications menu."
echo "Note: You might need to log out and log back in for the desktop entry to appear if it's the first time."
