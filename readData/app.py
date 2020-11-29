from flask import *
from flask_login import LoginManager,current_user,login_required,login_user,logout_user,UserMixin
from collections import defaultdict
from flask_migrate import Migrate
from flask_sqlalchemy import *
import os
import sqlite3
from PIL import Image
import cv2
import base64
import sys
import inspect
import multiprocessing as mp
from werkzeug.utils import secure_filename
from werkzeug.security import  generate_password_hash, check_password_hash
from datetime import datetime
import zipfile

app=Flask(__name__)
L={}
@app.route('/read')
def commercial():
    return render_template('readData.html',List=L.keys(),D=L)
@app.route('/hola',methods=["GET",'POST'])
def post_route():
     data=request.form["category_text"]
     if data not in L.keys():
            L[data]=[]
    
     print(L)
     print(data)
     return render_template('readData.html',List=L.keys(),D=L)


@app.route('/yolo/<name>')
def yolo(name=None):
        if name:
                return render_template('yolo.html',name=name)
        else:
                return redirect(url_for('index'))

@app.route('/qwert/<name>',methods=["GET","POST"])
def fancy(name=None):
        if name:
                ## Form data
                Item=request.form["item"]
                Des=request.form['desc']
                Price=request.form['price']
                F=request.files['image']
                ## /form data
                L[name].append([Item,Des,Price])
                file=secure_filename(F.filename)
               
                F.save(os.path.join(os.getcwd(),file))
                
                with open(file, "rb") as img_file:
                        my_string = base64.b64encode(img_file.read())
                print(my_string)
                os.remove(file)
                return redirect(url_for('commercial',List=L.keys(),D=L))
        else:
                return redirect(url_for('index'))


if __name__=='__main__':
        app.run(debug=True,port=4000)

        