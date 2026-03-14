from flask import Flask, send_file, render_template, url_for, request, jsonify, session, redirect
import qrcode
import socket
import os
import fitz
from PIL import Image
import json
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "scrc-admin-key-2026")  # Change this in production
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Folder structure
STATIC_FOLDER = "static"
POSTERS_FOLDER = os.path.join(STATIC_FOLDER, "posters")
MUSIC_FOLDER = os.path.join(STATIC_FOLDER, "music")
QR_FOLDER = os.path.join(STATIC_FOLDER, "qr")
JSON_FOLDER = os.path.join(STATIC_FOLDER, "json")

MUSIC_FILE = "music.mp3"
PORT = int(os.environ.get("PORT", 5000))
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")  # Change this!
POSTERS_FILE = os.path.join(JSON_FOLDER, "posters.json")
UPLOAD_FOLDER = STATIC_FOLDER

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'mpeg', 'wav', 'ogg', 'm4a', 'aac'}

# Create folders on startup
for folder in [STATIC_FOLDER, POSTERS_FOLDER, MUSIC_FOLDER, QR_FOLDER, JSON_FOLDER]:
    os.makedirs(folder, exist_ok=True)


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def load_posters():
    """Load posters database"""
    try:
        if os.path.exists(POSTERS_FILE):
            with open(POSTERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"posters": []}
    except Exception as e:
        print(f"Error loading posters: {e}")
        return {"posters": []}


def save_posters(data):
    """Save posters database"""
    try:
        os.makedirs(JSON_FOLDER, exist_ok=True)
        with open(POSTERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving posters: {e}")
        return False


def get_poster_by_id(poster_id):
    """Get poster by ID"""
    posters_data = load_posters()
    for poster in posters_data.get("posters", []):
        if poster["id"] == poster_id:
            return poster
    return None


def generate_qr_for_poster(poster_id):
    """Generate QR code for specific poster"""
    local_ip = get_local_ip()
    url = f"https://{local_ip}:{PORT}/poster/{poster_id}"
    
    try:
        qr = qrcode.make(url)
        qr_filename = f"qr_{poster_id}.png"
        qr_path = os.path.join(QR_FOLDER, qr_filename)
        qr.save(qr_path)
        print(f"Generated {qr_filename} -> {url}")
        return qr_filename
    except Exception as e:
        print(f"Failed to generate QR: {e}")
        return None


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


@app.route("/")
def index():
    """Show gallery of all posters"""
    posters_data = load_posters()
    posters = posters_data.get("posters", [])
    
    return render_template('gallery.html', posters=posters)


@app.route("/poster/<poster_id>")
def view_poster(poster_id):
    """View a specific poster (public)"""
    poster = get_poster_by_id(poster_id)
    if not poster:
        return "Poster not found", 404
    
    qr_path = url_for('static', filename=f"qr/{poster['qr_code']}") if poster.get('qr_code') else None
    poster_img = url_for('static', filename=f"posters/{poster['image']}") if poster.get('image') else None
    music_file = poster.get('music', 'music.mp3')
    
    return render_template('poster_view.html', 
                         qr_path=qr_path, 
                         poster_img=poster_img,
                         poster=poster,
                         music_file=music_file)


@app.route('/poster/<poster_id>/qr')
def poster_qr(poster_id):
    """Generate or return QR image for a poster (returns JSON with url)
       Generates the QR file on demand and returns its static URL so gallery can display it."""
    poster = get_poster_by_id(poster_id)
    # Determine filename to use
    qr_filename = None
    if poster and poster.get('qr_code'):
        qr_filename = poster['qr_code']
    else:
        qr_filename = f'qr_{poster_id}.png'

    qr_path = os.path.join(QR_FOLDER, qr_filename)
    # If file missing, attempt to generate
    if not os.path.exists(qr_path):
        generated = generate_qr_for_poster(poster_id)
        if not generated:
            return jsonify({'error': 'QR generation failed'}), 500
        qr_filename = generated

    qr_url = url_for('static', filename=f"qr/{qr_filename}")
    return jsonify({'qr_url': qr_url})


@app.route("/music/<poster_id>")
def poster_music(poster_id):
    """Serve music for specific poster"""
    poster = get_poster_by_id(poster_id)
    if not poster:
        return "Poster not found", 404
    
    music_filename = poster.get('music') or poster.get('audio')
    if not music_filename:
        return "No music configured", 404
    
    music_path = os.path.join(MUSIC_FOLDER, music_filename)
    if os.path.exists(music_path):
        # Detect mimetype based on extension
        ext = music_filename.rsplit('.', 1)[-1].lower()
        mimetypes = {
            'mp3': 'audio/mpeg',
            'wav': 'audio/wav',
            'ogg': 'audio/ogg',
            'm4a': 'audio/mp4',
            'aac': 'audio/aac'
        }
        mimetype = mimetypes.get(ext, 'audio/mpeg')
        return send_file(music_path, mimetype=mimetype)
    return "Music file not found", 404


@app.route("/music.mp3")
def music():
    """Legacy music endpoint"""
    return send_file(MUSIC_FILE, mimetype="audio/mpeg")


@app.route("/admin")
def admin():
    """Admin login page"""
    if not session.get('authenticated'):
        return render_template('admin_login.html')
    return redirect('/admin/dashboard')


@app.route("/admin/dashboard")
def admin_dashboard():
    """Admin dashboard - requires authentication"""
    if not session.get('authenticated'):
        return redirect('/admin')
    
    posters_data = load_posters()
    return render_template('admin_dashboard.html', posters=posters_data.get("posters", []))


@app.route("/admin/poster/new")
def admin_new_poster():
    """New poster form - requires authentication"""
    if not session.get('authenticated'):
        return redirect('/admin')
    
    return render_template('admin_new_poster.html')


@app.route("/admin/poster/create", methods=["POST"])
def admin_create_poster():
    """Create new poster - requires authentication"""
    if not session.get('authenticated'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        poster_id = request.form.get('id')
        poster_name = request.form.get('name')
        poster_description = request.form.get('description', '')
        
        if not poster_id or not poster_name:
            return jsonify({"error": "ID and name are required"}), 400
        
        # Check if ID already exists
        if get_poster_by_id(poster_id):
            return jsonify({"error": "Poster ID already exists"}), 400
        
        # Handle image upload
        image_file = request.files.get('image')
        if not image_file or not allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
            return jsonify({"error": "Valid image file (PNG, JPG, PDF) required"}), 400
        
        image_filename = secure_filename(f"{poster_id}_{image_file.filename}")
        image_path = os.path.join(POSTERS_FOLDER, image_filename)
        image_file.save(image_path)
        
        # Convert PDF to PNG if needed
        if image_filename.lower().endswith('.pdf'):
            try:
                doc = fitz.open(image_path)
                page = doc[0]
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                png_filename = image_filename.rsplit('.', 1)[0] + '.png'
                png_path = os.path.join(POSTERS_FOLDER, png_filename)
                pix.save(png_path)
                doc.close()
                os.remove(image_path)  # Remove PDF
                image_filename = png_filename
            except Exception as e:
                return jsonify({"error": f"PDF conversion failed: {str(e)}"}), 500
        
        # Handle music upload
        music_file = request.files.get('music')
        if not music_file or not allowed_file(music_file.filename, ALLOWED_AUDIO_EXTENSIONS):
            return jsonify({"error": "Valid MP3 file required"}), 400
        
        music_filename = secure_filename(f"music_{poster_id}.{music_file.filename.rsplit('.', 1)[-1]}")
        music_path = os.path.join(MUSIC_FOLDER, music_filename)
        music_file.save(music_path)
        
        # Generate QR code
        qr_filename = generate_qr_for_poster(poster_id)
        
        # Create sections file for this poster
        sections_filename = f"sections_{poster_id}.json"
        sections_path = os.path.join(JSON_FOLDER, sections_filename)
        with open(sections_path, 'w', encoding='utf-8') as f:
            json.dump({"sections": []}, f, indent=2)
        
        # Add poster to database
        posters_data = load_posters()
        new_poster = {
            "id": poster_id,
            "name": poster_name,
            "description": poster_description,
            "image": image_filename,
            "music": music_filename,
            "sections_file": sections_filename,
            "created": datetime.now().strftime("%Y-%m-%d"),
            "qr_code": qr_filename
        }
        posters_data["posters"].append(new_poster)
        
        if not save_posters(posters_data):
            return jsonify({"error": "Failed to save poster database"}), 500
        
        return jsonify({"success": True, "poster_id": poster_id})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/admin/poster/<poster_id>/edit")
def admin_edit_poster(poster_id):
    """Edit poster sections - requires authentication"""
    if not session.get('authenticated'):
        return redirect('/admin')
    
    poster = get_poster_by_id(poster_id)
    if not poster:
        return "Poster not found", 404
    
    qr_path = url_for('static', filename=f"qr/{poster['qr_code']}") if poster.get('qr_code') else None
    poster_img = url_for('static', filename=f"posters/{poster['image']}") if poster.get('image') else None
    
    return render_template('admin.html', 
                         qr_path=qr_path, 
                         poster_img=poster_img,
                         poster=poster,
                         poster_id=poster_id)


@app.route("/admin/poster/<poster_id>/delete", methods=["POST"])
def admin_delete_poster(poster_id):
    """Delete poster - requires authentication"""
    if not session.get('authenticated'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        poster = get_poster_by_id(poster_id)
        if not poster:
            return jsonify({"error": "Poster not found"}), 404
        
        # Delete files with folder mapping
        file_folder_mapping = [
            (poster.get('image'), POSTERS_FOLDER),
            (poster.get('music'), MUSIC_FOLDER),
            (poster.get('sections_file'), JSON_FOLDER),
            (poster.get('qr_code'), QR_FOLDER)
        ]
        
        for filename, folder in file_folder_mapping:
            if filename:
                file_path = os.path.join(folder, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
        
        # Remove from database
        posters_data = load_posters()
        posters_data["posters"] = [p for p in posters_data["posters"] if p["id"] != poster_id]
        
        if not save_posters(posters_data):
            return jsonify({"error": "Failed to update database"}), 500
        
        return jsonify({"success": True})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/admin/login", methods=["POST"])
def admin_login():
    """Authenticate admin"""
    password = request.form.get('password')
    if password == ADMIN_PASSWORD:
        session['authenticated'] = True
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Invalid password"}), 401


@app.route("/admin/logout", methods=["POST"])
def admin_logout():
    """Logout admin"""
    session.pop('authenticated', None)
    return jsonify({"success": True})


@app.route("/admin/upload-music", methods=["POST"])
def upload_music():
    """Upload music file for a poster"""
    if not session.get('authenticated'):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    try:
        if 'music' not in request.files:
            return jsonify({"success": False, "error": "No file provided"}), 400
        
        file = request.files['music']
        poster_id = request.form.get('poster_id', 'scrc-architecture')
        
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected"}), 400
        
        if file and allowed_file(file.filename, ALLOWED_AUDIO_EXTENSIONS):
            # First, get the old music file to delete it
            posters_data = load_posters()
            old_music_file = None
            for poster in posters_data.get('posters', []):
                if poster['id'] == poster_id:
                    old_music_file = poster.get('music') or poster.get('audio')
                    break
            
            # Delete old music file if it exists
            if old_music_file:
                old_filepath = os.path.join(MUSIC_FOLDER, old_music_file)
                if os.path.exists(old_filepath):
                    try:
                        os.remove(old_filepath)
                        print(f"Deleted old music file: {old_filepath}")
                    except Exception as e:
                        print(f"Error deleting old music file: {e}")
            
            # Secure the filename and get extension
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'mp3'
            # Save with poster-specific name, preserving extension
            music_filename = f"music_{poster_id}.{file_ext}"
            filepath = os.path.join(MUSIC_FOLDER, music_filename)
            
            # Save the new file
            file.save(filepath)
            print(f"Saved new music file: {filepath}")
            
            # Update poster data with new music filename
            for poster in posters_data.get('posters', []):
                if poster['id'] == poster_id:
                    poster['music'] = music_filename
                    break
            
            save_posters(posters_data)
            
            return jsonify({
                "success": True,
                "message": "Music uploaded successfully",
                "music_url": f"/music/{poster_id}"
            })
        else:
            return jsonify({"success": False, "error": "Invalid file type. Supported: MP3, WAV, OGG, M4A, AAC"}), 400
    
    except Exception as e:
        print(f"Music upload error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/sections", methods=["GET"])
def get_sections():
    """Get sections configuration for a poster"""
    poster_id = request.args.get('poster_id', 'scrc-architecture')  # Default to legacy
    poster = get_poster_by_id(poster_id)
    
    if poster:
        sections_file = os.path.join(JSON_FOLDER, poster['sections_file'])
    else:
        # Fallback to legacy sections.json
        sections_file = os.path.join(JSON_FOLDER, "sections.json")
    
    try:
        if os.path.exists(sections_file):
            with open(sections_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data)
        else:
            return jsonify({"sections": []})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/sections", methods=["POST"])
def save_sections():
    """Save sections configuration - requires authentication"""
    if not session.get('authenticated'):
        return jsonify({"error": "Unauthorized"}), 401

    # Safely parse JSON body (may be None if client didn't send JSON)
    data = request.get_json(silent=True) or {}

    # Determine which poster's sections to save
    poster_id = request.args.get('poster_id') or data.get('poster_id', 'scrc-architecture')
    poster = get_poster_by_id(poster_id)
    
    if poster:
        sections_file = os.path.join(JSON_FOLDER, poster['sections_file'])
    else:
        sections_file = os.path.join(JSON_FOLDER, "sections.json")
    
    try:
        # Remove poster_id from data if present
        data.pop('poster_id', None)

        # Ensure we always write an object with a "sections" array
        # (keeps compatibility with existing readers)
        if isinstance(data, list):
            data = {"sections": data}
        elif "sections" not in data:
            data["sections"] = data.get("sections", [])
        
        os.makedirs(JSON_FOLDER, exist_ok=True)
        with open(sections_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return jsonify({"success": True, "message": "Sections saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def convert_pdf_to_poster():
    """Convert first page of PDF to poster1.png if no poster image exists"""
    # Check if poster already exists
    for ext in ['jpg', 'jpeg', 'png']:
        if os.path.exists(os.path.join('static', f'poster1.{ext}')):
            return
    
    # Look for PDF and convert
    try:
        for f in os.listdir('static'):
            if f.lower().endswith('.pdf'):
                pdf_path = os.path.join('static', f)
                doc = fitz.open(pdf_path)
                page = doc[0]
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better quality
                img_path = os.path.join('static', 'poster1.png')
                pix.save(img_path)
                doc.close()
                print(f"Converted {f} to poster1.png")
                break
    except Exception as e:
        print(f"Failed to convert PDF: {e}")


if __name__ == "__main__":
    # Initialize poster database if it doesn't exist
    if not os.path.exists(POSTERS_FILE):
        print("Initializing poster database...")
        os.makedirs('static', exist_ok=True)
        
        # Create default poster entry from existing files
        default_poster = {
            "id": "scrc-architecture",
            "name": "SCRC Poster Gallery",
            "description": "Living Lab Data Architecture",
            "image": "poster1.png",
            "music": "music.mp3",
            "sections_file": "sections.json",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "qr_code": "music_qr.png"
        }
        
        save_posters({"posters": [default_poster]})
        
        # Generate QR for default poster
        generate_qr_for_poster("scrc-architecture")
    
    # Convert PDF to image if needed
    convert_pdf_to_poster()

    print(f"Server starting on http://0.0.0.0:{PORT}")
    print("Admin login at http://localhost:" + str(PORT) + "/admin")
    print("Press Ctrl+C to stop.")
    app.run(host="0.0.0.0", port=PORT, debug=True)
