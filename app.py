import os
from flask import Flask, flash, request, redirect, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import pytesseract
from PyPDF2 import PdfFileMerger, PdfFileReader
from merge_pdf import merge_pdf

app=Flask(__name__)

try:
    pytesseract.get_tesseract_version()
except pytesseract.pytesseract.TesseractNotFoundError as e:
    print(e)
    os.system('sudo apt install tesseract-ocr')
except Exception as e:
    print(e,type(e))

app.secret_key = "secret key"
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

GENERATED_FOLDER = os.path.join(path, 'generated')
out_file = os.path.join(GENERATED_FOLDER ,'your_notes.pdf')

if not os.path.exists(GENERATED_FOLDER):
    os.mkdir(GENERATED_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    #print("upload called")
    if request.method == 'POST':

        if os.path.exists(out_file):
            os.remove(out_file)
        
        # Get the file from post request
        files = request.files

        f_names = [] #stores name of files in sequence
        for file_id in files:
            
            filename = secure_filename(files[file_id].filename)
            if allowed_file(filename):
                f_names.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                files[file_id].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        print("File recived and saved.")
        
        ### convert to pdf ###
        results = []
        for f_name in f_names:
            result = pytesseract.image_to_pdf_or_hocr(f_name, extension='pdf')
            results.append(result)




        pdf_names = []  
        for i,f_name in enumerate(f_names):
            pdf_name = os.path.join(GENERATED_FOLDER,
                                    os.path.basename(f_name).rsplit('.',1)[0]+'.pdf')
            pdf_names.append(pdf_name)

            with open( pdf_name, 'wb') as f:
                f.write(results[i])
            #delete the image file which is useless now
            os.remove(f_name)
        
        print("File converted and saved.")
        
        ### Merge the pdfs ###
        merge_pdf(pdf_names,out_file)
        print("Merged and saved.")

        [os.remove(pdf_name) for pdf_name in pdf_names]
        



        flash('File(s) successfully uploaded')
        return send_file(out_file)
        #return jsonify({"result": 'File(s) successfully uploaded'})




    return jsonify({"result": 'End'})



if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True,threaded=True)

