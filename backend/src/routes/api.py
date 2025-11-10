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

    # resolve temp paths relative to this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.normpath(os.path.join(base_dir, "..", "temp"))
    os.makedirs(temp_dir, exist_ok=True)
    upload_path = os.path.join(temp_dir, "input.png")
    output_path = os.path.join(temp_dir, "output.png")

    file.save(upload_path)

    # read image (preserve alpha if present)
    raw = cv2.imread(upload_path, cv2.IMREAD_UNCHANGED)
    if raw is None:
        return ("Invalid image", 400)

    # separate alpha channel if present
    alpha = None
    if raw.ndim == 3 and raw.shape[2] == 4:
        b, g, r, alpha = cv2.split(raw)
        image_bgr = cv2.merge([b, g, r])
    else:
        image_bgr = raw

    # normalize to [0,1] and apply gamma where gamma>1 darkens: out = in^gamma
    image_f = image_bgr.astype(np.float32) / 255.0
    corrected = np.power(image_f, gamma)
    timage = np.clip(corrected * 255.0, 0, 255).astype(np.uint8)

    # reattach alpha if needed
    if alpha is not None:
        timage = cv2.merge([timage[:, :, 0], timage[:, :, 1], timage[:, :, 2], alpha])

    cv2.imwrite(output_path, timage)

    resp = send_file(output_path, mimetype="image/png")
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    return resp
