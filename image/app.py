from flask import Flask, render_template, redirect, request
from xgboost import XGBClassifier
import pandas as pd
import numpy as np
import pickle
import base64
import re
# import cStringIO
from io import StringIO
from PIL import Image

# Create an instance of Flask
app = Flask(__name__)

# Route to render index.html template using data from Mongo
@app.route("/", methods=["GET", "POST"])
def home():
    output_message = ""

    if request.method == "POST":
        imgstring = request.form["imgtext"]
        print(imgstring)
        imgstring = re.sub('^data:image/.+;base64,', '', imgstring)
        imgdata = base64.b64decode(imgstring)
        print(imgdata)
        # send to service 
        with open('static\\uploads\\uploadimg.png', 'wb') as f:
            f.write(imgdata)
    
    return render_template("index.html", message = output_message)

if __name__ == "__main__":
    app.run()
