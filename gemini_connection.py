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
import time


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
    textspread.config(state=NORMAL)
    textbid.config(state=NORMAL)
    textask.config(state=NORMAL)
    textspread.delete(0,END)
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
    #print("BIDs -------------------------")
    for x in btc_book['bids']:
        bids.append(x)
    while i < len(bids):
        #textbid.insert(INSERT,bids[i]['price']+"\n")
        #textbid.insert(INSERT,bids[i]['timestamp']+" "+bids[i]['amount']+" "+bids[i]['price']+"\n")
        textbid.insert(INSERT,"\t\t"+bids[i]['amount']+"\t\t"+bids[i]['price']+"\n")
        i += 1

    i = 0
    asks = []
    #print("ASKs -------------------------")
    for x in btc_book['asks']:
        asks.append(x)
    while i < len(asks):
        #textask.insert(INSERT,asks[i]['price']+"\n")
        #textask.insert(INSERT,asks[i])
        #textask.insert(INSERT,asks[i]['timestamp']+" "+asks[i]['amount']+" "+asks[i]['price']+"\n")
        textask.insert(INSERT,"\t\t"+asks[i]['amount']+"\t\t"+asks[i]['price']+"\n")
        i += 1

    spread = float(asks[0]['price']) - float(bids[0]['price'])
    textspread.insert(INSERT, spread)
    #print(spread)

def getAllBooks(list):
    for x in list:
            if x == 'btcusd':
                url = get_book + x
                r = (http.request('GET',url).data.decode('utf-8'))
                symbol_obj = json.loads(r)
    return symbol_obj


if __name__=='__main__':
    top = tkinter.Tk()
    top.configure(bg='black')
    top.overrideredirect(1)
    top.title("Gemini Order Book")
    crypto = StringVar()
    mainframe = Frame(top,background='Black',borderwidth = 1, relief =SUNKEN)
    equity = Entry(top, width=5, textvariable=crypto)
    textspread=Entry(top, width=25,background='black',foreground='white')
    texttime=Entry(top, width=25, background ='black', foreground='red')
    refresh = Button(top, text="Refresh", command=getMarketData)
    textbid=Text(top, width=60, height=30, background ='black', foreground='green')
    textask=Text(top, width=60, height=30, background ='black', foreground='red')
    equity.pack()
    equity.bind("<KeyRelease>",autocapitalize)
    textspread.pack()
    texttime.pack()
    refresh.pack()
    textbid.pack(side=TOP)
    textask.pack(side=BOTTOM)
    top.mainloop()
