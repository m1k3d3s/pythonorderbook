import Tkinter
from Tkinter import *
from bs4 import BeautifulSoup
import urllib2
import collections
import time
import re


def getMarketData():
    textbid.config(state=NORMAL)
    textask.config(state=NORMAL)
    textbid.delete(1.0,END)
    textask.delete(1.0,END)
    stock = equity.get()
    if stock == "":
        equity.insert(0, "PG")
        stock = "PG"
        top.title(time.asctime( time.localtime(time.time())))
    url = "http://finance.yahoo.com/q/ecn?s="+stock+"+Order+Book";
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    companyname = soup.find_all(re.compile("h2"))
    top.title(companyname[2].string) #in the list of h2 tags companyname is 3rd one
    localtime = time.asctime( time.localtime(time.time()))
    texttime.delete(0,30) #clear textfield
    texttime.insert(INSERT, localtime)
    tables = soup.findAll("table")
    try:
        table = tables[1]
    except IndexError:
        table = 'null'
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
    textbid.config(state=DISABLED)
    textask.config(state=DISABLED)

top = Tkinter.Tk()
equity = Entry(top, width=5)
texttime = Entry(top, width=25, background = 'black', foreground = 'red')
refresh = Button(top, text="Refresh", command=getMarketData)
textbid=Text(top, width=20, height=20, background ='black', foreground='green')
textask=Text(top, width=20, height=20, background ='black', foreground='green')
equity.pack()
refresh.pack()
textbid.pack(side=LEFT)
textask.pack(side=RIGHT)
top.mainloop()
