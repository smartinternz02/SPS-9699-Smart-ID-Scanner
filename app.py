from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from PIL import Image
import pytesseract,os
from flask_uploads import UploadSet,configure_uploads, IMAGES
from werkzeug.utils import secure_filename


project_dir=os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,static_url_path='',
            static_folder='static',
            template_folder='templates')

photos=UploadSet('photos',IMAGES)

app.config['UPLOAD_FOLDER']='static'
app.config['MYSQL_HOST']="remotemysql.com"     
app.config['MYSQL_USER']="EcIPQXuPvx"
app.config['MYSQL_PASSWORD']="wYchCLapIq"
app.config['MYSQL_DB']="EcIPQXuPvx"
mysql=MySQL(app)


@app.route('/',methods=['GET', 'POST'])                #Home page
def index():
    return render_template('login.html')

@app.route('/login',methods =['GET', 'POST'])                #Home page
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM signup WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        if account:
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

        

   
@app.route('/signup', methods =['GET', 'POST'])         #Signup/Login
def signup():
    msg = ''
    if request.method == 'POST' :
        username = request.form.get('username')
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM signup WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO signup VALUES (NULL, % s, % s, % s)', (username, email,password))
            mysql.connection.commit()
            return render_template('/index.html', msg = msg)
        
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg)


class GetText(object):
    def __init__(self,file):
        self.file=pytesseract.image_to_string(Image.open(project_dir+'\\static\\'+file))  
        

@app.route('/index',methods =['GET', 'POST'])
def home():
     msg=''
     if request.method=='POST':
        if 'photo' not in request.files:
            return 'There is no photo in the form'
        name=request.form['img-name']+'.jpg'
        photo=request.files['photo']
        path=os.path.join(app.config['UPLOAD_FOLDER'],name)
        photo.save(path)
        
        textObject=GetText(name)
        print(textObject.file)
        msg=textObject.file
        if msg:
            return render_template('/index.html', msg = format(msg))


if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
