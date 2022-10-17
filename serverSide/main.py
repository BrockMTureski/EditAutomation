import os
import urllib.request
from app import app
import modules
from flask import Flask, request, send_file,send_from_directory,jsonify,Response
from werkzeug.utils import secure_filename
import zipfile


ALLOWED_FILE_TYPE=set(['mp4','txt'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_TYPE


@app.route('/upload',methods=['POST'])
def uploadFile():
    # ensure post has file
    files = request.files.getlist("file")
    print(files)
    if request.files['file'].filename == '':
        resp=jsonify({'message':'no file uploaded'})
        resp.status_code = 400
        return resp 

    files = request.files.getlist("file")

    if files:
        for file in files:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Only .mp4 files are allowed.'})
        resp.status_code = 400
        return resp


@app.route('/test',methods=['GET'])
def test():
    resp=jsonify({'message':"running."})

    return resp


@app.route('/show-input',methods=['GET'])
def show():
    message=modules.showDir(app.config['UPLOAD_FOLDER'])
    resp=jsonify({'message' : message})
    resp.status_code=200
    return resp


@app.route('/show-output',methods=['GET'])
def show():
    message=modules.showDir(app.config['OUTPUT_FOLDER'])
    resp=jsonify({'message' : message})
    resp.status_code=200
    return resp


@app.route('/clear-input',methods=['GET'])
def clearIn():
    tempBool=modules.clearDir(app.config['UPLOAD_FOLDER'])
    print(app.config['UPLOAD_FOLDER'])
    if tempBool is True:
        resp=jsonify({'message' : "Input folder cleared."})
        resp.status_code=200
    if tempBool is False:
        resp=jsonify({'message' : "Unable to clear input folder."})
        resp.status_code=400
    return resp


@app.route('/clear-output',methods=['GET'])
def clearOut():
    tempBool=modules.clearDir(app.config['OUTPUT_FOLDER'])
    print(app.config['OUTPUT_FOLDER'])
    if tempBool is True:
        resp=jsonify({'message' : "Output folder cleared."})
        resp.status_code=200
    if tempBool is False:
        resp=jsonify({'message' : "Unable to clear output folder."})
        resp.status_code=400
    return resp


@app.route('/download',methods=['GET'])
def download():
    try:
        zipfolder=zipfile.ZipFile('EditedFiles.zip','w',compression=zipfile.ZIP_STORED)
        modules.zip('C:\\Users\\Brock\\Desktop\\editAutomation\\serverSide\\output',zipfolder)
        zipfolder.close    
        return Response(open("C:\\Users\\Brock\\Desktop\\editAutomation\\EditedFiles.zip",'rb'))
    except:
        resp=jsonify({'message':'ERROR downloading.'})
        resp.status_code=400
        return resp


@app.route('/run/<sensitivity>',methods=['GET'])
def run(sensitivity=0.5):
    sens=float(sensitivity)
    r= modules.main(sens)
    resp=jsonify({"message":"video automation complete. Download available."})
    resp.status_code=200
    return resp


if __name__ == "__main__":
    app.run(debug=True)

