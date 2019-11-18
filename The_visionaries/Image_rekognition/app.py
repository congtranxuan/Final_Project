import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, send_file, url_for, jsonify
from s3_function import list_files, download_file, upload_file
import pickle
import base64
import re
from io import StringIO
from PIL import Image
import boto3

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
BUCKET = "finalprojectawsrekognition"   

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/registration")
def registration():
    return render_template("registration.html")


# @app.route("/storage")
# def storage():
#     contents = list_files(BUCKET)
#     return render_template('index.html', contents=contents)

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        imgstring = request.form['imgtext']
        text = request.form['imp']
        print(text)
        imgstring = re.sub('^data:image/.+;base64,', '', imgstring)
        imgdata = base64.b64decode(imgstring)
        with open('imageforrecognition.jpg', 'wb') as f:
            f.write(imgdata)

        f.filename = 'imageforrecognition.jpg'
        upload_file(f"{f.filename}","usersuploadimages")
        return redirect("/")

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)
        return send_file(output, as_attachment=True)

@app.route("/face_compare")
def face_compare():
    KEY_BUCKET = "finalprojectawsrekognition"
    KEY_SOURCE = "jessica1.jpeg"
    KEY_TARGET = "jessica2.jpg"

    def compare_faces(bucket, key, bucket_target, key_target, threshold=90):
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
    return jsonify(source_face)    

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
# db = SQLAlchemy(app)

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)

# # Save references to each table
# Samples_Metadata = Base.classes.sample_metadata
# Samples = Base.classes.samples


# @app.route("/")
# def index():
#     """Return the homepage."""
#     return render_template("index.html")


# @app.route("/names")
# def names():
#     """Return a list of sample names."""

#     # Use Pandas to perform the sql query
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Return a list of the column names (sample names)
#     return jsonify(list(df.columns)[2:])


# @app.route("/metadata/<sample>")
# def sample_metadata(sample):
#     """Return the MetaData for a given sample."""
#     sel = [
#         Samples_Metadata.sample,
#         Samples_Metadata.ETHNICITY,
#         Samples_Metadata.GENDER,
#         Samples_Metadata.AGE,
#         Samples_Metadata.LOCATION,
#         Samples_Metadata.BBTYPE,
#         Samples_Metadata.WFREQ,
#     ]

#     results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

#     # Create a dictionary entry for each row of metadata information
#     sample_metadata = {}
#     for result in results:
#         sample_metadata["sample"] = result[0]
#         sample_metadata["ETHNICITY"] = result[1]
#         sample_metadata["GENDER"] = result[2]
#         sample_metadata["AGE"] = result[3]
#         sample_metadata["LOCATION"] = result[4]
#         sample_metadata["BBTYPE"] = result[5]
#         sample_metadata["WFREQ"] = result[6]

#     print(sample_metadata)
#     return jsonify(sample_metadata)


# @app.route("/samples/<sample>")
# def samples(sample):
#     """Return `otu_ids`, `otu_labels`,and `sample_values`."""
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Filter the data based on the sample number and
#     # only keep rows with values above 1
#     sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]

#     # Sort by sample
#     sample_data.sort_values(by=sample, ascending=False, inplace=True)

#     # Format the data to send as json
#     data = {
#         "otu_ids": sample_data.otu_id.values.tolist(),
#         "sample_values": sample_data[sample].values.tolist(),
#         "otu_labels": sample_data.otu_label.tolist(),
#     }
#     return jsonify(data)

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
        
# #     # Format the data to send as json
# #     keys = ["Country","Bothsexes16"]
    
# #     jsondata =[]
# #     for i in range(len(data["Country"])):
# #         newdata={}
# #         for j in range(len(keys)):
# #             newdata.update({keys[j] : data[keys[j]][i]})
# #         jsondata.append(newdata)
# #     return jsonify(jsondata)

# # @app.route("/country")
# # def namequery():

# #     stmt = db.session.query(Metadata).statement
# #     data = pd.read_sql_query(stmt, db.session.bind)
# #     countries = data["Country"]
# #     return jsonify(list(countries))


# @app.route("/names")
# def names():
#     """Return a list of sample names."""

#     # Use Pandas to perform the sql query
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Return a list of the column names (sample names)
#     return jsonify(list(df.columns)[2:])


# @app.route("/metadata/<sample>")
# def sample_metadata(sample):
#     """Return the MetaData for a given sample."""
#     sel = [
#         Samples_Metadata.sample,
#         Samples_Metadata.ETHNICITY,
#         Samples_Metadata.GENDER,
#         Samples_Metadata.AGE,
#         Samples_Metadata.LOCATION,
#         Samples_Metadata.BBTYPE,
#         Samples_Metadata.WFREQ,
#     ]

#     results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

#     # Create a dictionary entry for each row of metadata information
#     sample_metadata = {}
#     for result in results:
#         sample_metadata["sample"] = result[0]
#         sample_metadata["ETHNICITY"] = result[1]
#         sample_metadata["GENDER"] = result[2]
#         sample_metadata["AGE"] = result[3]
#         sample_metadata["LOCATION"] = result[4]
#         sample_metadata["BBTYPE"] = result[5]
#         sample_metadata["WFREQ"] = result[6]

#     print(sample_metadata)
#     return jsonify(sample_metadata)


# @app.route("/samples/<sample>")
# def samples(sample):
#     """Return `otu_ids`, `otu_labels`,and `sample_values`."""
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Filter the data based on the sample number and
#     # only keep rows with values above 1
#     sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]

#     # Sort by sample
#     sample_data.sort_values(by=sample, ascending=False, inplace=True)

#     # Format the data to send as json
#     data = {
#         "otu_ids": sample_data.otu_id.values.tolist(),
#         "sample_values": sample_data[sample].values.tolist(),
#         "otu_labels": sample_data.otu_label.tolist(),
#     }
#     return jsonify(data)


if __name__ == "__main__":
    app.run()




