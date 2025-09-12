import uuid
import os


def picture_upload_to(folder):
    while True:
        unique_name = f"{folder}/{uuid.uuid4().hex}.jpg"
        full_path = os.path.join("uploads", unique_name)
        if not os.path.exists(os.path.join("media", full_path)):
            return unique_name
