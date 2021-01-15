from flask import *
import random,string,os,socket
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_folder='static')
app.secret_key = 'pqcwwmv'
#
#Manages Sessions
#
class sesh_manager():
    user_login={}
#
#Manages User Login Data
#
class users():
    users_details={'asdf':'qwer'}
    #imports userdata from userdata.txt
    def import_usrdata(self):
        usrdata_file = open('userdata.txt')
        usrdata = usrdata_file.read().split(':')
        for x in usrdata:
            y = x.split('=')
            users.users_details[y[0]]=y[1]
        usrdata_file.close()
    #saves username data to userdata.txt
    def save_usrdata(self,usrnm,pswd):
        usrdata_file = open('userdata.txt','a')
        usrdata_file.write(':%s=%s'%(usrnm,pswd))
        usrdata_file.close
    #gives token to user to use instead of password(default length 20)
    def give_token(self,l=38):
        chars = string.digits+string.ascii_lowercase+string.ascii_uppercase
        token = str()
        for i in range(l):
            token += random.choice(chars)
        return token
    #checks if user is logged in using cookies
    def chk_usr_lg(self,u):
        if request.cookies.get('id') in sesh_manager.user_login.keys():
            lgusertoken = 1
            #if lgusertoken is 1 it gives user page link
            if u == 1:
                username = sesh_manager.user_login[request.cookies.get('id')]
                #username is checked in total logged in user by using cookies,1 is used as it is the second in a list
                return username
        else:
            lgusertoken = 0
            #if lgusertoken is 0 gives a login button
        return lgusertoken
#
#Stores Video Data
#
class v_data():
    thumbs = list()
    def thumb(self):
        v_data.thumbs = os.listdir(path='static/thumbs')
    def vid_id(self):
        chars = string.ascii_letters+string.digits
        ascir = str()
        for i in range(12):
            ascir += random.choice(chars)
        return ascir
    def vid_name(self):
            name_select = ['shocking ','real ','(gone wrong) ','fortnite ','epic ','marvel ','new skin ','vbucks ']
            ac_name = str() 
            for x in range(3):
                ac_name += random.choice(name_select)
            return ac_name
#
#Placholder for a Database
#
class db_holder():
    com_li = []#comments list        
#
#
#🌌🌌🌌🌌🌌🌌
#   S P A C E
#🌌🌌🌌🌌🌌🌌
#
v_data.thumb(v_data)
users.import_usrdata(users)
#
#Index (Home)
#
@app.route("/") 
def home():
    session.clear()
    random.shuffle(v_data.thumbs)
    al_thumbs = v_data.thumbs
    ran6 = random.randint(100000000,1000000000)
    ascir = v_data.vid_id(v_data)
    username = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    return render_template('index.html',rand = ran6,ascr = ascir,thumb= al_thumbs,token=lgusertoken,username=username)
#
#Log In Page
#
@app.route('/login/', methods = ["POST","GET"])
def login():
    username = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    if request.method == 'POST':
        name = str(request.form['name'])
        paswd = str(request.form['pass'])
        keeplogin = request.form['keeplogin'] #gets a T/F value of keeping the user logged in
        if users.users_details[name] == paswd:
            del paswd
            randID = users.give_token(users)
            while randID in sesh_manager.user_login:
                try:
                    randID = users.give_token(users)
                except randID not in sesh_manager.user_login:
                    break
            #give user a random ID
            session[randID] = name
            #save it to session
            sesh_manager.user_login[randID] = name
            #save it to db of all users currently logged in
            secure_lg_cookie = make_response(render_template('lg_success.html'))
            #this is required to make a cookie
            if keeplogin == 'True':
                print(keeplogin)
                secure_lg_cookie.set_cookie('id',randID,max_age=60*60*24*365)
            else:
                print(keeplogin)
                secure_lg_cookie.set_cookie('id',randID)
            del randID,name,keeplogin
            return secure_lg_cookie
        else:
            redirect(url_for('login'))
    return render_template('login.html',token=lgusertoken,username=username)
#
#Signup
#
@app.route('/signup/', methods = ["POST","GET"])
def signup():
    username = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    if request.method == 'POST':
        name = str(request.form['name'])
        paswd = str(request.form['pass'])
        keeplogin = request.form['keeplogin'] #gets a T/F value of keeping the user logged in
        if users.users_details[name] == paswd:
            del paswd
            randID = users.give_token(users)
            while randID in sesh_manager.user_login:
                try:
                    randID = users.give_token(users)
                except randID not in sesh_manager.user_login:
                    break
            #give user a random ID
            session[randID] = name
            #save it to session
            sesh_manager.user_login[randID] = name
            #save it to db of all users currently logged in
            secure_lg_cookie = make_response(render_template('lg_success.html'))
            #this is required to make a cookie
            if keeplogin == 'True':
                print(keeplogin)
                secure_lg_cookie.set_cookie('id',randID,max_age=60*60*24*365)
            else:
                print(keeplogin)
                secure_lg_cookie.set_cookie('id',randID)
            del randID,name,keeplogin
            return secure_lg_cookie
        else:
            redirect(url_for('login'))
    return render_template('signup.html',token=lgusertoken,username=username)
#
#Listing
#
@app.route('/list/')
def listing():
    username = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    return render_template('listing.html',token=lgusertoken,username=username)
#
#Image Page
#
@app.route('/i/<img>')
def img(img):
    username = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    imgsrc = 'thumbs/' + img
    imgna = img.rstrip('.png')
    return render_template('img.html',imgn = img,imgsrc = imgsrc,imgna = imgna,token=lgusertoken,username=username)
#
#Page for logged in users
#
@app.route('/u/',methods=['GET', 'POST'])
def lg_usr():
    username = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    if request.cookies.get('id') in sesh_manager.user_login:
        if request.method == 'POST':
            request.form['logout']
            session.pop(request.cookies.get('id'))
            sesh_manager.user_login.pop(request.cookies.get('id'))
            return redirect(url_for('home'))
        u = sesh_manager.user_login[request.cookies.get('id')]
        ran3 = random.randint(10000,100000)
        return render_template('user.html',user= u,rand = ran3,token=lgusertoken,username=username)
    else :
        return redirect(url_for('login'))
#
#Video Page
#
@app.route('/v/<vid_n>/', methods = ['POST','GET'])
def vid(vid_n):
    username = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    al_thumbs = v_data.thumbs
    if request.method == 'POST':
        comment = request.form['post-comment-box']
        db_holder.com_li.append(comment)
    return render_template('video.html',v_id= vid_n,vfile='cfv.mp4',v_name=v_data.vid_name(v_data),thumb=al_thumbs,token=lgusertoken,username=username,com_li=db_holder.com_li)

if __name__ == "__main__":
    PCNAME = socket.gethostname()
    #this gets your device name which gets your local ip addresss
    app.run(host=socket.gethostbyname(PCNAME),debug=True)