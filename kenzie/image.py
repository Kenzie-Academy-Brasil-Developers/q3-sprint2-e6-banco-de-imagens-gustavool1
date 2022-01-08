import os
from flask import request
from app import  ALLOWED_EXTENSIONS


def testii():
    print("abcd")
# def is_extension_allowed(extension):
#     if extension not in ALLOWED_EXTENSIONS:
#         return False
#     return True


# def upload_route():
#     key = request.files.keys()
#     archive = request.files.get(*key)
#     _name,extension = os.path.splitext(archive.filename)

#     if not is_extension_allowed(extension[1::]):
#         return {"msg": "extension not allowed"}, 415

#     else:

#         path = f"./{extension[1::]}/{archive.filename}"
#         file_exists = os.path.isfile(path)
#         if file_exists:
#             return {"msg":"the file already exists"}, 409
        
#         archive.save(path)
#         return {"msg":"archive uploaded"}, 201