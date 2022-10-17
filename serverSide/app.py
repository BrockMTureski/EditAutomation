from flask import Flask

app=Flask(__name__)

UPLOAD_FOLDER = "C:\\Users\\Brock\Desktop\\editAutomation\\serverSide\\input"
OUTPUT_FOLDER = "C:\\Users\\Brock\\Desktop\\editAutomation\\serverSide\\output"

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


#Folder output for clips to be output to
outputDir="C:\\Users\\Brock\\Desktop\\editAutomation\\serverSide\\output\\"
#Folder for clip being edited
inputDir="C:\\Users\\Brock\\Desktop\\editAutomation\\serverSide\\input\\"