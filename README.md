# Tetra

Tetra is a simple, native Ubuntu wrapper for AI services.

It provides a unified, no-nonsense interface for accessing:
- ChatGPT
- Grok
- Gemini
- Claude

## Features
- **Native UI**: Built with GTK4 and Libadwaita for a perfect integration with Ubuntu/GNOME.
- **Lightweight**: Doing nothing more than wrapping the web interfaces in a clean window.
- **Zero Distractions**: No tab clutter, just the 4 favorite LLMs side-by-side (or one click away).
- **Privacy**: Uses standard WebKit instances; sessions persist but code is minimal and transparent.

## Installation

### Prerequisites
Requires: `python3`, `gtk4`, `libadwaita`, `webkitgtk-6.0`.

On Ubuntu 24.04+:
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 gir1.2-webkit-6.0
```

### Install to System
To install Tetra to your applications menu (Dock/Activity View):
```bash
git clone https://github.com/nmcmil/tetra.git
cd tetra
chmod +x install.sh
./install.sh
```

### Run Locally
To run without installing:
```bash
python3 main.py
```

## Future
Possibly more models to come, but for now, it's just the big 4.
