from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import cv2
import time

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename, operation):
    print(f"The operation is {operation} and the filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            new_file_name = f"static/{filename}"
            cv2.imwrite(new_file_name,imgProcessed)
            time.sleep(100)
            os.remove(f"uploads/{filename}")
            return new_file_name
        case "cwebp":
            new_file_name = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(new_file_name,img)
            # time.sleep(300)
            os.remove(f"uploads/{filename}")
            return new_file_name
        case "cpng":
            new_file_name = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(new_file_name,img)
            # time.sleep(300)
            os.remove(f"uploads/{filename}")
            return new_file_name
        case "cjpg":
            new_file_name = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(new_file_name,img)
            # time.sleep(300)
            os.remove(f"uploads/{filename}")
            return new_file_name
        
    pass

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
         # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and it is available <a href='/{new}'target = '_blank' >here</a>" )
            # time.sleep(10)
            # os.remove(f"static/{new}")
            return render_template("index.html")
            # new_filename = processImage(filename, operation)
            # if new_filename:
            #     flash(f"Your image has been processed and it is available <a href='/{new_filename}'>here</a>" )
            # else:
            #     flash("Error processing the image.")
            # return render_template("index.html")

    return render_template("index.html")



app.run(debug=True)