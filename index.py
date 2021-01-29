from flask import *
from sitedb import *
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,TextAreaField,DecimalField,FileField
from wtforms.validators import ValidationError,DataRequired,Length
from PIL import Image
from datetime import datetime
import random,string,os,socket,locale

upload_folder = '/static/listthumb'
#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__,static_folder='static')
app.config['UPLOADED_PHOTOS_DEST'] = upload_folder
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'pqcwwmv'        
#
#
#   S P A C E
#
#
users.import_usrdata(users)
list_mgr.import_list(list_mgr)
list_mgr.import_list_users(list_mgr)
list_mgr.thumb(list_mgr)
locale.setlocale(locale.LC_ALL,'English_India')
#
#Forms
#
class SignupForm(FlaskForm):
    username = StringField(label='Enter your permanent username',validators=[DataRequired(),Length(min=3,max=15)])
    dispname = StringField(label='Enter your display name',validators=[DataRequired(),Length(min=3,max=30)])
    paswd = PasswordField(label='Password',validators=[DataRequired(),Length(min=4,max=20)])
    submit = SubmitField(label='Submit')
    def validate_username(self, username):
        excluded_chars = "*?!'^+%&/()=}][{$#Ⅱ Ⅰ,:"
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(f"Character {char} is not allowed in username.")
            if self.username.data in users.users_details:
                raise ValidationError(f"Username Already Taken")
    def validate_dispname(self, dispname):
        excluded_chars = "*?!'^+%&/()=}][{$#ⅡⅠ,"
        for char in self.dispname.data:
            if char in excluded_chars:
                raise ValidationError(f"Character {char} is not allowed in username.")
    def validate_paswd(self, paswd):
        excluded_chars = "*Ⅱ Ⅰ"
        for char in self.paswd.data:
            if char in excluded_chars:
                raise ValidationError(f"Character {char} is not allowed in username.")
class NewListingForm(FlaskForm):
    lname = StringField()
    lprice = DecimalField(places=2)
    lfeature = TextAreaField()
    lspecs = TextAreaField()
    laddr = TextAreaField()
    limg = FileField()
    lsubmit = SubmitField(label='Submit')

    
#
#Index (Home)
#
@app.route("/") 
def home():
    random.shuffle(list_mgr.thumbs)
    thumb = list_mgr.thumbs
    dispname = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    return render_template('index.html',thumb=thumb,token=lgusertoken,dispname=dispname,lname=list_mgr.lists_data)
#
#Log In Page
#
@app.route('/login/', methods = ["POST","GET"])
def login():
    dispname = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    err = str()
    if request.cookies.get('id') in sesh_manager.user_login:
        return redirect(url_for('lg_usr'))
    if request.method == 'POST':
        name = str(request.form['name'])
        paswd = str(request.form['pass'])
        keeplogin = request.form['keeplogin'] #gets a T/F value of keeping the user logged in
        if name == '':
            return redirect(url_for('login'))
        if name in users.users_details and paswd == users.users_details[name][1]:
            del paswd
            randID = users.give_token(users)
            while randID in sesh_manager.user_login:
                try:
                    randID = users.give_token(users)
                except randID not in sesh_manager.user_login:
                    break
            #give user a random ID
            sesh_manager.user_login[randID] = name
            #save it to db of all users currently logged in
            secure_lg_cookie = make_response(render_template('lg_success.html'))
            #this is required to make a cookie
            if keeplogin == 'True':
                secure_lg_cookie.set_cookie('id',randID,max_age=60*60*24*365)
            else:
                secure_lg_cookie.set_cookie('id',randID)
            del randID,name,keeplogin
            return secure_lg_cookie
        else:
            redirect(url_for('login'))
            err = 'Incorrect UserID/Password'
    return render_template('login.html',token=lgusertoken,dispname=dispname,err=err)
#
#Signup
#
@app.route('/signup/', methods = ["POST","GET"])
def signup():
    dispname = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    form = SignupForm()
    if form.validate_on_submit():
        name = form.username.data
        dispname = form.dispname.data
        paswd = form.paswd.data
        users.users_details[name]=[dispname,paswd]
        users.save_usrdata(users,name,dispname,paswd)
        return redirect(url_for('home'))
    return render_template('signup.html',token=lgusertoken,dispname=dispname,form=form)
#
#Listing
#
@app.route('/list/<lno>')
def listing(lno):
    dispname = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    lname = list_mgr.lists_data[lno][0]
    lprice = list_mgr.lists_data[lno][1]
    lfeature = list_mgr.lists_data[lno][2]
    lspecs = list_mgr.lists_data[lno][3]
    laddr = list_mgr.lists_data[lno][4]
    lauth = users.users_details[list_mgr.lists_data[lno][6]][0]
    return render_template('listing.html',token=lgusertoken,dispname=dispname,lno=lno,lname=lname,lauth=lauth,laddr=laddr,lspecs=lspecs,lfeature=lfeature,lprice=lprice)
#
#Image Page
#
@app.route('/i/<img>')
def img(img):
    dispname = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    imgsrc = 'listthumb/' + img
    imgna = img.rstrip('.jpg')
    return render_template('img.html',imgn = img,imgsrc = imgsrc,imgna = imgna,token=lgusertoken,dispname=dispname)
#
#Page for logged in users
#
@app.route('/u/',methods=['GET', 'POST'])
def lg_usr():
    dispname = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    username = sesh_manager.user_login[request.cookies.get('id')]
    if request.cookies.get('id') in sesh_manager.user_login:
        if request.method == 'POST':
            request.form['logout']
            sesh_manager.user_login.pop(request.cookies.get('id'))
            return redirect(url_for('home'))
        return render_template('user.html',dispname=dispname,token=lgusertoken,username=username)
    else :
        return redirect(url_for('login'))
#
#Create a listing
#
@app.route('/newlisting',methods=['GET','POST'])
def newlisting():
    dispname = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    if request.cookies.get('id') in sesh_manager.user_login:
        lform = NewListingForm()
        if lform.validate_on_submit():
            lno = list_mgr.create_lno(list_mgr)
            limg = lform.limg.data
            lprice = locale.currency(lform.lprice.data,symbol=False,grouping=True)
            limg.save('static/listthumb/%s.jpg'%lno)
            lauth = sesh_manager.user_login[request.cookies.get('id')]
            list_mgr.lists_data[lno] = [lform.lname.data,lprice,lform.lfeature.data,lform.lspecs.data,lform.laddr.data,lno,lauth]
            list_mgr.save_list(list_mgr,lform.lname.data,lprice,lform.lfeature.data,lform.lspecs.data,lform.laddr.data,lno,lauth)
            list_mgr.thumbs.append(lno)
            print(list_mgr.lists_data[lno])
            return redirect(url_for('lg_usr'))
        return render_template('newlisting.html',dispname=dispname,token=lgusertoken,lform=lform)
    else:
        return redirect(url_for('home'))
#
#Error Handling
#
@app.errorhandler(500)
def pnf500(e):
        return render_template('404.html'), 500

@app.errorhandler(404)
def pnf(e):
        return render_template('404.html'), 404

#
#Execution
#
if __name__ == "__main__":
    PCNAME = socket.gethostname()
    #this gets your device name which gets your local ip addresss
    app.run(host=socket.gethostbyname(PCNAME),debug=True)