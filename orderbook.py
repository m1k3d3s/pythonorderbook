#!/usr/bin/python

import Tkinter
from Tkinter import *
from bs4 import BeautifulSoup
import urllib2
import collections
import time
import re

def autocapitalize(event):
    stock.set(stock.get().upper())

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
    textbid.config(state=NORMAL)
    textask.config(state=NORMAL)
    textbid.delete(1.0,END)
    textask.delete(1.0,END)
    stock = equity.get()
    if stock == "":
        equity.insert(0, "GOOG")    
        stock = "GOOG"
    url = "http://finance.yahoo.com/q/ecn?s="+stock+"+Order+Book";
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    #print(soup)
    companyname = soup.find_all(re.compile("h2"))
    top.title(companyname[2].string) #in the list of h2 tags companyname is 3rd one
    localtime = time.asctime( time.localtime(time.time()))
    textlt.delete(0,30)
    texttime.delete(0,30)
    texttime.insert(INSERT,localtime)
    tables = soup.findAll("table")
    #for i in tables:
    #    print i
    try:
        table = tables[1]
    except IndexError:
        table = 'null'
        textlt.insert(INSERT,"N/A")
        textbid.insert(INSERT,"N/A")
        textask.insert(INSERT,"N/A")
    rows = table.findAll("tr")
    for row in rows:
        tds = row.findAll('td')
        if(len(tds)==2):
            bidprice = tds[0].string
            bidsize = tds[1].string
            textbid.insert(INSERT,bidprice.strip())
            textbid.insert(INSERT,"   ")
            textbid.insert(END,bidsize.strip())
            textbid.insert(INSERT,"\n")
            textbid.focus_set()
    try:
        table_a = tables[2]
    except IndexError:
        table_a = 'null'
        textlt.insert(INSERT,"N/A")
        textbid.insert(INSERT,"N/A")
        textask.insert(INSERT,"N/A")
    rows = table_a.findAll("tr")
    for row in rows:
        tdsa = row.findAll('td')
        if(len(tdsa)==2):
            askprice = tdsa[0].string
            asksize = tdsa[1].string
            textask.insert(INSERT,askprice.strip())
            textask.insert(INSERT,"   ")
            textask.insert(END,asksize.strip())
            textask.insert(INSERT,"\n")
            textask.focus_set()
    
    try:
        table_lt = tables[3]
    except IndexError:
        table_lt = 'null'
        textlt.insert(INSERT,"N/A")
        textask.insert(INSERT,"N/A")
        textbid.insert(INSERT,"N/A")
    rows = table_lt.findAll('tr')
    for row in rows:
        ltrade = row.findAll('td', {'class':'yfi_last_trade'})
        if(not len(ltrade)==0):
            #print str(ltrade).strip('[]')
            value = row.text
            global old_value
            arrow = check_updown(value,old_value)
            textlt.insert(INSERT,value+" "+arrow)
            old_value = value
    
    textbid.config(state=DISABLED)
    textask.config(state=DISABLED)
    #<td class="yfnc_tabledata1 yfi_last_trade"><span id="yfs_l90_drys">0.10</span></td></tr>
    #lasttrade = soup.find_all(table,id="table1")
    #print lasttrade


top = Tkinter.Tk()
stock = StringVar()
equity = Entry(top, width=5, textvariable=stock)
textlt=Entry(top, width=25,background='black',foreground='red')
texttime=Entry(top, width=25, background ='black', foreground='red')
refresh = Button(top, text="Refresh", command=getMarketData)
textbid=Text(top, width=20, height=20, background ='black', foreground='green')
textask=Text(top, width=20, height=20, background ='black', foreground='green')
equity.pack()
equity.bind("<KeyRelease>",autocapitalize)
textlt.pack()
texttime.pack()
refresh.pack()
textbid.pack(side=LEFT)
textask.pack(side=RIGHT)
top.mainloop()
