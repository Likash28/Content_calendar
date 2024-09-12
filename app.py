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


from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.objectid import ObjectId
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Set a secret key for session management

# MongoDB connection setup
try:
    print("Connecting to MongoDB...")
    client = MongoClient("mongodb+srv://likashgunisetti:4wYTzaQVIR3hV1GB@cluster0.zqe2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.calender
    print("MongoDB connection successful.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Cloudinary configuration
cloudinary.config(
    cloud_name="dcoszqcjp",
    api_key="551166384184842",
    api_secret="Wwq7L4NOHUUXMfgKFmT7eNzd5f4"
)

# Upload configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    allowed = '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    print(f"File '{filename}' allowed: {allowed}")
    return allowed

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            print("Form submission received.")

            # Get form data
            First_Name = request.form["First_Name"]
            Last_Name = request.form["Last_Name"]
            Country = request.form["country"]
            industry = request.form["industry"]
            print(f"Form Data - First Name: {First_Name}, Last Name: {Last_Name}, Country: {Country}, Industry: {industry}")

            # Check if the file is included in the request
            if 'file' not in request.files:
                flash('No file part in the request', 'error')
                print("No file part in the request.")
                return redirect(request.url)

            file = request.files['file']

            # Check if a file was actually selected
            if file.filename == '':
                flash('No file selected', 'error')
                print("No file selected.")
                return redirect(request.url)

            # Validate file extension
            if not allowed_file(file.filename):
                flash('File type not allowed. Only PDF, DOC, and DOCX are accepted.', 'error')
                print(f"Invalid file extension for file: {file.filename}")
                return redirect(request.url)

            # Secure filename and upload to Cloudinary
            filename = secure_filename(file.filename)
            print(f"Uploading file '{filename}' to Cloudinary...")
            result = cloudinary.uploader.upload(file)
            file_url = result['secure_url']
            print(f"File uploaded to Cloudinary: {file_url}")

            # Prepare data for MongoDB
            data = {
                "First_Name": First_Name,
                "Last_Name": Last_Name,
                "country": Country,
                "industry": industry,
                "file_url": file_url
            }

            # Insert data into MongoDB
            print("Inserting data into MongoDB...")
            db.formdata.insert_one(data)
            print(f"Data inserted successfully into MongoDB: {data}")

            return render_template('target.html', file_url=file_url)

        except Exception as e:
            flash(f"An error occurred: {e}", 'error')
            print(f"Error during form submission: {e}")
            return redirect(request.url)

    print("Rendering index page.")
    return render_template('index.html')

@app.route('/target')
def target():
    print("Rendering target page.")
    return render_template('target.html')

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(debug==False, host='0.0.0.0')
