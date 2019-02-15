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
    #print(symbol_obj)
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
        try:
            #textbid.insert(INSERT,bids[i]['price']+"\n")
            #textbid.insert(INSERT,bids[i]['timestamp']+" "+bids[i]['amount']+" "+bids[i]['price']+"\n")
            textbid.insert(INSERT,"\t\t"+bids[i]['amount']+"\t\t"+bids[i]['price']+"\n")
        except IndexError:
            textask.insert(INSERT,"\t\t"+"N/A"+"\t\t"+"\n")
        i += 1
    textbid.config(state=DISABLED)

    i = 0
    asks = []
    #print("ASKs -------------------------")
    for x in current_book['asks']:
        asks.append(x)
    while i < 15:     #only want 15 levels here
        try:
            textask.insert(INSERT,"\t\t"+asks[i]['amount']+"\t\t"+asks[i]['price']+"\n")
        except IndexError:
            textask.insert(INSERT,"\t\t"+"N/A"+"\t\t"+"\n")
        i += 1
    textask.config(state=DISABLED)
    
    global old_value
    spread = float(asks[0]['price']) - float(bids[-1]['price'])
    arrow = check_updown(spread, old_value)
    spread_val = arrow + " Spread: " + str(spread)
    try:
        textspread.insert(INSERT, spread_val)
    except:
        textspread.insert(INSERT, "N/A")
    textspread.config(state=DISABLED)
    texttime.config(state=DISABLED)
    old_value = spread
    #print(spread)
    #getTrades()

def getAllBooks(list):
    x = pairs_choice.get()
    url = get_book + x
    r = (http.request('GET',url).data.decode('utf-8'))
    symbol_obj = json.loads(r)
    return symbol_obj

def autoGetBook():
    getMarketData()
    getTrades()
    time.sleep(5)

def getTrades():
    i=0
    texttrades.config(state=NORMAL)
    texttradeamount.config(state=NORMAL)
    texttrades.delete(1.0,END)
    texttradeamount.delete(1.0,END)
    base_url = "https://api.gemini.com/v1/trades/"
    x = pairs_choice.get()
    t_rades = http.request('GET', base_url + x)
    trades = t_rades.data.decode('utf=8')
    trades_obj = json.loads(trades)
    trades_t = tuple(trades_obj)
    #print(trades_t)
    try:
        while i < len(trades_t) - 20 :    # removing 20 execution prints to fit nicely in window.
            texttradeamount.insert(INSERT, trades_t[i]['type'][0:1].upper()+' '+trades_t[i]['amount']+'\n')
            texttrades.insert(INSERT, ' '+trades_t[i]['price']+'\n')
            i += 1
    except:
        texttrades.insert(INSERT, "\t\t"+"N/A"+"\t\t"+"\n")
    texttrades.config(state=DISABLED)
    texttradeamount.config(state=DISABLED)

if __name__=='__main__':
    base_url = "https://api.gemini.com/v1/symbols"
    r_symbols = http.request('GET', base_url)
    pairs = r_symbols.data.decode('utf-8')
    symbol_obj = json.loads(pairs)
    symbol_obj = [x.upper() for x in symbol_obj]
    pairs_t = tuple(symbol_obj)
    choice = 0
    
    master = Tk()
    master.title("Gemini Order Book")
    master.configure(bg='black',borderwidth = 0, relief = FLAT, highlightcolor='black')
    master.resizable(0, 0)
    cFrame = Frame(master)
    cFrame.grid(row=0, column=0)
    pairs_choice = Spinbox(cFrame, width=10, state="readonly", values=pairs_t)
    refresh = Button(cFrame, text="Refresh", width=8, background = 'black', command=lambda:[getMarketData(),getTrades()])
    textspread=Text(master, width=30, height=1, background='black',foreground='white')
    texttime=Text(master, width=30, height=1, background ='black', foreground='white')
    textbid=Text(master, width=60, height=15, highlightthickness=0, borderwidth = 0, background ='black', foreground='green')
    textask=Text(master, width=60, height=15, highlightthickness=0, borderwidth = 0, background ='black', foreground='red')
    texttrades=Text(master, width=15, height=20, highlightthickness=0, borderwidth = 0, background = 'black', foreground='white')
    texttradeamount=Text(master, width=15, height=20, highlightthickness=0, borderwidth = 0, background = 'black', foreground='cyan')
    checkbutton_autorefresh=Checkbutton(master, variable=choice, text="Enable AR")

    pairs_choice.grid(row=0, columnspan=1, rowspan=1)
    refresh.grid(row=0, column=1)

    texttime.grid(row=2)
    textbid.grid(row=3)
    textspread.grid(row=4, sticky=N)
    textask.grid(row=5, sticky=N)
    texttradeamount.grid(row=3, rowspan=3, column=2, sticky=N+S+W)
    texttrades.grid(row=3, rowspan=3, column=3, sticky=N+S+W)
    checkbutton_autorefresh.grid(row=0, column=3, sticky=E)
    
    #t = Timer(5.0, autoGetBook) 
    #t.start()
    getMarketData()
    getTrades()
    master.mainloop()
    
