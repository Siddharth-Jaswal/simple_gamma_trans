from flask import request, send_file, Blueprint
import cv2
import numpy as np
import os

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/gamma-transform", methods=["POST"])
def applyGammaTransform():
    file = request.files["file"]
    gamma = float(request.form["gamma"])

    # ensure gamma > 0
    if gamma <= 0:
        gamma = 0.1

    # paths
    upload_path = os.path.join("backend", "src", "temp", "input.png")
    output_path = os.path.join("backend", "src", "temp", "output.png")

    file.save(upload_path)

    # read and normalize
    image = cv2.imread(upload_path).astype(np.float32) / 255.0

    # gamma correction
    timage = np.power(image, gamma)
    timage = np.clip(timage * 255.0, 0, 255).astype(np.uint8)

    cv2.imwrite(output_path, timage)

    return send_file(output_path, mimetype="image/png")
