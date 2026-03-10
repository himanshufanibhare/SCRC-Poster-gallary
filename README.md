# SCRC Poster Gallery

An interactive poster gallery that combines audio narration with time-synced visual highlighting of poster sections. Share via QR code for mobile access.

## Features

- 🎵 **Audio playback** synced with poster presentation
- 🖼️ **PDF to image conversion** for poster display
- ⏰ **Time-based section highlighting** - automatically highlight different poster areas during playback
- ✏️ **Visual section editor** - drag, resize, and customize highlight boxes
- 📱 **QR code generation** for easy mobile sharing
- 🔄 **Web Share API** integration for native sharing
- 📝 **JSON-based configuration** for easy section management

## Files

- `app.py` - Flask server with API endpoints
- `requirements.txt` - Python dependencies
- `templates/index.html` - Interactive poster viewer
- `static/style.css` - Styling
- `static/sections.json` - Section highlight configurations
- `SECTIONS_GUIDE.md` - Detailed guide for section configuration

## Quick Start

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Add your content:**
   - Place audio file as `music.mp3`
   - Place poster as `static/poster1.jpg` (or add PDF to `static/` folder - it will be auto-converted)

3. **Run the app:**

```bash
python app.py
```

4. **Access:**
   - Open the printed URL (e.g., `http://192.168.x.x:5000/`)
   - Or scan `static/music_qr.png` from your phone (same WiFi required)

## Interactive Sections

Configure time-synced highlights in `static/sections.json`:

```json
{
  "sections": [
    {
      "id": "section1",
      "name": "Top Layer",
      "startTime": 5,
      "endTime": 15,
      "position": {"x": 150, "y": 80},
      "size": {"width": 250, "height": 120},
      "color": "#7dd3fc",
      "transparency": 0.4,
      "borderColor": "#7dd3fc",
      "borderWidth": 3
    }
  ]
}
```

### Visual Editor

1. Click **"Edit Sections"** button
2. Drag sections to reposition
3. Drag corner handles to resize
4. Double-click to edit color/transparency
5. Click **"Save Sections"** to persist changes

See [SECTIONS_GUIDE.md](SECTIONS_GUIDE.md) for detailed documentation.

## API Endpoints

- `GET /api/sections` - Retrieve section configurations
- `POST /api/sections` - Save section configurations

## Environment Variables

- `MUSIC_URL` - Override local hosting with external URL
- `PORT` - Change server port (default: 5000)

Example:
```powershell
$env:MUSIC_URL = "https://example.com/music.mp3"
python app.py
```

Notes:
- If you already have a public link for your audio (Dropbox, Google Drive, GitHub, etc.), set the `MUSIC_URL` environment variable before running to generate a QR that points to that URL instead of your local IP.

  Example (Windows PowerShell):

  ```powershell
  $env:MUSIC_URL = "https://example.com/music.mp3"
  python app.py
  ```

- Mobile devices must be on the same local network as the PC hosting the file when serving locally.
- Ensure your firewall allows incoming connections to the chosen port (default 5000).
- Autoplay may be blocked by some mobile browsers; use the provided player controls to start playback if necessary.

Security:
- This is a minimal demo for local use. Do not expose the host to the public internet without proper security and HTTPS.
