# from flask import Flask, render_template, redirect, url_for, request
# from werkzeug.utils import secure_filename
# # for mongoDB connect with python we need below libraries
# from pymongo import MongoClient
# from bson.objectid import ObjectId

# # to upload the data
# import cloudinary.uploader

# app = Flask(__name__)


# client = MongoClient("mongodb+srv://likashgunisetti:4wYTzaQVIR3hV1GB@cluster0.zqe2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


# # username = 'likashgunisetti'
# # password = '4wYTzaQVIR3hV1GB'

# # connection string for MongoDB Local usage
# # client = MongoClient("mongodb://localhost:27017")
# db = client.calender

# # Provide your Cloudinary credentials

# # Cloudinary configuration
# cloudinary.config(
#     cloud_name="dcoszqcjp",
#     api_key="551166384184842",
#     api_secret="Wwq7L4NOHUUXMfgKFmT7eNzd5f4"
# )



# app.config['UPLOAD_FOLDER'] = 'uploads'  # Directory to save uploaded files
# app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}  # Allowed file extensions




# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         First_Name = request.form["First_Name"]
#         Last_Name = request.form["Last_Name"]
#         Country = request.form["country"]
#         industry = request.form["industry"]

#         # Check if a file is included in the request
#         if 'file' not in request.files:
#             return "No file part in the request"

#         file = request.files['file']

#         # Check if a file was actually selected
#         if file.filename == '':
#             return "No selected file"

#         # Upload file to Cloudinary
#         if file:
#             filename = secure_filename(file.filename)
#             result = cloudinary.uploader.upload(file)
#             file_url = result['secure_url']
#             print("PDF Uploaded to Cloudinary is:", file_url)

#             # Store the file URL from Cloudinary along with other form data
#             # file_url = result.get("url")

#             # Create the data dictionary to insert into MongoDB
#             data = {
#                 "First_Name": First_Name,
#                 "Last_Name": Last_Name,
#                 "country": Country,
#                 "industry": industry,
#                 "file_url": file_url  # Store the Cloudinary URL in MongoDB
#             }

#             # Insert the data into MongoDB
#             db.formdata.insert_one(data)
#             print(data)
#             return render_template('target.html', file_url=file_url)

#     return render_template('index.html')



# @app.route('/target')
# def target():
#     return render_template('target.html')

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')

from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
# for mongoDB connect with python we need below libraries
from pymongo import MongoClient
from bson.objectid import ObjectId
import docx2pdf 
# to upload the data
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import os
import tempfile
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import cloudinary
import cloudinary.uploader
from docx2pdf import convert
from io import BytesIO
app = Flask(__name__)


client = MongoClient("mongodb+srv://likashgunisetti:4wYTzaQVIR3hV1GB@cluster0.zqe2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


# username = 'likashgunisetti'
# password = '4wYTzaQVIR3hV1GB'

# connection string for MongoDB Local usage
# client = MongoClient("mongodb://localhost:27017")
db = client.calender

# Provide your Cloudinary credentials

# Cloudinary configuration
cloudinary.config(
    cloud_name="dcoszqcjp",
    api_key="551166384184842",
    api_secret="Wwq7L4NOHUUXMfgKFmT7eNzd5f4"
)



app.config['UPLOAD_FOLDER'] = 'uploads'  # Directory to save uploaded files
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}  # Allowed file extensions



def convert_to_pdf(file):
    if file.filename.endswith('.pdf'):
        return file.read()  # Already a PDF
    else:
        # Save the uploaded .doc or .docx file to a temporary directory
        temp_dir = tempfile.mkdtemp()
        filepath = os.path.join(temp_dir, secure_filename(file.filename))
        file.save(filepath)

        # Convert the file to PDF
        output_pdf_path = os.path.join(temp_dir, 'output.pdf')
        convert(filepath, output_pdf_path)  # Converts the file to PDF
        
        # Open the converted PDF to return it
        with open(output_pdf_path, 'rb') as pdf_file:
            pdf_bytes = BytesIO(pdf_file.read())

        # Clean up temporary files
        os.remove(filepath)
        os.remove(output_pdf_path)
        os.rmdir(temp_dir)

        return pdf_bytes



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        First_Name = request.form["First_Name"]
        Last_Name = request.form["Last_Name"]
        Country = request.form["country"]
        industry = request.form["industry"]

        # Capture selected audience checkboxes
        selected_audience = request.form.getlist('audience')

        # Check if a file is included in the request
        if 'file' not in request.files:
            return "No file part in the request"

        file = request.files['file']

        # Check if a file was actually selected
        if file.filename == '':
            return "No selected file"

        # Check if the file is allowed
        if file and allowed_file(file.filename):
            if file.filename.endswith('.pdf'):
                # Handle PDF file upload
                result = cloudinary.uploader.upload(file)
                file_url = result['secure_url']
                print("PDF Uploaded to Cloudinary is:", file_url)

                # Create the data dictionary to insert into MongoDB
                data = {
                    "First_Name": First_Name,
                    "Last_Name": Last_Name,
                    "country": Country,
                    "industry": industry,
                    "selected_audience": selected_audience,
                    "file_url": file_url
                }

                # Insert the data into MongoDB
                db.formdata.insert_one(data)
                print(data)
                return render_template('target.html', file_url=file_url)

            else:
                # Convert non-PDF files to PDF
                pdf_bytes = convert_to_pdf(file)
                result = cloudinary.uploader.upload(pdf_bytes, resource_type='raw')
                file_url = result['secure_url']
                print("Converted PDF Uploaded to Cloudinary is:", file_url)

                # Create the data dictionary to insert into MongoDB
                data = {
                    "First_Name": First_Name,
                    "Last_Name": Last_Name,
                    "country": Country,
                    "industry": industry,
                    "selected_audience": selected_audience,
                    "file_url": file_url
                }

                # Insert the data into MongoDB
                db.formdata.insert_one(data)
                print(data)
                return render_template('target.html', file_url=file_url)

        else:
            return render_template('index.html', error_message="File type not allowed. Please upload a PDF or a Word document.")

    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/target')
def target():

    if request.method == 'POST':
    # Capture selected audience checkboxes
        selected_audience = request.form.getlist('audience')  # This will capture all selected checkboxes as a list
    
    # Assuming additional data needs to be handled or logged, e.g., MongoDB insert
    # If you want to store this into MongoDB, you can include it like this:
    data = {
        "selected_audience": selected_audience  # Store the selected audience in MongoDB
        }

    # Insert into MongoDB if needed
    db.audience_selection.insert_one(data)

    print("Selected Audience:", selected_audience)
    
    return render_template('target.html', selected_audience=selected_audience)
        

        # return render_template('target.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
