# Norman Police Department - project0 - Text Analysis 2020
import urllib.request
import tempfile
import PyPDF2
import sqlite3
import re

def fetchincidents(url):
   # url = ("http://normanpd.normanok.gov/filebrowser_download/657/2020-02-21%20Daily%20Incident%20Summary.pdf")
    data = urllib.request.urlopen(url).read()
    return data


def extractincidents(data):
    fp = tempfile.TemporaryFile()
    result=[]
    fp.write(data)
    fp.seek(0)
    pdfReader = PyPDF2.pdf.PdfFileReader(fp)
    pdfReader.getNumPages()
    for page in range(0,pdfReader.getNumPages()):
        pages =pdfReader.getPage(page).extractText()
        pages = re.sub(r"\s\n", " ", pages)
        pagges = pages.split("\n")
        if page ==0:
            result+=pagges[5:-3]
        else:
            result+=pagges[:-1]
    result=result[:-1]
    lists = []
    i = 0
    while (i+5 < len(result)):
        if (result[i+5]):
            lists.append(result[i:i+5])
            i += 5
        else:
            lists.append([result[i], result[i+1], result[i+2]+" "+result[i+3],result[i+4], result[i+5]])
            i += 6
    #print(lists)
    return lists
def createdb():
    con= sqlite3.connect("normanpd.db")
    c = con.cursor()
    c.execute("DROP TABLE IF EXISTS incidents")

    #create table
    c.execute('''CREATE TABLE IF NOT EXISTS incidents(
           incident_time TEXT,
           incident_number TEXT,
           incident_location TEXT,
           nature TEXT,
           incident_ori TEXT)''')
       # Save (commit) the changes
    con.commit()
        # We can also close the connection if we are done with it
    con.close()
    return
def populatedb(db,incidents):

    con = sqlite3.connect('normanpd.db')
    c = con.cursor()
    for row in range(len(incidents)):
        d=c.execute("INSERT INTO incidents VALUES (?,?,?,?,?);", incidents[row])
        #print(d)
        con.commit()

    c.close()
    con.close()
    #print(incidents)
def status(db):
    con = sqlite3.connect('normanpd.db')
    c = con.cursor()
    #r=c.execute('SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY nature asc ').fetchall()
    #r=c.fetchall()

    #print(r)
    for r in c.execute('SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY nature asc ').fetchall():
        print(*r,sep="|")
    #print(d)
   # return d

    con.close()
