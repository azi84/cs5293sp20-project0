
# Azadeh Gilanpour 

The Norman, Oklahoma police department regularly reports of incidents arrests and other activity.This data is hosted on the
ir website. This data is distributed to the public in the form of PDF files.The website contains three types of summaries a
rrests, incidents, and case summaries.In this assignment we will try to build a function that collects only the incidents.

#Project Description

In this project I worked on incident pdf file from Norman Police Department and below I explain evaerything I did during this projects.


#  Github :

First I made github repository with the name of cs5293sp20-project0. This one would be use at the end of project when are done we need to push every directory and file we made in our cloud instant.
All directory and file was created in the cloud SSH can use $git clone + you github url of the project repository to get accsess to github and following code would be used after we done with project to have them in our github :
                    
   1. $git status      (at first time it is red before adding the files/directories to github)
   2. $git add filename
   3. $git status      (turn to green after adding)
   3. $git commit -m "your comment"
   4. $git push origin master

#Directory :

We need to make a blow directory in our cloud instants(ssh). 

  cs5293p19-project0/
  ├── COLLABORATORS
  ├── LICENSE
  ├── Pipfile
  ├── Pipfile.lock
  ├── README
  ├── project0
  │   ├── __init__.py
  │   └── main.py
  │   └── ...
  ├── docs
  ├── setup.cfg
  ├── setup.py
  └── tests
    ├── test_download.py
    └── test_date_times.py
    └── ..
          

Then start to make your directory such as ## project0/docs/test... with the command:
 
  mkdir "name of directory"

While for making the ##Pipfile and ##Pipfile.lock we need the other kind of command for them like :

   Pipfile ==>      $pipenv --python python3

   Pipfile.lock ==> $pipenv install requests

The ##main.py file  is contain the main function of our codes and after we wrote our python code in project0.py we need to call them from this file.
 
The ##setup.py is contain below codes which you can write into it by using Vim setup.py command :

 from setuptools import setup, find packages
  setup(
	name='project0',
	version='1.0',
	author='You Name',
	authour_email='your ou email',
	packages=find_packages(exclude=('tests', 'docs')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
        )

Finally the ##setup.cfg file should have at least the following text inside which  for writing into it we use Vim setup.cfg command:
  [aliases]
  test=pytest

  [tool:pytest]
  norecursedirs = .*, CVS, _darcs, {arch}, *.egg, venv 

#packages:

Following the packages were used in this projects that for having them in your SSH you need to use the ##pipenve install filename.
    
	   1:urllib.request
           2:PyPDf2
           3:sqlite3
           4:tempfile
           5:re
  
# Main Function Description:
We use the blow function in our main.py file as main function and when we are done with the whole projects we calling this file to run the project.The main file contain 5 function that I will explain them one by one.
import argparse

import project0

def main(url):
    # Download data
    project0.fetchincidents(url)

    # Extract Data
    incidents = project0.extractincidents()
	
    # Create Dataase
    db = project0.createdb()
	
    # Insert Data
    project0.populatedb(db, incidents)
	
    # Print Status
    project0.status(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="The arrest summary url.")
     
    args = parser.parse_args()
    if args.arrests:
        main(args.arrests)

# Project :

As I said before We have five function in this project:

    ##1.Download data

    The ##fetchincidents(url) function, here we use urllib.request library to grab the data which here would be incidents pdf file from Norman Police Department"http://normanpd.normanok.gov/content/daily-activity".
    Which I used the below commond as professor sugessted to help me to download a file from website:

     url = ("http://normanpd.normanok.gov/filebrowser_download/657/2020-02-21%20Daily%20Incident%20Summary.pdf")
     data = urllib.request.urlopen(url).read()
    
    

    ##2.Extract Data

    The ##extractincidents() function,here we need to reads the pdf files from url and extracts the specefic data that related to incidents and stored it in a temporary file. Which  tempfile package would be useful for this part.
    Each incident pdf is contain the following vriables  includes a Date/Time, Incident number, Incident location, nature, and Incident ori.
    To extract the data from the pdf files, the best way is  using the PyPdf2 package and read the pdf file with pdfFileReader(), getNumPages and getPage.extractText() which they allow us to read ecah page of pdf file and finaly extraxt the text.
    Here we need to read all the pages of the pdf so we need to have loop to go through each page.Below it is the example of code that I used it :
         
     import tempfile
     fp = tempfile.TemporaryFile()
     import PyPDF2

     # Write the pdf data to a temp file
     fp.write(data.read())

     # Set the curser of the file back to the begining
     fp.seek(0)

     # Read the PDF
     pdfReader = PyPDF2.pdf.PdfFileReader(fp)
     pdfReader.getNumPages()

     # Get all the pages
 	for page in range(0, pdfReader.getNumPages()):
 		 pages=pdfReader.getPage(page).extractText()

     After getting the all the PDF file pages we need to remove unncecery stuff from the pdf such as hedaer/footer/multiple line/number of the page ..... So for get ride of this problems I used re.sub and spilit method.  
     Then we need to make it as a list of row  which make it easier for our next step to insert these data in to the databsae.And also again here I checked that most of the multiple line is in the location part so for making
     all to gether and having list of 5 for each of them I wrote the while loop to take of this issue. As you see blow I tried to read if there is not any multiple line put them all in the one list if it is
     (as I said before because they happend in the location) add them thoes to part together and put all of them in the list.Below you can see the code I used for them 
      
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
  		 if ( result[i+5])):
                    lists.append(result[i:i+5])
                       i += 5
                else:
                     lists.append([result[i], result[i+1], result[i+2]+" "+result[i+3],result[i+4], result[i+5]])
                     i += 6



    ##3.Create Dataase

    The ##createdb() function help us to creates an database table which sqlite package  which we called it as "normanpd.db" here and inserts a below schema in our table:
    
		CREATE TABLE incidents (
   		 incident_time TEXT,
   		 incident_number TEXT,
   		 incident_location TEXT,
   		 nature TEXT,
   		 incident_ori TEXT
			)	;
   I used sqlite3.connect to create a connection to our database table.Then cursor's execute() method to create a incidents table anf finally commit to save it. Each time we made a connection we need to close it after we are done witgh it.


    ##4. Insert Data

    The ###populatedb(db, incidents) function use the list of rows we created in the extractincidents() function and add them to our data base which is here is the " normanpd.db" database.
    Here also we need to make a connection to our database with sqlite commend and use curser's exexute method like pervious to insert our data in the table.

	
    ##4.Print Status

   The ##status(db) function is our last function that prints the finall result we want. Here we want a list of the nature of incidents and the number of times they have occured. 
   The list should be sorted alphabetically by the nature. Also need to separeated with the "|"  which I used the print with the star and sep="|".


#Check the project result:

After we wrote the whole project we need to run in to make sure that it gives us all desirable output we want for this part we need the blow code that we use it in our ssh and we need to add the url to it to see the final result :
  
    pipenv run python project0/main.py --incidents <url>

## Test 

After we are done weit our real code we need to test them to see that they are work correctly or not. So in this part we have to create our own test file to check each function.I checked all 5 function in the test_download.py file.I also import folowing packages 
for this part:
       1.import project0
       2.import pytest
       3.import sqlite3
       4.import PyPDF2
       5.import tempfile
  


	##1.Download Data:
 

	For this part I checked that my fetchincidents(url) function in the main is working perfectly and fetch the url or not.
        By is not None to see that data in the main file is None or not. 
                    
              def test_download():
       		 data=project0.fetchincidents(url)
   		 assert data is not None



       ##2.Extract Data:
      
       For this part we need to know that the extractincidents() function extract the pdf file from provided url link in fetchincidents(url) function.
       Therefore I decided to checked that if extract it what is the number of pages of each pdf file and printing that number so I choose the assert 0 to see the result. 
       The other thing that I checked was the length of the list I tried to extracted is equal to the 5 or not. Because the Incidents dataset has 5 attibute.    
    	 
             def test_extract_num_of_pages():
                       data= project0.fetchincidents(url)
                       incidents = project0.extractincidents(data)
                       fp = tempfile.TemporaryFile()
                       fp.write(data)
                       fp.seek(0)
                       pdf = PdfFileReader(fp)
                       pdf.getNumPages()
                       print(pdf.getNumPages())
                        assert 0

            def test_extract_length():
                      data= project0.fetchincidents(url)
                      incidents = project0.extractincidents(data)
                      #extractincidents(data)
                      assert len(incidents[0]) == 5


       ##3.createdb():
   
       For this part we are creating the database so test part I decided to check the name of the table that I created for tha database. For this part I also used assert 0 to see the result.( Because with assert 0 the test failed and we can see the print result)

           def test_createdb():	
 		    db = project0.createdb()
		    con = sqlite3.connect("normanpd.db")
   		    cur = con.cursor()
                    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    for name in res:
                        print (name[0])
                     assert 0


       ##4.populatedb():
        
       For this part we inserting the data we fetch and extraced before in the table we created. Therefore for testing part I decided to check different query to see that all 3 others function also work correctly or not. 
       I tried to see all the location of the incidents when the nature it is "Traffic Stop"  Again I used assert 0 to see the result.
		
           def test_populatedb():
    		    data=project0.fetchincidents(url)
                    incidents = project0.extractincidents(data)
                    db = project0.createdb()
                    project0.populatedb(db,incidents)
                    con = sqlite3.connect("normanpd.db")
                    cur = con.cursor()
                    cur.execute('SELECT incident_location  FROM incidents where nature="Traffic Stop";')
                    row=cur.fetchall()
                    print(row)
                    assert 0


       ##5.Status():

       For this part in the main file we print each nature and the number of time they appears in the file. For the testing part I decided to do the same and print the nature and thier number of the time to make sure all my functions works prefectly.
    
          def test_status():
                  data=project0.fetchincidents(url)
                  incidents = project0.extractincidents(data)
                  db=project0.createdb()
                  project0.populatedb(db,incidents)
                  s = project0.status(db)
                  print(s)
                  assert 0


#Check the test result:
For checking the test result in ssh we need to install pytest first. I install pytest with the ##pip install pytest because pipenv install pytest dosen't work for me.
Finally after writig all the test functiona the test should be run by using one of the below method which in my case the first one didn't work till I add the init.py to my test directory(https://stackoverflow.com/questions/49028611/pytest-cannot-find-module):

                  1. pipenv run pytes

                  3. pipenv run python -m pyest 
