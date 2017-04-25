from flask import Flask, render_template,request
from  flask_bootstrap import Bootstrap
import templates
from flask import Blueprint
from flask_paginate import Pagination
# from flask_pagination import paginate

app = Flask(__name__)
Bootstrap(app)
global globalinputstring
global globallist
# from app import view
# http://0.gravatar.com/avatar/81b58502541f9445253f30497e53c280?s=50&d=identicon&r=G
# '''so by default this makes the user logged in as none.
# However if the user is already loggd in shows a diff webpage
# so we map both of the URLS to the same page '''

@app.route('/')
def searchword():
    return render_template("indexmodified.html")
#
# @app.route('/shopping/<myname>')
# def shopping(myname):
#     food = ["cheese", "tuna", "beef", "gcohoh"]
#     return render_template("shopping.html", food=food,myname=myname)

# @app.route('/sample/<input_str>')
# @app.route('/sample/<input_str>/<pgnumber>')
@app.route('/sample/<pgnumber>',methods=['POST'])
# @app.route('/sample/<pgnumber>')
def sample(pgnumber="pg1"):
    # if request.method == "POST":
    text = request.form['textReceived']
    input_str = text
    global globalinputstring
    globalinputstring = input_str
    print(globalinputstring)
    if globalinputstring=="apple":
        global globallist
        globallist=["aaaaaaaaaapple" ,"apple2", "appl3", "apple4", "apple" ,"apple2", "appl3", "apple4","apple" ,"apple2", "appl3", "apple4","apple" ,"apple2", "appl3", "apple4", "apple" ,"apple2", "appl3", "apple4","apple" ,"apple2", "appl3", "apple4","monkey", "monh2", "monkey3", "sasas4","monkey", "monh2", "monkey3", "sasas4" ]
    else:
        global globallist
        globallist= ["monkey", "monh2", "monkey3", "sasas4","monkey", "monh2", "monkey3", "sasas4","monkey", "monh2", "monkey3", "sasas4","monkey", "monh2", "monkey3", "sasas4","monkey", "monh2", "monkey3", "sasas4","monkey", "monh2", "monkey3", "sasas4"]
    print(pgnumber)
    pgNo = pgnumber[-1:]
    if(pgNo=="1"):
        prevlink="#"
    else:
        prevlink = "pg"+str(int(pgNo)-1)
    nextlink="pg"+str(int(pgNo)+1)
    # food = ["cheese", "tuna", "beef", "gcohoh"]
    return render_template("dummy2.html", globallist=globallist,pgnumber=pgnumber,prevlink=prevlink,nextlink=nextlink)

@app.route('/sample/<pgnumber>')
def pagesredirected(pgnumber):
    print(pgnumber)
    pgNo = pgnumber[-1:]
    if (pgNo == "1"):
        prevlink = "#"
    else:
        prevlink = "pg" + str(int(pgNo) - 1)
    nextlink = "pg" + str(int(pgNo) + 1)
    global globallist
    return render_template("dummy2.html", globalinputstring=globalinputstring, globallist=globallist, pgnumber=pgnumber, prevlink=prevlink, nextlink=nextlink)

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['textReceived']
    processed_text = text.upper()
    return processed_text

@app.route('/bootstrap')
def bootstrap():
    return render_template('indexnew.html')

#
# @app.route("/profile/<name>")
# def profile(name):
#     return render_template("profile.html",name= name)

if __name__ == '__main__':
    app.run()
