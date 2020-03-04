from PyPDF2 import PdfFileReader
import PyPDF2
import pytest
import sqlite3
import project0
import urllib.request
from project0 import main
from project0 import project0
import tempfile
url="http://normanpd.normanok.gov/filebrowser_download/657/2020-02-27%20Daily%20Incident%20Summary.pdf"
def test_download():
    data=project0.fetchincidents(url)
    assert data is not None 
    
    #assert data ==urllib.request.urlopen(url).read()
def test_extract_num_of_pages():

   data= project0.fetchincidents(url)
   incidents = project0.extractincidents(data)
   fp = tempfile.TemporaryFile()
   fp.write(data)
   fp.seek(0)
   pdf = PdfFileReader(fp)
   d= pdf.getNumPages()
   #print(d)
   # assert 0
   assert d == 23
def test_extract_length():
    data= project0.fetchincidents(url)
    incidents = project0.extractincidents(data)
    #extractincidents(data)
    assert len(incidents[0]) == 5 

def test_createdb():
    db = project0.createdb()
    con = sqlite3.connect("normanpd.db")
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    for name in res:
         assert name[0] == 'incidents'

def test_populatedb():
    data=project0.fetchincidents(url)
    incidents = project0.extractincidents(data)
    db = project0.createdb()
    project0.populatedb(db,incidents)
    con = sqlite3.connect("normanpd.db")
    cur = con.cursor()
    cur.execute('SELECT incident_location  FROM incidents where nature="Traffic Stop";')
    row=cur.fetchall()
    
    assert row[0]== ('48TH AVE NE / E ROBINSON ST',)
  
def test_status():
    data=project0.fetchincidents(url)
    incidents = project0.extractincidents(data)
    db=project0.createdb()
    project0.populatedb(db,incidents)
    s = project0.status(db)
    with open("test.txt", "w") as file:
        d= file.write(str(s))
    print (d)
   # assert type(d) == int
    assert 0

