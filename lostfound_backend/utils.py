import os
from werkzeug.utils import secure_filename
from config import Config
def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in Config.ALLOWED_EXTENSIONS
def save_image(file,folder,prefix=""):
    os.makedirs(folder,exist_ok=True)
    name=secure_filename(file.filename)
    if prefix: name=f"{prefix}_{name}"
    path=os.path.join(folder,name)
    file.save(path)
    return name