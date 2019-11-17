import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, send_file, url_for, jsonify
from s3_function import list_files, download_file, upload_file

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
BUCKET = "finalprojectawsrekognition"   

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/storage")
def storage():
    contents = list_files(BUCKET)
    return render_template('index.html', contents=contents)

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(f.filename)
        upload_file(f"{f.filename}", BUCKET)
        print(f)
        return redirect("/")

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)
        return send_file(output, as_attachment=True)

@app.route("/rekognition")
def image_rekognition():
    BUCKET = "finalprojectawsrekognition"
    KEY_SOURCE = "jessica1.jpeg"
    KEY_TARGET = "jessica2.jpg"

def compare_faces(bucket, key, bucket_target, key_target, threshold=80):
	rekognition = boto3.client("rekognition")
	response = rekognition.compare_faces(
	    SourceImage={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		TargetImage={
			"S3Object": {
				"Bucket": bucket_target,
				"Name": key_target,
			}
		},
	    SimilarityThreshold=threshold,
	)
	return response['SourceImageFace'], response['FaceMatches']


source_face, matches = compare_faces(BUCKET, KEY_SOURCE, BUCKET, KEY_TARGET)

# the main source face
print (f"Source_face: {source_face}")

# one match for each target face
for match in matches:
	print(match)

# @app.route('/hook')
# def get_image():
#     image_b64 = request.args.get('image')

#     content = image_b64.split(';')[1]
#     image_encoded = content.split(',')[1]
#     body = base64.decodebytes(image_encoded.encode('utf-8'))
#     return body

    # image_data = re.sub('^data:image/.+;base64,', '', image_b64).decode('base64')
    # image_PIL = Image.open(io.StringIO(image_b64))
    # image_np = np.array(image_PIL)
    # print ('Image received: {}'.format(image_np.shape))
    # print(image_np)


# @app.route("/data")
# def dataquery():
    
#     stmt = db.session.query(Metadata).statement
#     data = pd.read_sql_query(stmt, db.session.bind)
        
#     # Format the data to send as json
#     keys = ["Country","Continent",
#         "Bothsexes16","Male16","Female16","Bothsexes15","Male15","Female15",
#         "Bothsexes14","Male14","Female14","Bothsexes13","Male13","Female13",
#         "Bothsexes12","Male12","Female12","Bothsexes11","Male11","Female11",
#         "Bothsexes10","Male10","Female10","Bothsexes09","Male09","Female09",
#         "Bothsexes08","Male08","Female08","Bothsexes07","Male07","Female07",
#         "Bothsexes06","Male06","Female06","Bothsexes05","Male05","Female05",
#         "Bothsexes04","Male04","Female04","Bothsexes03","Male03","Female03",
#         "Bothsexes02","Male02","Female02","Bothsexes01","Male01","Female01",
#         "Bothsexes00","Male00","Female00",
#         "2015","2015capita","2014","2014capita","2013","2013capita","2012","2012capita",
#         "2011","2011capita","2010","2010capita","2009","2009capita","2008","2008capita",
#         "2007","2007capita","2006","2006capita","2005","2005capita","2004","2004capita",
#         "2003","2003capita","2002","2002capita","2001","2001capita","2000","2000capita"]
    
#     jsondata =[]
#     for i in range(len(data["Country"])):
#         newdata={}
#         for j in range(len(keys)):
#             newdata.update({keys[j] : data[keys[j]][i]})
#         jsondata.append(newdata)
      
#     return jsonify(jsondata)

# @app.route("/map")
# def mapquery():
    
#     stmt = db.session.query(Mapdata).statement
#     data = pd.read_sql_query(stmt, db.session.bind)
        
#     # Format the data to send as json
#     keys = ["Country","Bothsexes16"]
    
#     jsondata =[]
#     for i in range(len(data["Country"])):
#         newdata={}
#         for j in range(len(keys)):
#             newdata.update({keys[j] : data[keys[j]][i]})
#         jsondata.append(newdata)
#     return jsonify(jsondata)

# @app.route("/country")
# def namequery():

#     stmt = db.session.query(Metadata).statement
#     data = pd.read_sql_query(stmt, db.session.bind)
#     countries = data["Country"]
#     return jsonify(list(countries))



if __name__ == "__main__":
    app.run()




