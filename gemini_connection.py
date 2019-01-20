#!/usr/bin/python

import urllib3
import json
import tkinter
from tkinter import *
import urllib3.contrib.pyopenssl
import certifi
import collections
import time
import re


http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
urllib3.contrib.pyopenssl.inject_into_urllib3()
get_book = "https://api.gemini.com/v1/book/"

def autocapitalize(event):
    crypto.set(crypto.get().upper())

def check_updown(price,old_price):
    if price > old_price:
        arrow = u"\u2191"
    elif price == old_price:
        arrow = ""
    else:
        arrow = u"\u2193"
    return arrow

old_value = 0

def getMarketData():
    localtime = time.asctime( time.localtime(time.time()))
    texttime.delete(0,30)
    texttime.insert(INSERT,localtime)
    textbid.config(state=NORMAL)
    textask.config(state=NORMAL)
    textbid.delete(1.0,END)
    textask.delete(1.0,END)
    request_symbols = []
    btc_book = {}
    base_url = "https://api.gemini.com/v1/symbols"
    r_symbols = http.request('GET', base_url)
    r = http.request('GET', get_book)
    request_symbols = r_symbols.data.decode('utf-8')
    symbol_obj = json.loads(request_symbols)

    btc_book = getAllBooks(symbol_obj)
    #print(btc_book.values())
    i = 0
    bids = []
    print("BIDs -------------------------")
    for x in btc_book['bids']:
        bids.append(x)
    while i < len(bids):
        #textbid.insert(INSERT,bids[i]['price']+"\n")
        textbid.insert(INSERT,bids[i]['timestamp']+" "+bids[i]['amount']+" "+bids[i]['price']+"\n")
        i += 1

    i = 0
    asks = []
    print("ASKs -------------------------")
    for x in btc_book['asks']:
        asks.append(x)
    while i < len(asks):
        #textask.insert(INSERT,asks[i]['price']+"\n")
        #textask.insert(INSERT,asks[i])
        textask.insert(INSERT,asks[i]['timestamp']+" "+asks[i]['amount']+" "+asks[i]['price']+"\n")
        i += 1



def getAllBooks(list):
    for x in list:
            if x == 'btcusd':
                url = get_book + x
                r = (http.request('GET',url).data.decode('utf-8'))
                symbol_obj = json.loads(r)
    return symbol_obj


top = tkinter.Tk()
crypto = StringVar()
equity = Entry(top, width=5, textvariable=crypto)
textlt=Entry(top, width=25,background='black',foreground='red')
texttime=Entry(top, width=25, background ='black', foreground='red')
refresh = Button(top, text="Refresh", command=getMarketData)
textbid=Text(top, width=60, height=60, background ='black', foreground='green')
textask=Text(top, width=60, height=60, background ='black', foreground='green')
equity.pack()
equity.bind("<KeyRelease>",autocapitalize)
textlt.pack()
texttime.pack()
refresh.pack()
textbid.pack(side=LEFT)
textask.pack(side=RIGHT)
top.mainloop()
