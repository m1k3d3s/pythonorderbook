#!/usr/bin/python

import urllib3
import json
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
    #tk=Tk()
import urllib3.contrib.pyopenssl
import certifi
import collections
import time
import re
import time
from threading import *


http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
urllib3.contrib.pyopenssl.inject_into_urllib3()
get_book = "https://api.gemini.com/v1/book/"

def autocapitalize(event):
    crypto.set(crypto.get().upper())

def check_updown(price,old_price):
    if price > old_price:
        arrow = u"\u2191"
    elif price == old_price:
        arrow = "<->"
    else:
        arrow = u"\u2193"
    return arrow

old_value = 0

def getMarketData():
    texttime.config(state=NORMAL)
    texttime.delete(1.0,END)
    localtime = time.asctime( time.localtime(time.time()))
    texttime.insert(INSERT,localtime)
    textspread.config(state=NORMAL)
    textbid.config(state=NORMAL)
    textask.config(state=NORMAL)
    textspread.delete(1.0,END)
    textbid.delete(1.0,END)
    textask.delete(1.0,END)
    request_symbols = []
    current_book = {}
    base_url = "https://api.gemini.com/v1/symbols"
    r_symbols = http.request('GET', base_url)
    r = http.request('GET', get_book)
    request_symbols = r_symbols.data.decode('utf-8')
    symbol_obj = json.loads(request_symbols)
    print(symbol_obj)
    current_book = getAllBooks(symbol_obj)
    #print(current_book.values())
    i = 0
    bids = []
    #print("BIDs -------------------------")
    for x in current_book['bids']:
        bids.append(x)
    bids = bids[14::-1]      # reverse the bids to display bottom up
    #while i < len(bids):
    while i <= 14:    #only want 15 levels here
        #textbid.insert(INSERT,bids[i]['price']+"\n")
        #textbid.insert(INSERT,bids[i]['timestamp']+" "+bids[i]['amount']+" "+bids[i]['price']+"\n")
        textbid.insert(INSERT,"\t\t"+bids[i]['amount']+"\t\t"+bids[i]['price']+"\n")
        i += 1
    textbid.config(state=DISABLED)

    i = 0
    asks = []
    #print("ASKs -------------------------")
    for x in current_book['asks']:
        asks.append(x)
    while i < 15:     #only want 15 levels here
        textask.insert(INSERT,"\t\t"+asks[i]['amount']+"\t\t"+asks[i]['price']+"\n")
        i += 1
    textask.config(state=DISABLED)
    
    global old_value
    spread = float(asks[0]['price']) - float(bids[-1]['price'])
    arrow = check_updown(spread, old_value)
    spread_val = arrow + " Spread: " + str(spread)
    textspread.insert(INSERT, spread_val)
    textspread.config(state=DISABLED)
    texttime.config(state=DISABLED)
    old_value = spread
    #print(spread)

def getAllBooks(list):
    x = pairs_choice.get()
    url = get_book + x
    r = (http.request('GET',url).data.decode('utf-8'))
    symbol_obj = json.loads(r)
    return symbol_obj

def autoGetBook():
    getMarketData()
    time.sleep(5)

def getTrades():
    pass

if __name__=='__main__':
    base_url = "https://api.gemini.com/v1/symbols"
    r_symbols = http.request('GET', base_url)
    pairs = r_symbols.data.decode('utf-8')
    symbol_obj = json.loads(pairs)
    symbol_obj = [x.upper() for x in symbol_obj]
    pairs_t = tuple(symbol_obj)
    
    master = Tk()
    master.title("Gemini Order Book")
    master.configure(bg='black',borderwidth = 0, relief = FLAT, highlightcolor='black')
    cFrame = Frame(master)
    cFrame.grid(row=0, column=0)
    pairs_choice = Spinbox(cFrame, width=10, state="readonly", values=pairs_t)
    refresh = Button(cFrame, text="Refresh", width=8, background = 'black', command=getMarketData)
    textspread=Text(master, width=30, height=1, background='black',foreground='white')
    texttime=Text(master, width=30, height=1, background ='black', foreground='white')
    textbid=Text(master, width=60, height=15, borderwidth = 0, background ='black', foreground='green')
    textask=Text(master, width=60, height=15, borderwidth = 0, background ='black', foreground='red')
    texttrades=Text(master, width=30, height=30, borderwidth = 0, background = 'black', foreground='white')

    pairs_choice.grid(row=0, columnspan=1, rowspan=1)
    refresh.grid(row=0, column=1)

    texttime.grid(row=2)
    textbid.grid(row=3)
    textspread.grid(row=4, sticky=N)
    textask.grid(row=5, sticky=N)
    texttrades.grid(row=3, rowspan=3, column=2, sticky=N+S+W)
    
    #t = Timer(5.0, autoGetBook) 
    #t.start()
    master.mainloop()
    
