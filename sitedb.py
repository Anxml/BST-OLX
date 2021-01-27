import random,string,os
from flask import *
#contains all of the variable storage and stuff for index.py
#user database with username, Display Name, password 
#
#Manages Sessions
#
class sesh_manager():
    user_login={}
#
#Manages User Login Data
#
class users():
    users_details={'asdf':['Debug User','qwer']}
    #users_details={'asdf':'qwer'}
    #imports userdata from userdata.txt
    def import_usrdata(self):
        usrdata_file = open('sdb/userdata.txt')
        oneusrdta = usrdata_file.read().split(':')
        for usrdta in oneusrdta:
            eachdatafield = usrdta.split(',')
            users.users_details[eachdatafield[0]]=[eachdatafield[1],eachdatafield[2]]
        usrdata_file.close()
    #saves username data to userdata.txt
    def save_usrdata(self,usrnm,dispname,pswd):
        usrdata_file = open('sdb/userdata.txt','a')
        usrdata_file.write(':%s,%s,%s'%(usrnm,dispname,pswd))
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
                userid = sesh_manager.user_login[request.cookies.get('id')]
                username = users.users_details[userid][0]
                print (username)
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
#
#Placholder for a Database
#
class db_holder():
    com_li = []#comments list
#
#Listing Manager
#
class list_mgr():
    user_lists = {
        'qwer':['dQw4w9WgXcQ']
    }
    lists_data = {
        'dQw4w9WgXcQ':['My Add','2323','Some Feature','Some Specs','43rd Street Bababooey Area  Bruh City','Screenshot (10).png','qwer']
    }
    def create_lno(self,lnol=12):
        chars = string.digits
        genlno = str()
        for i in range(lnol):
            genlno += random.choice(chars)
        return genlno
    def import_list_users(self):
        lusers = users.users_details.keys()
        for indiusers in lusers:
            list_mgr.user_lists[lusers] = []
    def import_list(self):
        pass
    def add_list(self):
        pass
    def list_id_gen(self):
        pass
