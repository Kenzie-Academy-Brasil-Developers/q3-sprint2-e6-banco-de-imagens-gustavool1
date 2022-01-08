import os
from flask import Flask, request, jsonify, send_from_directory
from zipfile import ZipFile
from kenzie.image import testii

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
# app.config['UPLOAD_FOLDER'] = '../downloads'
ALLOWED_EXTENSIONS = {'jpg','jpeg','png', 'gif'}


def is_extension_allowed(extension):
    if extension not in ALLOWED_EXTENSIONS:
        return False
    return True

def showing_dir_content(path):
    for dirpath, dirnames, filenames in os.walk(f'./{path}'):
        return filenames
    
def file_exists(filename):
    name = filename.split(".")[0]
    extension = filename.split(".")[1]
    os.system(f"cd {extension}")
    path = f"./{extension}/{filename}"
    exists = os.path.isfile(path)
    return exists

@app.before_request
def creating_dirs():
        directories = " ".join(ALLOWED_EXTENSIONS)
        os.system(f"mkdir {directories}")
        

@app.get('/download/<name_extension>')
def download_file(name_extension):
    
    dot_index = name_extension.index(".") + 1
    directorie = name_extension[dot_index::]

    directorie_content = showing_dir_content(directorie)
    if name_extension in directorie_content:

        print(directorie)
        return send_from_directory(
            directory=f"../../{directorie}",
            path=name_extension,
            as_attachment=True
        ),200
         
    return {"msg":"file doenst exist"}, 404


@app.get("/download-zip")
def download_dir_as_zip():
    
    query = request.args.get("filename")
    print(query)
    print(query)
    archive_name =query.split(".")[0]
    extension = query.split(".")[1]
    path = f'./{extension}/{query}'
    if file_exists(query):
        with ZipFile(f"./downloads/{archive_name}.zip", "w") as zipfile:
            zipfile.write(path)
            zipfile.close()
        return {"msg": 'Archive zipped successfully'},200
    return  {"msg": "File doenst exist"}, 404




@app.get("/files")
def list_files():
    
    dirs_content = []
    for extension in ALLOWED_EXTENSIONS:
        content = showing_dir_content(extension)
        dirs_content.extend(content)

    return jsonify(dirs_content), 200



@app.get("/files/<extension>")
def list_files_by_extension(extension):
    if extension not in ALLOWED_EXTENSIONS:
        return {"msg":"Extension not allowed"}, 404
    files = showing_dir_content(extension)
    return jsonify(files),200





@app.post("/upload")
def upload():

    key = request.files.keys()
    archive = request.files.get(*key)
    _name,extension = os.path.splitext(archive.filename)

    if not is_extension_allowed(extension[1::]):
        return {"msg": "extension not allowed"}, 415

    else:

        path = f"./{extension[1::]}/{archive.filename}"
        file_exists = os.path.isfile(path)
        if file_exists:
            return {"msg":"the file already exists"}, 409
        
        archive.save(path)
        return {"msg":"archive uploaded"}, 201
        


