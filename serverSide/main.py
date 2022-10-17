import os
import app as app
import modules
from flask import request, Flask,send_from_directory,jsonify,Response
from werkzeug.utils import secure_filename
import zipfile


App = Flask(__name__)
App.secret_key = "secret key"
App.config['UPLOAD_FOLDER'] = app.UPLOAD_FOLDER
App.config['OUTPUT_FOLDER'] = app.OUTPUT_FOLDER


@App.route('/upload',methods=['POST'])
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
            if modules.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(App.config['UPLOAD_FOLDER'],filename))
        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Only .mp4 and .zip files are allowed.'})
        resp.status_code = 400
        return resp


@App.route('/test',methods=['GET'])
def test():
    resp=jsonify({'message':"running."})

    return resp


@App.route('/show-input',methods=['GET'])
def showIn():
    message=modules.showDir(App.config['UPLOAD_FOLDER'])
    resp=jsonify({'message' : message})
    resp.status_code=200
    return resp


@App.route('/show-output',methods=['GET'])
def showOut():
    message=modules.showDir(App.config['OUTPUT_FOLDER'])
    resp=jsonify({'message' : message})
    resp.status_code=200
    return resp


@App.route('/clear-input',methods=['GET'])
def clearIn():
    tempBool=modules.clearDir(App.config['UPLOAD_FOLDER'])
    print(App.config['UPLOAD_FOLDER'])
    if tempBool is True:
        resp=jsonify({'message' : "Input folder cleared."})
        resp.status_code=200
    if tempBool is False:
        resp=jsonify({'message' : "Unable to clear input folder."})
        resp.status_code=400
    return resp


@App.route('/clear-output',methods=['GET'])
def clearOut():
    tempBool=modules.clearDir(App.config['OUTPUT_FOLDER'])
    print(App.config['OUTPUT_FOLDER'])
    if tempBool is True:
        resp=jsonify({'message' : "Output folder cleared."})
        resp.status_code=200
    if tempBool is False:
        resp=jsonify({'message' : "Unable to clear output folder."})
        resp.status_code=400
    return resp


@App.route('/download',methods=['GET'])
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


@App.route('/delZip',methods=['GET'])
def delzip():
    r=modules.delFile('EditedFiles.zip')
    if r is True:
        resp=jsonify({'message':'Download file deleted.'})
        resp.status_code=200
        return resp
    else:
        resp=jsonify({'message':'Failed to delete download file.'})
        resp.status_code=200


@App.route('/run/<sensitivity>',methods=['GET'])
def run(sensitivity=0.5):
    sens=float(sensitivity)
    r= modules.main(sens)
    resp=jsonify({'message':'Video automation complete. Download available.'})
    resp.status_code=200
    return resp


if __name__ == "__main__":
    App.run(debug=True,port=8080)