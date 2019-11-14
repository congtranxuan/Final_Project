import os

import pandas as pd
import numpy as np

from flask import Flask, jsonify, render_template

from PIL import Image
import base64
import re
import cStringIO

app = Flask(__name__)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route('/hook', methods=['POST'])
def get_image():
    image_b64 = request.values['imageBase64']
    image_data = re.sub('^data:image/.+;base64,', '', image_b64).decode('base64')
    image_PIL = Image.open(cStringIO.StringIO(image_b64))
    image_np = np.array(image_PIL)
    print ('Image received: {}'.format(image_np.shape))
    return ''

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




