from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
# for mongoDB connect with python we need below libraries
from pymongo import MongoClient
from bson.objectid import ObjectId

# to upload the data
import cloudinary.uploader

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




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        First_Name = request.form["First_Name"]
        Last_Name = request.form["Last_Name"]
        Country = request.form["country"]
        industry = request.form["industry"]

        # Check if a file is included in the request
        if 'file' not in request.files:
            return "No file part in the request"

        file = request.files['file']

        # Check if a file was actually selected
        if file.filename == '':
            return "No selected file"

        # Upload file to Cloudinary
        if file:
            filename = secure_filename(file.filename)
            result = cloudinary.uploader.upload(file)
            file_url = result['secure_url']
            print("PDF Uploaded to Cloudinary is:", file_url)

            # Store the file URL from Cloudinary along with other form data
            # file_url = result.get("url")

            # Create the data dictionary to insert into MongoDB
            data = {
                "First_Name": First_Name,
                "Last_Name": Last_Name,
                "country": Country,
                "industry": industry,
                "file_url": file_url  # Store the Cloudinary URL in MongoDB
            }

            # Insert the data into MongoDB
            db.formdata.insert_one(data)
            print(data)
            return render_template('target.html', file_url=file_url)

    return render_template('index.html')



@app.route('/target')
def target():
    return render_template('target.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')