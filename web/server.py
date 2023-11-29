import os

from flask import Flask, request, render_template, jsonify, url_for

from orchestrator.main_user_flow import flow

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('find.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return render_template('find.html', message='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('find.html', message='No selected file')

    # Save the uploaded image to a temporary file
    temp_path = 'web/static/temp_image.jpg'
    file.save(temp_path)

    # Perform image processing (replace this with your actual image processing logic)
    outfits = flow(temp_path, "web/static")
    outfits = [url_for('static', filename=f"{out_url}") for out_url in outfits]
    target_path = url_for('static', filename="temp_image.jpg")

    return render_template('find.html', message='Image processed successfully', outfits_paths=outfits, target_path=target_path)


if __name__ == '__main__':
    app.run(debug=True)
