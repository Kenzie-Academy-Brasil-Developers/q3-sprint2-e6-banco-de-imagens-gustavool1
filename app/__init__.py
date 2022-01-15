from os import getenv, mkdir
from flask import Flask, request
from zipfile import ZipFile
from kenzie.image import route_upload, list_file_route, list_files_by_extension_route, download_file_route, download_dir_as_zip_route

app = Flask(__name__)

MAX_CONTENT_LENGTH = getenv('MAX_CONTENT_LENGTH')
app.config['MAX_CONTENT_LENGTH'] = int(MAX_CONTENT_LENGTH) * 1024 * 1024
ALLOWED_EXTENSIONS = getenv('ALLOWED_EXTENSIONS')
FILES_DIRECTORY = getenv("FILES_DIRECTORY")

try:
    mkdir("folders")
    mkdir(f"folders/zip")
    
except FileExistsError:
    pass

try:
    for extension in ALLOWED_EXTENSIONS.split(","):
        mkdir(f"{FILES_DIRECTORY}/{extension}")
    
except FileExistsError:
    pass


@app.get('/download/<name_extension>')
def download_file(name_extension):
    return download_file_route(name_extension)


@app.get("/download-zip")
def download_dir_as_zip():
    file_type = request.args.get("file_extension")
    compression_ratio = request.args.get("comprenssion_ratio", 6)
    
    if  file_type not in ALLOWED_EXTENSIONS.split(","):
        return {"msg":"Extension not allowed"}, 404

    return download_dir_as_zip_route(file_type, compression_ratio)




@app.get("/files")
def list_files():
    return list_file_route()
    



@app.get("/files/<extension>")
def list_files_by_extension(extension):
    return list_files_by_extension_route(extension)




@app.post("/upload")
def upload():
    return route_upload()

        


