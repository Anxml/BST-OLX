import random,string,os
from flask import *
import time
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
        usrdata_file = open('sdb/userdata.json',encoding='utf-8')
        oneusrdta = usrdata_file.read().split(':')
        for usrdta in oneusrdta:
            eachdatafield = usrdta.split(',')
            users.users_details[eachdatafield[0]]=[eachdatafield[1],eachdatafield[2]]
        usrdata_file.close()
    #saves username data to userdata.txt
    def save_usrdata(self,usrnm,dispname,pswd):
        usrdata_file = open('sdb/userdata.json','a',encoding='utf-8')
        usrdata_file.write(':%s,%s,%s'%(usrnm,dispname,pswd))
        usrdata_file.close()
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
                #username is checked in total logged in user by using cookies,1 is used as it is the second in a list
                return username
        else:
            lgusertoken = 0
            #if lgusertoken is 0 gives a login button
        return lgusertoken
#
#Listing Manager
#
class list_mgr():
    user_lists = {
        'qwer':['dQw4w9WgXcQ']
    }
    lists_data = {
        'dQw4w9WgXcQ':['My Test Advertisement','6,980.00','Some Feature','Some Specs','43rd Street,\nMain Area,\nBruh City','dQw4w9WgXcQ','qwer']
    }
    thumbs = list()
    def thumb(self):
        for x in os.listdir(path='static/listthumb'):
            list_mgr.thumbs.append(x.rstrip('.jpg'))
            #list_mgr.thumbs.append((x.rstrip('.jpg'),list_mgr.lists_data[x.rstrip('.jpg')][0]))
    def create_lno(self,lnol=12):
        chars = string.digits
        genlno = str()
        for i in range(lnol):
            genlno += random.choice(chars)
        if genlno in list_mgr.lists_data:
            list_mgr.create_lno(list_mgr)
        return genlno
    def import_list_users(self):
        for usersl in users.users_details.keys():
            list_mgr.user_lists[usersl]=[]
        for ldata in list_mgr.lists_data:
            list_mgr.user_lists[list_mgr.lists_data[ldata][6]].append(list_mgr.lists_data[ldata][5])
    def save_list(self,lname,lprice,lfeature,lspecs,laddr,lno,lauth):
        usrdata_file = open('sdb/ldata.json','a',encoding='utf-16-le')
        usrdata_file.write('Ⅱ%sⅠ%sⅠ%sⅠ%sⅠ%sⅠ%sⅠ%s'%(lname,lprice,lfeature,lspecs,laddr,lno,lauth))
        usrdata_file.close
    def import_list(self):
        list_data = open('sdb/ldata.json',encoding='utf-16-le')
        onelistdata = list_data.read().split('Ⅱ')
        for eachitem in onelistdata:
            eachdatafield = eachitem.split('Ⅰ')
            list_mgr.lists_data[eachdatafield[5]]=[eachdatafield[0],eachdatafield[1],eachdatafield[2],eachdatafield[3],eachdatafield[4],eachdatafield[5],eachdatafield[6]]        
        list_data.close()
#
#Chat Functionality
#
class chats():
    chats_list = {
        '11012':[('qwer','anmol'),[('qwer','anmol'),('qwer','hello guyy'),('anmol','Hii')]]
    }
    chats_per_user = {
        'qwer':[('anmol','11012')],
        'anmol':[('qwer','11012')]
    }
    def newchatno(cno=6):
        chars = string.digits
        chatno = str()
        for i in range(cno):
            chatno += random.choice(chars)
        if chatno in chats.chats_list:
            chats.newchatno()
        return chatno
    def importchatuser():
        for eachuser in users.users_details.keys():
            if eachuser in chats.chats_per_user:
                pass
            else:
                chats.chats_per_user[eachuser] = []
    def newchatstartfunc(chatsender,chatreciever,lno):
        contactlist = list_mgr.lists_data[lno][0]
        newchatno = chats.newchatno()
        chats.chats_list[newchatno] = [(chatsender,chatreciever),[('System','%s contacted %s for %s'%(chatsender,chatreciever,contactlist))]]
        if chatsender in chats.chats_per_user:
            chats.chats_per_user[chatsender].append((chatreciever,newchatno))
        else:
            chats.chats_per_user[chatsender] = [(chatreciever,newchatno)]

        if chatreciever in chats.chats_per_user:
            chats.chats_per_user[chatreciever].append((chatsender,newchatno))
        else:
            chats.chats_per_user[chatreciever] = [(chatsender,newchatno)]
        return newchatno