import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, send_file, url_for, jsonify
import pickle
import base64
import re
from io import StringIO

import boto3

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

database = "database-2"
#engine = create_engine(f'postgresql://postgres:{password}@database-2.cq0ruejyag78.us-east-2.rds.amazonaws.com:5432/{database_name}')
# conn = engine.connect()

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///static/db/Team_member.db"
db = SQLAlchemy(app)

Base = automap_base()

Base.prepare(db.engine, reflect=True)

# Save references to each table
Member = Base.classes.member

UPLOAD_FOLDER = "uploads"
BUCKET = "sourceimageforrekognition"

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/face_compare") 
def compare_page():
    return render_template("face_compare.html")

@app.route("/face_analysis") 
def face_analysis():
    return render_template("face_analysis.html")    

@app.route("/add_member")
def registration():
    stmt = db.session.query(Member).statement
    contents = pd.read_sql_query(stmt, db.session.bind)
    df = pd.DataFrame(contents)
    alist = []
    for i in range(len(df["fullname"])):
        data = {}
        image_name = "https://usersuploadimages.s3.us-east-2.amazonaws.com/" + \
            df.loc[i, "fullname"] + ".jpg"
        data["imglink"] = image_name
        data["fullname"] = df.loc[i, "fullname"]
        data["email"] = df.loc[i, "email"]
        alist.append(data)
    return render_template("registration.html", contents=alist)

@app.route("/update_members", methods=['POST'])
def update_members():
    if request.method == "POST":
        imgstring = request.form['imagecode']
        fullname = request.form['fullname']
        email = request.form["email"]

        a_member = Member(fullname=fullname, email=email)
        db.session.add(a_member)
        db.session.commit()

        print("Database was updated a new member")

        imgstring = re.sub('^data:image/.+;base64,', '', imgstring)
        imgdata = base64.b64decode(imgstring)
        image_name = fullname + ".jpg"
        with open(image_name, 'wb') as f:
            f.write(imgdata)

        f.filename = image_name
        upload_file(f"{f.filename}", "usersuploadimages")
        return redirect("/registration")

@app.route("/upload_compare", methods=['POST'])
def upload_compare():
    if request.method == "POST":
        imgstring = request.form['imagecode']
        imgstring = re.sub('^data:image/.+;base64,', '', imgstring)
        imgdata = base64.b64decode(imgstring)
        with open('face_compare_image.jpg', 'wb') as f:
            f.write(imgdata)

        f.filename = 'face_compare_image.jpg'
        upload_file(f"{f.filename}","sourceimageforrekognition")
        imglink = "https://sourceimageforrekognition.s3.us-east-2.amazonaws.com/" + f.filename
        upload_imglink = [imglink]
        return render_template("face_compare.html", contents = upload_imglink, target_image = [])

@app.route("/face_comparision")
def face_compare():
    stmt = db.session.query(Member).statement
    contents = pd.read_sql_query(stmt, db.session.bind)
    df = pd.DataFrame(contents)
            

    SOURCE_BUCKET = "sourceimageforrekognition"
    TARGET_BUCKET = "usersuploadimages"
    KEY_SOURCE = "face_compare_image.jpg"
    max_confidence = 95
    target = []


    for i in range(len(df["fullname"])):
        KEY_TARGET = df.loc[i,"fullname"] + ".jpg"
        source_face, matches = compare_faces(SOURCE_BUCKET, KEY_SOURCE, TARGET_BUCKET, KEY_TARGET)
        data={}
        for match in matches:
            confidence = match['Face']['Confidence']
            print(confidence)
            if confidence > max_confidence:
                data['image'] = "https://usersuploadimages.s3.us-east-2.amazonaws.com/" + KEY_TARGET
                data['confidence'] = confidence
                print(confidence)
                target.append(data)
              
    imglink = "https://sourceimageforrekognition.s3.us-east-2.amazonaws.com/" + 'face_compare_image.jpg'
    upload_imglink = [imglink]

    return render_template("face_compare.html", contents = upload_imglink, target_image = target)

@app.route("/upload_for_analysis", methods=['POST'])
def upload_for_analysis():
    if request.method == "POST":
        imgstring = request.form['imagecode']
        imgstring = re.sub('^data:image/.+;base64,', '', imgstring)
        imgdata = base64.b64decode(imgstring)
        with open('image_for_face_analysis.jpg', 'wb') as f:
            f.write(imgdata)

        f.filename = 'image_for_face_analysis.jpg'
        upload_file(f"{f.filename}","sourceimageforrekognition")
        imglink = "https://sourceimageforrekognition.s3.us-east-2.amazonaws.com/" + f.filename
        upload_imglink = [imglink]
        return render_template("face_analysis.html", contents = upload_imglink, outcomes = [])

@app.route('/face_analyzing')
def face_analyzing():
    BUCKET = "sourceimageforrekognition"
    KEY = "image_for_face_analysis.jpg"
    FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")
    result= []
    response = detect_faces(BUCKET, KEY)
    print(response[0])
    face = response[0]
    print(face)
    confidence = face['Confidence']
    result.append(f'Face: {confidence}')
    emotions = face['Emotions']
    for emotion in emotions:
        types = emotion['Type']
        confi = emotion['Confidence']
        result.append(f'{types} : {confi}')

    quality = face['Quality']
    for i in quality:
        result.append(f'{i} : {quality[i]}')
    for j in face:
        if j not in FEATURES_BLACKLIST:
            result.append(f'{j} : {face[j]}')
	   
    filename = 'image_for_face_analysis.jpg'
    imglink = "https://sourceimageforrekognition.s3.us-east-2.amazonaws.com/" + filename
    upload_imglink = [imglink]
    return render_template('face_analysis.html', contents = upload_imglink, result = result)


def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={"ContentType": "image/jpg", 'ContentDisposition':'inline','ACL': 'public-read'})

    return response

def compare_faces(bucket, key, bucket_target, key_target, threshold=90, region="us-east-2"):
    rekognition = boto3.client("rekognition",region)
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

def detect_faces(bucket, key, attributes=['ALL'], region="us-east-2"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.detect_faces(
	    Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
	    Attributes=attributes,
	)
	return response['FaceDetails']

if __name__ == "__main__":
    app.run()
