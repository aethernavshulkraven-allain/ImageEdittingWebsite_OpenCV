from flask import Flask, render_template, request, redirect, url_for, send_file
import cv2
import numpy as np
import os

app = Flask(__name__)

croppingFlag = False
ix = -1
iy = -1
img = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global croppingFlag, ix, iy, img

    if 'image' in request.files:
        image_file = request.files['image']

        # Check if the file is allowed
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
        if '.' in image_file.filename and image_file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
            # Read the image as a NumPy array
            image_data = np.frombuffer(image_file.read(), np.uint8)
            img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

            cv2.namedWindow(winname="window")
            cv2.setMouseCallback("window", cropper)

            # Save the image to a file for display
            image_path = 'static/uploads/input_image.jpg'
            cv2.imwrite(image_path, img)
        else:
            return redirect(url_for('index'))

    return render_template('index.html', image_path=image_path)

@app.route('/get_image')
def get_image():
    if img is not None:
        _, buffer = cv2.imencode('.jpg', img)
        return send_file(
            io.BytesIO(buffer),
            mimetype='image/jpeg',
            as_attachment=True,
            download_name='image.jpg'
        )
    return 'Image not found', 404

if __name__ == '__main__':
    app.run(debug=True)
