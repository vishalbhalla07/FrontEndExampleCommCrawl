from __future__ import print_function
from flask import Flask,render_template,request
import happybase
import sys
from flask import jsonify
from nltk.corpus import stopwords
from textblob import TextBlob
from urllib.parse import unquote
import urllib
from nltk import PorterStemmer
import math
from functools import reduce
import operator
import json
from  flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
totalDocuments = 54446
global globalinputstring
global globallist
global urllistfordisplay

@app.route('/')
def searchword():
    return render_template("searchword.html")


def split_into_tokens(message):
    # message = unicode(message, 'utf8')  # convert bytes into proper unicode
    return TextBlob(message).words


def split_into_lemmas(message):
    # message = unicode(message, 'utf8').lower()
    words = TextBlob(message).words
    # for each word, take its "base form" = lemma
    return [word.lemma for word in words]

 # Stemming usually refers to a crude heuristic process that chops off the ends of words in the hope of achieving
    # this goal correctly most of the time, and often includes the removal of derivational affixes. Lemmatization
    # usually refers to doing things properly with the use of a vocabulary and morphological analysis of words,
    # normally aiming to remove inflectional endings only and to return the base or dictionary form of a word,
    # which is known as the lemma


# @app.route('/sample/<input_str>')
@app.route('/sample/<pgnumber>',methods=['POST'])
def sample(pgnumber="pg1"):
    text = request.form['textReceived']
    input_str = text
    global globalinputstring
    globalinputstring = input_str
    print(globalinputstring)
    connection = happybase.Connection(host='ec2-54-174-109-153.compute-1.amazonaws.com', port=9090)
    # Replace % xx  escapes by their single - character equivalent. Example: unquote('/%7Econnolly/')
    # yields '/~connolly/'.
    input_str = urllib.parse.unquote(input_str)
    filtered_words = [bytes(PorterStemmer().stem(word),'utf8') for word in split_into_lemmas(input_str) if
                      word not in stopwords.words('english')]

    freqTable = connection.table('FreqTable')
    posVecTable = connection.table('PosVecTable')
    urlDictTable = connection.table('UrlDictTable')
    #so here i am filtering the rows based on the ones which have the row id's as the filtered words
    freqVec = freqTable.rows(filtered_words)
    posVec = posVecTable.rows(filtered_words)
    # pagerank = pagerankTable.row()

    tempDict = {}
    tfidfDict = {}
    for key, data in freqVec:
        tl = []
        for k in data:
            #len(data) means it should be the number of docs that contain the word
            # so this implies that each value is the number of times the word is contained, and
            #  the len is ultimately how many docs cintain it
            # so column family could be same, while column name could be the document name
            tfidf = (1 + math.log(int(data[k].hex(), 16))) * math.log(totalDocuments / len(data))

            #Below is the summation part for taking sum of scors across the different terms
            #in the query for obtaining the score of each document
            if (k in tfidfDict):
                tfidfDict[k] = tfidfDict[k] + tfidf
            else:
                tfidfDict[k] = tfidf
            #appending all the docs containing the word , to t1
            tl.append(k)
            # print(key + "->" + k + "->" + str(tfidf))
        # creating a set of all the documents for every key (words in query)
        tempDict[key] = set(tl)

    # print(tfidfDict)
    #performing the intersection for the different words to obtain the documents in common
    keys = reduce(set.intersection, [tempDict[item] for item in tempDict])

    results = {}
    lsk = []
    for k in keys:
        results[k] = tfidfDict[k]
        lsk.append(k[2:])

    # sorted_tfidfDict = sorted(results.items(), key=operator.itemgetter(1))

    res = []
    # Vishal made this
    urllistfordisplay=[]
    domainList = []
    print(lsk)
    for key, data in urlDictTable.rows(lsk):
        # print(data)
        s = data[b'u:totalwords']
        x = 'f:' + key.decode("utf-8")
        # res[key] = [int(s.encode('hex'), 16),data["u:domain"],data["u:url"], results["f:"+str(key)]]
        res.append(
            {'DocId': str(key,"utf-8"), 'totalwords': int(s.hex(), 16), 'domain': str(data[b'u:domain'],"utf-8"), 'url': str(data[b'u:url'],"utf-8"),
             'tfidf': results[bytes(x,'utf8')]})
        domainList.append(data[b'u:domain'])
        global urllistfordisplay
        urllistfordisplay.append({'url': str(data[b'u:url'],"utf-8")})
    newlist = sorted(res, key=operator.itemgetter('tfidf'), reverse=True)
    dumplist=json.dumps(list(newlist))
    global globallist
    globallist=newlist
    # The following part is for the next and previous links
    pgNo = pgnumber[-1:]
    if (pgNo == "1"):
        prevlink = "#"
    else:
        prevlink = "pg" + str(int(pgNo) - 1)
    nextlink = "pg" + str(int(pgNo) + 1)
    return render_template('dummy.html',newlist=newlist,pgnumber=pgnumber,globallist=urllistfordisplay,prevlink=prevlink,nextlink=nextlink)

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
    global globalinputstring
    global urllistfordisplay
    for data in urllistfordisplay:
        print('in Extract list : ', data)
    return render_template("dummy.html", globalinputstring=globalinputstring, globallist=urllistfordisplay, pgnumber=pgnumber, prevlink=prevlink, nextlink=nextlink)

@app.route('/extractedlist/')
def extract():
    # global globallist
    global urllistfordisplay
    for data in urllistfordisplay:
        print('in Extract list : ',data)

def boolean_search():
    return ""


def topk_search():
    return ""


def consine_search():
    return ""


if __name__ == '__main__':
    app.run()
