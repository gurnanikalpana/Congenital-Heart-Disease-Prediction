from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from pyngrok import ngrok, conf
import os

# Set your Ngrok authentication token
conf.get_default().auth_token = "2fzZ9mFKlxpE2SSDZbp1qWJNf3L_51AZ1VGZ5DWGy2tcBa"

app = Flask(__name__)

# Set the upload folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return "<b style='text-align:center;'>Contact Page</b>"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return 'No selected file'

        # Securely save the file to the upload folder
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return 'File uploaded successfully'

    return render_template('upload.html')

# Start ngrok tunnel
public_url = ngrok.connect(5000)

print(" * Ngrok tunnel: ", public_url)

# Run Flask app
if __name__ == '__main__':
    app.run()
