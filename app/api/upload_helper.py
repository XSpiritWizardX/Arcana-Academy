import os
import uuid

import cloudinary
import cloudinary.uploader

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "gif", "webp"}


cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True,
)

CLOUDINARY_UPLOAD_FOLDER = os.environ.get("CLOUDINARY_UPLOAD_FOLDER", "uploads")
CLOUDINARY_UPLOAD_PRESET = os.environ.get("CLOUDINARY_UPLOAD_PRESET")
DEFAULT_FOLDER = "user-uploads"


def get_unique_filename(filename):
    ext = filename.rsplit(".", 1)[1].lower()
    unique_filename = uuid.uuid4().hex
    return f"{unique_filename}.{ext}"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file_to_cloudinary(file):
    if not allowed_file(file.filename):
        return {"errors": "File type not permitted"}

    original_filename = file.filename
    try:
        upload_options = {
            "folder": CLOUDINARY_UPLOAD_FOLDER or DEFAULT_FOLDER,
            "public_id": file.filename,
            "use_filename": False,
            "unique_filename": False,
            "overwrite": False,
            "use_filename_as_display_name": True,
            "display_name": original_filename,
            "resource_type": "auto",
        }
        if CLOUDINARY_UPLOAD_PRESET:
            upload_options["upload_preset"] = CLOUDINARY_UPLOAD_PRESET

        upload = cloudinary.uploader.upload(file, **upload_options)
    except Exception as e:  # pragma: no cover - cloudinary raises many types
        return {"errors": str(e)}

    return {"url": upload.get("secure_url"), "public_id": upload.get("public_id")}


def remove_file_from_cloudinary(public_id):
    try:
        result = cloudinary.uploader.destroy(public_id, invalidate=True)
    except Exception as e:  # pragma: no cover
        return {"errors": str(e)}

    if isinstance(result, dict):
        if result.get("result") == "ok":
            return True
        return {"errors": result}

    if isinstance(result, str) and result == "ok":
        return True

    return {"errors": f"Unable to delete asset {public_id}"}
