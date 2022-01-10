from flask import request, jsonify, send_from_directory
import os 
from zipfile import ZipFile



ALLOWED_EXTENSIONS = {'jpg','jpeg','png', 'gif'}

def is_extension_allowed(extension):
    if extension not in ALLOWED_EXTENSIONS:
        return False
    return True


def showing_dir_content(path):
    for dirpath, dirnames, filenames in os.walk(f'./folders/{path}'):
        return filenames

def file_exists(filename):
    name = filename.split(".")[0]
    extension = filename.split(".")[1]
    os.system(f"cd {extension}")
    path = f"./folders/{extension}/{filename}"
    exists = os.path.isfile(path)
    return exists


def route_upload():
    key = request.files.keys()
    archive = request.files.get(*key)
    name,extension = os.path.splitext(archive.filename)

    if not is_extension_allowed(extension[1::]):
        return {"msg": "extension not allowed"}, 415

    else:

        path = f"./folders/{extension[1::]}/{archive.filename}"
        file_exists = os.path.isfile(path)
        if file_exists:
            return {"msg":"the file already exists"}, 409
        
        archive.save(path)
        return {"msg":"archive uploaded"}, 201




def list_file_route():

    dirs_content = []
    for extension in ALLOWED_EXTENSIONS:
        content = showing_dir_content(extension)
        dirs_content.extend(content)

    return jsonify(dirs_content), 200


def list_files_by_extension_route(extension):

    if extension not in ALLOWED_EXTENSIONS:
        return {"msg":"Extension not allowed"}, 404
    files = showing_dir_content(extension)
    return jsonify(files),200



def download_file_route(name_extension):
    
    dot_index = name_extension.index(".") + 1
    directorie = name_extension[dot_index::]

    directorie_content = showing_dir_content(directorie)
    if name_extension in directorie_content:

        return send_from_directory(
            directory=f"../folders/{directorie}",
            path=name_extension,
            as_attachment=True
        ),200
         
    return {"msg":"file doenst exist"}, 404


def download_dir_as_zip_route():
    query = request.args.get("filename")
    archive_name =query.split(".")[0]
    extension = query.split(".")[1]
    path = f'./folders/{extension}/{query}'
    if file_exists(query):
        with ZipFile(f"./folders/zip/{archive_name}.zip", "w") as zipfile:
            zipfile.write(path)
            zipfile.close()

        return send_from_directory(
            directory=f"../folders/zip",
            path=f"{archive_name}.zip",
            as_attachment=True
        ), 200
    return  {"msg": "File doenst exist"}, 404