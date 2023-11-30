import os

from flask import Flask, request, render_template, jsonify, url_for
import atexit
import shutil

from orchestrator.main_user_flow import flow

app = Flask(__name__)


static_dir = "static"
temp_dir = os.path.join(static_dir, "temp")

if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)


@app.route("/")
def index():
    return render_template("find.html")


@atexit.register
def cleanup():
    try:
        shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Error during cleanup: {e}")


@app.route("/process_image", methods=["POST"])
def process_image():
    if "file" not in request.files:
        return render_template("find.html", message="No file part")

    file = request.files["file"]

    if file.filename == "":
        return render_template("find.html", message="No selected file")

    target_path = os.path.join(temp_dir, file.filename)
    file.save(target_path)

    # Perform image processing (replace this with your actual image processing logic)
    outfits = flow(target_path, temp_dir)
    outfits = [
        url_for(static_dir, filename=f"temp/{os.path.basename(out_url)}")
        for out_url in outfits
    ]
    target_path = url_for(static_dir, filename=f"temp/{file.filename}")

    return render_template(
        "find.html",
        message="Image processed successfully",
        outfits_paths=outfits,
        target_path=target_path,
    )


if __name__ == "__main__":
    app.run(debug=True)
