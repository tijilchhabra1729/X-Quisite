import os
import secrets
from PIL import Image

from flask import url_for, current_app

def add_car_pic(pic_upload,username):

    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    random = secrets.token_hex(8)
    storage_filename = str(username) + '_'+ random + '_' + 'car' +'.' +ext_type
    filepath = os.path.join(current_app.root_path, 'static', storage_filename)

    # Play Around with this size.
    output_size = (1000 , 1000)

    # Open the picture and save it
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename
