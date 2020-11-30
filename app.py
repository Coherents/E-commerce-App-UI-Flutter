from flask import *
from flask_login import LoginManager,current_user,login_required,login_user,logout_user,UserMixin
from collections import defaultdict
from forms import *
from flask_migrate import Migrate
from flask_sqlalchemy import *
import os
import json
import sqlite3
from PIL import Image
import cv2
import base64
import sys
import inspect
import multiprocessing as mp
from werkzeug.utils import secure_filename
from ProductInfo import getInfo
from message import gen
########
from stats import Stats
from test import func
#######
from GPT3 import gpt
from werkzeug.security import  generate_password_hash, check_password_hash
from datetime import datetime
import zipfile

def Read_File():
     with open(name,'w') as file:
             file.write()


PATH=os.getcwd()
sess={}
IGNORE=[]
sess['name']=None
sess['file']=None
with open('req.txt','r') as file:
    auth=file.read()
L={}
z={}
app=Flask(__name__)
app.config["SECRET_KEY"]='asdasd'
app.config["SQLALCHEMY_DATABASE_URI"]=auth  # psql used 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
db = SQLAlchemy(app)
login=LoginManager(app)
class Account(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=False,nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(1000),unique=False,nullable=False)
    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=password
    def __repr__(self):
        return self.username

class Category(db.Model,UserMixin):
        id=db.Column(db.Integer,primary_key=True)
        cat=db.Column(db.String(100),nullable=False,unique=False)
        ItemName=db.Column(db.String(100),unique=False,nullable=False)
        Description=db.Column(db.String(1100),unique=False,nullable=False)
        Price=db.Column(db.Integer,unique=False,nullable=False)
        ImageByte=db.Column(db.String(1100000),unique=False,nullable=False)
        def __init__(self,name,des,price,byt,usr):
                self.ItemName=name
                self.Description=des
                self.Price=price
                self.ImageByte=byt
                self.cat=usr
        def __repr__(self):
                return self.ItemName


@login.user_loader
def validate(user):
        
        return Account.query.get(int(user))
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/<name>')
@app.route('/')
@login_required
def index(name=None):
    
    if name!=None:
            return render_template('index.html',name=name,path='/') 
    else:
            return render_template('index.html',name=sess['name'],path='/')
   
        

  
@app.route("/register",methods=["GET","POST"])
def register():
	form=Register()
	if form.validate_on_submit():
		users=Account(username=form.username.data,email=form.email.data,password=generate_password_hash(form.password.data))
		session["file"]=form.file.data.filename
		try:
			print(session["file"])
		except:
			pass
		db.session.add(users)
		db.session.commit()
		return redirect (url_for("login"))
	return render_template("register.html",form=form,path='/register')
@app.route("/login",methods=["GET","POST"])
def login():
    if  current_user.is_authenticated:
        return redirect(url_for('index'))
    form=Login()
    if form.validate_on_submit():
            D=Account.query.filter_by(email=form.email.data).first()
            n=D.username
            if D:
                    if not check_password_hash(D.password,form.password.data):
                            data=False
                            sess["Email"]=form.email.data
                            login_user(D,remember=form.remember_me.data)
                            sess['name']=n
                            return redirect(url_for('index',name=sess['name'],path='/login'))
                            
            else:
                    return redirect(url_for('register'))
            
    return render_template('login.html',form=form,path='/login')
    #return render_template('login.html',form=form)

                    
@app.route('/read')
@login_required
def commercial():
    if sess['file']:
        pass
        #os.remove(sess['file'])
    
    return render_template('readData.html',List=L.keys(),D=L,enumerate=enumerate)
@app.route('/hola',methods=["GET",'POST'])
def post_route():
     data=request.form["category_text"]
     if data not in L.keys():
            L[data]=[]
            z[data]=[]
    
     print(L)
     print(data)
     return render_template('readData.html',List=L.keys(),D=L,enumerate=enumerate)


@app.route('/yolo/<name>')
def yolo(name=None):
        if name:
                return render_template('yolo.html',name=name,path='/')
        else:
                return redirect(url_for('index',path='/'))
        
@app.route('/generate',methods=['GET','POST'])
def Generate():
        if request.method=='POST':
                temp=request.form['code']
                code2=gpt(temp).strip(':')
                print(code2)
                if temp!=None:
                        return render_template('Gen.html',temp=code2,flag=True)
                else:
                        return redirect(url_for('index',name=sess['name']))
        
        return render_template('Gen.html',temp='',flag=False)

@app.route('/qwert/<name>',methods=["GET","POST"])
def fancy(name=None):
        if name:
                Item=request.form["item"]
                Des=request.form['desc']
                Price=request.form['price']
                F=request.files['image']
                L[name].append([Item,Des,Price])
                file=secure_filename(F.filename)
               
                F.save(os.path.join(os.getcwd(),file))
                
                with open(file, "rb") as img_file:
                        my_string = base64.b64encode(img_file.read()).decode('utf-8')
                        z[name].append([Item,Price,Des,name,my_string])
                #print(my_string)
                item_content=Category(name=Item,des=Des,price=Price,byt=my_string,usr=name)
                db.session.add(item_content)
                db.session.commit()
                sess['file']=file
                Makeinfo()
                return redirect(url_for('commercial',List=L.keys(),D=L,path='/read'))
        else:
                return redirect(url_for('index',path='/'))
                    

@app.route('/download',methods=["GET","POST"]) # basically takes 2mins28secs on avg.
@login_required
def download():
        if request.method=="POST":
                IGNORE=['Symbol','Series']
                g=request.files['File']
                file=secure_filename(g.filename)
                g.save(os.path.join(os.getcwd(),file))
                G=Stats(file)
                G.Load_data(IGNORE)
                
                P1=mp.Process(target=G.Getting_plots)
                P2=mp.Process(target=G.distribution)
                P3=mp.Process(target=G.Outliers)
                P4=mp.Process(target=G.Getting_description)
                P1.start()
                P2.start()
                P3.start()
                P4.start()
                P1.join()
                P2.join()
                P3.join()
                P4.join()
                
                
                ziph=zipfile.ZipFile('data.zip','w',zipfile.ZIP_DEFLATED)
                for r,d,f in os.walk('dataFiles/'):
                        for file in f:
                                ziph.write(os.path.join(r,file))
                ziph.close()
                        
                return send_file('data.zip',as_attachment=True)
                os.remove(file)
        else:
                return render_template('download.html',path='/download');
                        
                


@app.route('/statShow')
def StatShow():
        f:bool =False
        if 'dataFiles' in os.listdir(os.path.join(os.getcwd(),'static')):
                f=True
        if f:
                path1={'Mean and stdev of Third feature':'static/dataFiles/Analysis/ID3.png',
                'Distribution Plot':'static/dataFiles/Distribution/Distributionplot_3.png',
                'Outlier in 10th feature':'static/dataFiles/Outliers/box_10.png',
                'Heatmap':'static/datafiles/Heatmap.png',
                'Volume Plot':'static/dataFiles/Volume.png'}
                return render_template('Images.html',flag=f,P=path1.keys(),D=path1)
        else:
                return redirect(url_for('index',name=name))

@app.route('/analyseText',methods=["GET","POST"])
def Text():
        if request.method=="POST":
                data=request.form["text"]
                print(data)
                gen(data)
                link='static/textCloud.png'
                
                return render_template('Text.html',flag=True,link=link)
        return render_template('Text.html',flag=False)

@app.route("/logout")
def logout():
	logout_user()
	sess['name']=None
	return redirect(url_for("login",path='/login'))


        
@app.errorhandler(401)
def error1(error):
    return render_template('Auth.html')

@app.route('/build')
def Build():
        return send_file('build/app/outputs/flutter-apk/app-release.apk',as_attachment=True)


@app.route('/')

def Makeinfo():
        F_list=list()
        x=1
        for i in z.keys():
                for j in z[i]:
                        if len(j)==5:
                                j.insert(0,str(x))
                        x=x+1
                        print(j)
                        F_list.append(getInfo(j))
        print(F_list)
        with open('assets/info/info.txt','w') as f:
                json.dump(F_list,f)



if __name__=='__main__':
   app.run(debug=True,port=8000)