# QR-Play: Interactive Poster Gallery

A comprehensive web application for creating interactive poster galleries with time-synced audio narration and visual highlighting. Perfect for smart city exhibits, museums, educational displays, and interactive presentations.

## ✨ Features

### Multi-Poster Management
- 📚 **Gallery View** - Organize and display multiple posters
- 🎨 **Poster Dashboard** - Create, edit, and manage poster collections
- 🔒 **Admin Authentication** - Secure access to editing features
- 📱 **Individual QR Codes** - Each poster gets its own shareable QR code

### Interactive Playback
- 🎵 **Audio Synchronization** - Time-synced audio playback with visual highlights
- 🖼️ **Time-based Section Highlighting** - Automatically highlight poster areas during narration
- ▶️ **Responsive Player** - Play/pause controls with visual feedback
- 🎯 **Shape Support** - Rectangle and circular/ellipse highlight shapes

### Visual Section Editor
- ✏️ **Drag & Drop** - Intuitive section positioning
- 🔲 **Resize Handles** - Easy section sizing
- 🎨 **Color Customization** - Full color picker with transparency control
- 🔢 **Sequential IDs** - Auto-generated section numbering (1, 2, 3...)
- 👁️ **Live Preview** - See changes in real-time
- 💾 **Auto-Save on Delete** - Changes persist automatically

### Media Management
- 🎵 **Music Upload** - Replace poster audio with file validation
- 🖼️ **PDF to Image Conversion** - Automatic conversion of PDF posters
- 📁 **Organized Storage** - Clean folder structure (posters/, music/, qr/, json/)
- 🗑️ **Old File Cleanup** - Automatic deletion of replaced media

### Sharing & Distribution
- 🔗 **Dynamic QR Codes** - Auto-generated with current IP address
- 📥 **QR Download** - Save QR codes locally
- 🔗 **Share Button** - Web Share API integration with clipboard fallback
- 📱 **Mobile Responsive** - Optimized for all screen sizes

## 📁 Project Structure

```
QR-Play/
├── app.py                      # Flask server with API endpoints
├── requirements.txt            # Python dependencies
├── migrate_files.py           # One-time folder organization script
├── static/
│   ├── posters/               # Poster images (JPG, PNG)
│   ├── music/                 # Audio files (MP3, WAV, OGG, M4A, AAC)
│   ├── qr/                    # Generated QR codes
│   ├── json/                  # Database files (posters.json, sections_*.json)
│   └── style.css              # Global styles
└── templates/
    ├── gallery.html           # Main gallery page
    ├── poster_view.html       # Individual poster viewer
    ├── admin_login.html       # Admin authentication
    ├── admin_dashboard.html   # Poster management
    ├── admin_new_poster.html  # Create new poster
    └── admin.html             # Section editor
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- Flask - Web framework
- qrcode - QR code generation
- Pillow - Image processing
- PyMuPDF - PDF to image conversion

### 2. Run the Application

```bash
python app.py
```

The server will start on `http://0.0.0.0:5000/`

### 3. Access the Application

- **Gallery**: `http://YOUR_IP:5000/` - Browse all posters
- **Admin Dashboard**: `http://YOUR_IP:5000/admin` - Manage posters (password: `admin123`)
- **Scan QR Code**: Use your phone on the same WiFi network

## 📖 User Guide

### Creating a New Poster

1. Navigate to **Admin Dashboard** (`/admin`)
2. Login with password (default: `admin123`)
3. Click **"Add New Poster"**
4. Fill in the form:
   - **ID**: Unique identifier (e.g., `my-poster`)
   - **Name**: Display name
   - **Description**: Optional description
   - **Image**: Upload JPG, PNG, or PDF
   - **Music**: Upload MP3, WAV, OGG, M4A, or AAC
5. Click **"Create Poster"**

### Editing Sections

1. From the dashboard, click **"Edit Sections"** on any poster
2. Click **"Edit Sections"** button to enter edit mode
3. **Add Section**: Click "+ Add Section"
4. **Position**: Drag the section to desired location
5. **Resize**: Drag corner handles
6. **Edit Properties**: Click the edit button on the section
   - Set start/end times (in seconds)
   - Choose shape (Rectangle or Circle)
   - Select colors and transparency
   - Adjust border settings
7. **Delete**: Click "Delete Section" in the modal
8. **Save**: Click "Save Changes" (auto-exits edit mode)

### Uploading Music

1. Open poster in edit mode
2. Click **"🎵 Change Music"** button
3. Select audio file (MP3, WAV, OGG, M4A, AAC)
4. Click **"Upload"**
5. Old music file is automatically deleted

### Sharing Posters

1. Click the **QR button** (grid icon) on any poster card
2. Options:
   - **Download**: Save QR code as PNG
   - **Share**: Use native sharing or copy link to clipboard
3. Share the QR code or link with others

## 🎨 Section Configuration

Sections are stored in `static/json/sections_{poster_id}.json`:

```json
{
  "sections": [
    {
      "id": "1",
      "name": "Introduction",
      "shape": "rectangle",
      "startTime": 0,
      "endTime": 10,
      "position": { "x": "10%", "y": "10%" },
      "size": { "width": "30%", "height": "20%" },
      "color": "#7dd3fc",
      "transparency": 0.3,
      "borderColor": "#7dd3fc",
      "borderWidth": 2,
      "borderRadius": 6
    }
  ]
}
```

### Property Reference

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique section ID (auto-generated sequentially) |
| `name` | string | Section display name |
| `shape` | string | "rectangle" or "circle" |
| `startTime` | number | Start time in seconds |
| `endTime` | number | End time in seconds |
| `position.x` | string/number | Left position (% or px) |
| `position.y` | string/number | Top position (% or px) |
| `size.width` | string/number | Width (% or px) |
| `size.height` | string/number | Height (% or px) |
| `color` | string | Fill color (hex) |
| `transparency` | number | Opacity (0-1) |
| `borderColor` | string | Border color (hex) |
| `borderWidth` | number | Border width in pixels |
| `borderRadius` | number | Corner radius (ignored for circles) |

## 🔌 API Endpoints

### Sections API
- `GET /api/sections?poster_id={id}` - Retrieve section configurations
- `POST /api/sections?poster_id={id}` - Save section configurations

### Music API
- `GET /music/{poster_id}` - Stream audio file
- `POST /admin/upload-music` - Upload new music file

### Poster Management
- `GET /poster/{poster_id}` - View poster
- `GET /poster/{poster_id}/qr` - Get QR code URL
- `POST /admin/poster/create` - Create new poster
- `POST /admin/poster/{poster_id}/delete` - Delete poster

## ⚙️ Configuration

### Admin Password

Change the default password in `app.py`:

```python
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
```

Or set via environment variable:

```bash
# Windows PowerShell
$env:ADMIN_PASSWORD = "your_secure_password"

# Linux/Mac
export ADMIN_PASSWORD="your_secure_password"
```

### Port Configuration

```bash
# Windows PowerShell
$env:PORT = "8080"

# Linux/Mac
export PORT=8080
```

### File Upload Limits

Maximum file size: **50 MB**

Supported formats:
- **Images**: PNG, JPG, JPEG, PDF
- **Audio**: MP3, MPEG, WAV, OGG, M4A, AAC

## 🎯 Features in Detail

### Sequential ID Generation
- Sections automatically get IDs: 1, 2, 3, 4...
- ID field is read-only and grayed out
- IDs are reassigned sequentially after deletion

### Shape Support
- **Rectangle**: Customizable border radius
- **Circle/Ellipse**: Automatic 50% border radius
- Border radius input disabled for circular shapes

### Auto-Exit Edit Mode
- Automatically exits edit mode after saving
- Sections become hidden until next edit or playback

### Pause on Edit
- Music automatically pauses when entering edit mode
- Playback resets to 0:00
- Prevents conflicts between editing and playback

### Dynamic Share Links
- Share button copies actual poster URL: `/poster/{id}`
- Uses dynamic IP address (adapts to network changes)
- Works on gallery, poster view, and admin pages

### Responsive Footer
- Developer credit with portfolio link
- Centered and responsive
- Reduced height on mobile devices

## 🔧 Troubleshooting

### Music Not Playing
- Check file format (supported: MP3, WAV, OGG, M4A, AAC)
- Verify file is in `static/music/` folder
- Check browser console for errors

### Images Not Loading
- Ensure images are in `static/posters/` folder
- Check file permissions
- Verify correct path in database

### QR Codes Not Generating
- Check network connectivity
- Verify `static/qr/` folder exists
- Check file write permissions

### Can't Access Admin Panel
- Default password: `admin123`
- Check `ADMIN_PASSWORD` environment variable
- Clear browser cookies and try again

## 📱 Mobile Usage

1. **Connect to same WiFi** as the server
2. **Scan QR code** from gallery or poster page
3. **Tap to play** (autoplay may be blocked)

## 🚀 Deployment

### Local Network
```bash
python app.py
```
Access via `http://YOUR_LOCAL_IP:5000/`

### Production (with HTTPS)
Use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Future Enhancement)
Create `Dockerfile` for containerized deployment

## 🔐 Security Notes

⚠️ **Important Security Considerations:**

- **Change default password** before deployment
- **Not production-ready** - Designed for local/demo use
- **No HTTPS** - Do not expose to public internet without SSL/TLS
- **Session management** - Uses Flask sessions (configure `SECRET_KEY` in production)
- **File upload validation** - Basic validation included, enhance for production
- **Firewall** - Ensure appropriate rules for your network

## 🛠️ Technology Stack

- **Backend**: Python 3.x, Flask 2.x
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Libraries**: 
  - PyMuPDF (fitz) - PDF processing
  - Pillow - Image manipulation
  - qrcode - QR code generation
- **Storage**: JSON file-based database
- **Media**: HTML5 Audio API

## 📝 License

This project is open source and available for educational and commercial use.

## 👨‍💻 Developer

**Smart City Research Center**
- Portfolio: [himanshu-portfolio-beryl.vercel.app](https://smartcitylivinglab.iiit.ac.in/)
- GitHub: [@himanshufanibhare](https://github.com/himanshufanibhare)

## 🙏 Acknowledgments

Built for smart city initiatives, educational institutions, and interactive displays.

## 📊 Changelog

### Version 1.0.0 (Current)
- ✅ Multi-poster gallery system
- ✅ Admin authentication and dashboard
- ✅ Visual section editor with shapes
- ✅ Music upload and management
- ✅ QR code generation and sharing
- ✅ Organized folder structure
- ✅ Responsive design
- ✅ Sequential ID generation
- ✅ Auto-save on delete
- ✅ Dynamic share links

## 🔮 Future Enhancements

- [ ] Video support
- [ ] Multi-language support
- [ ] User roles and permissions
- [ ] Database backend (PostgreSQL/MongoDB)
- [ ] Real-time collaboration
- [ ] Analytics dashboard
- [ ] Export/Import poster configurations
- [ ] Template library
- [ ] Published poster URLs (public access)

---

**Made with ❤️ for interactive experiences**
