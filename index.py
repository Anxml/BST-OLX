from flask import *
from sitedb import *
from datetime import datetime
import random,string,os,socket

app = Flask(__name__,static_folder='static')
app.secret_key = 'pqcwwmv'        
#
#
#   S P A C E
#
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
    dispname = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    return render_template('index.html',thumb= al_thumbs,token=lgusertoken,dispname=dispname)
#
#Log In Page
#
@app.route('/login/', methods = ["POST","GET"])
def login():
    dispname = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    if request.method == 'POST':
        name = str(request.form['name'])
        paswd = str(request.form['pass'])
        keeplogin = request.form['keeplogin'] #gets a T/F value of keeping the user logged in
        if paswd == users.users_details[name][1]:
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
    return render_template('login.html',token=lgusertoken,dispname=dispname)
#
#Signup
#
@app.route('/signup/', methods = ["POST","GET"])
def signup():
    dispname = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    if request.method == 'POST':
        name = str(request.form['name'])
        dispname = str(request.form['dispname'])
        paswd = str(request.form['pass'])
        keeplogin = request.form['keeplogin'] #gets a T/F value of keeping the user logged in
        fielderr = False
        if name == '' or dispname == '' or paswd == '':
            flash ('Please fill all fields')
            fielderr = True
        elif name in users.users_details:
            flash ('User ID already exsists')
            fielderr = True
        elif fielderr == False:
            users.users_details[name]=[dispname,paswd]
            users.save_usrdata(users,name,dispname,paswd)
            print (users.users_details[name])
            flash ('Account Created Successfully')

    return render_template('signup.html',token=lgusertoken,dispname=dispname)
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
    return render_template('listing.html',token=lgusertoken,dispname=dispname,lname=lname,laddr=laddr,lspecs=lspecs,lfeature=lfeature,lprice=lprice)
#
#Image Page
#
@app.route('/i/<img>')
def img(img):
    dispname = users.chk_usr_lg(users,1)
    lgusertoken = users.chk_usr_lg(users,0)
    imgsrc = 'thumbs/' + img
    imgna = img.rstrip('.png')
    return render_template('img.html',imgn = img,imgsrc = imgsrc,imgna = imgna,token=lgusertoken,dispname=dispname)
#
#Page for logged in users
#
@app.route('/u/',methods=['GET', 'POST'])
def lg_usr():
    dispname = users.chk_usr_lg(users,1)
    username = sesh_manager.user_login[request.cookies.get('id')]
    lgusertoken = users.chk_usr_lg(users,0)
    if request.cookies.get('id') in sesh_manager.user_login:
        if request.method == 'POST':
            request.form['logout']
            sesh_manager.user_login.pop(request.cookies.get('id'))
            return redirect(url_for('home'))
        return render_template('user.html',dispname=dispname,token=lgusertoken,username=username)
    else :
        return redirect(url_for('login'))
if __name__ == "__main__":
    PCNAME = socket.gethostname()
    #this gets your device name which gets your local ip addresss
    app.run(host=socket.gethostbyname(PCNAME),debug=True)