from flask import Blueprint, render_template, session, redirect, url_for, request
from google_photos import GooglePhotos
import os

bp = Blueprint('main', __name__)

# Initialize Google Photos API client
google_photos_client = GooglePhotos(
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    redirect_uri=os.environ.get("GOOGLE_REDIRECT_URI")
)

@bp.route('/')
def index():
    # Check if the user is authenticated
    if 'credentials' not in session:
        return redirect(url_for('auth.login'))

    # Get the user's Google Photos albums or images (modify this logic as needed)
    albums_or_images = google_photos_client.get_albums_or_images()

    return render_template('index.html', albums_or_images=albums_or_images)

@bp.route('/process_image/<image_id>')
def process_image(image_id):
    # Check if the user is authenticated
    if 'credentials' not in session:
        return redirect(url_for('auth.login'))

    # Perform image processing (flipping) logic here (modify this logic as needed)
    result = google_photos_client.process_image(image_id)

    if result:
        return render_template('success.html', image_id=image_id)
    else:
        return render_template('error.html', message='Image processing failed')
