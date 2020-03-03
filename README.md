# Azadeh Gilanpour 
The Norman, Oklahoma police department regularly reports of incidents arrests and other activity.
This data is hosted on their website. This data is distributed to the public in the form of PDF files.
The website contains three types of summaries arrests, incidents, and case summaries.
In this assignment we will try to build a function that collects only the incidents.
-
#Project Description

## Directory
Below you can see the structure of the code.


[cs5293p19-project0]
        - COLLABORATORS
        - LICENCE
        - Pipfile
        - Pipfile.lock
        - README.md
        - project0/
            - __init__.py
            - main.py
            - project0.py
        - docs
        - setup.cfg
        - setup.py
        - tests/
            - test_download.py
            - test_date_times.py
        
All directory and file was created in the cloud SSH. You can use $git clone + you github url of the project repository.
Then start to make your directory such as #### project0/docs/test....While Some of them like Pipfile and Pipfile.lock need command to be created. The command for them is :
   Pipfile ==>      $pipenv --python python3
   Pipfile.lock ==> $pipenv install requests
The #### main.py is contain the main function of our codes and after we wrote our python code in project0.py we need to call them from this file. 
The #### setup.py is contain :

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

Finally the #### setup.cfg file should have at least the following text inside:
  [aliases]
  test=pytest

  [tool:pytest]
  norecursedirs = .*, CVS, _darcs, {arch}, *.egg, venv 

After making all the file and directory we need some commend to add them to our github repository:
   1. $git status      (at first time it is red before adding the files/directories to github)                    
   2. $git add filename
   3. $git status      (turn to green after adding)
   3. $git commit -m "your comment"
   4. $git push origin master

# Packages:
Following the packages were used in this projects that for having them in your SSH you need to use the ###pipenve install filename.
    
	   1:urllib.request
           2:PyPDf2
           3:sqlite3
           4:tempfile
           5:re
  
# Main Function Description
We have five function in this project that we need to commple them in the project0 and then as I said before calling from main.py file to check them.

    ##1.Download data

    The ####fetchincidents(url) use urllib.request library to grab the data which here would be incidents pdf file from Norman Police Department"http://normanpd.normanok.gov/content/daily-activity".
    Which I used the below commond as professor sugessted:

	    url = ("http://normanpd.normanok.gov/filebrowser_download/657/2020-02-21%20Daily%20Incident%20Summary.pdf")
   	    data = urllib.request.urlopen(url).read()
    
    This code help us to download a file from website. 

    ##2.Extract Data

     The ####extractincidents() we need to reads the pdf files from url and extracts the specefic data that related to incidents and stored it in a temporary file. Which I used tempfile package for this part.Each incident file was  includes a date_time, incident number, incident location, nature, and incident ori.
     To extract the data from the pdf files, the best way is  using the PyPdf2 package and read the pdf file withpdfFileReader() and getNumPages with both  will allow us to extract pages and pdf file and search for the rows.Extract each row and add it to a list. Below it is the example of code that I used it :
         
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

 After getting the PDF file the first step is to make loop throught the pdf and get all the pages which I make loop and used getPage(page).extractText() to extraxct all the text from the pdf.
 Then we need to remove unncecery stuff from the pdf such as hedaer/footer/multiple line/number of the page ..... So for get ride of this problems I used re.sub and spilit method.  Finally we need to make it as a list of row  which make it easier for our next step to insert these data in to the databsae.And also again here I checked that most of the multiple line is in the location part so for making all to gether and having list of 5 for each of them I wrote the while loop to take of this issue. As you see blow I tried to read if there is not any multiple line put them all in the one list if it is (as I said before because they happend in the location) add them thoes to part together and put all of them in the list. 

             i = 0
	     while (i+5 < len(result)):
   		 if ( result[i+5])):
                     lists.append(result[i:i+5])
                       i += 5
                else:
                     lists.append([result[i], result[i+1], result[i+2]+" "+result[i+3],result[i+4], result[i+5]])
                      i += 6

   ##3.Create Dataase

    The ####createdb()function help us to creates an database table which sqlite package  which we called it as "normanpd.db" here and inserts a below schema in our table:
    
		CREATE TABLE incidents (
   		 incident_time TEXT,
   		 incident_number TEXT,
   		 incident_location TEXT,
   		 nature TEXT,
   		 incident_ori TEXT
			)	;
   I used sqlite3.connect to create a connection to our database table.Then cursor's execute() method to create a incidents table anf finally commit to save it. Each time we made a connection we need to close it after we are done witgh it.

    ##4. Insert Data

    The ####populatedb(db, incidents) function use the list of rows we created in the extractincidents() function and add them  to  our data base which is here is the " normanpd.db" database.Here also we need to make a connection to our database with sqlite commend and use curser's exexute method like pervious to insert our data in the table.
	
    ##4.Print Status

   The ####status(db) function  is our last function that prints the finall result we want. Here we want  a list of the nature of incidents and the number of times they have occured. The list should be sorted alphabetically by the nature. Also need to separeated with the "|"  which I used the print with the star and sep="|".


## Test 

In this part we have to create our own test file to check each function to check that they are working as the project expected or not.I checked all 5 function in the test_download.py file. I install pytest with the #####pip install pytest because pipenv install pytest dosen't work for me.Finally after writig all the test functiona the test should be run by using one of the below method which in my case the first one didn't work till I add the __init__.py to my test directory(https://stackoverflow.com/questions/49028611/pytest-cannot-find-module):
            
                         1. pipenv run pytes

                         2. pipenv run python -m pyest 
   


	##1.Download Data:
 

	For this part I checked that my fetchincidents(url) function in the main is working perfectly and fetch the url or not.
        By is not None to see that data in the main file is None or not. 
                    
                         def test_download():
   				 data=project0.fetchincidents(url)
   				 assert data is not None



       ##2.Extract Data:
      
       For this part we need to know that the extractincidents() function extract the pdf file from provided url link in fetchincidents(url) function. Therefore I decided to checked that if extract it what is the number of pages of each pdf file and printing that number so I choose the assert 0 to see the result. The other thing that I checked was the length of the list I tried to extracted is equal to the 5 or not. Because the Incidents dataset has 5 attibute.    
    	 


       ##3.createdb():
   
       For this part we are creating the database so test part I decided to check the name of the table that I created for tha database. For this part I also used assert 0 to see the result.( Because with assert 0 the test failed and we can see the print result)


       ##4.populatedb():
        
        For this part we inserting the data we fetch and extraced before in the table we created. Therefore for testing part I decided to check different query to see that all 3 others function also work correctly or not. I tried to see all the location of the incidents when the nature it is "Traffic Stop"  Again I used assert 0 to see the result.


       ##5.Status():

       For this part in the main file we print each nature and the number of time they appears in the file. For the testing part I decided to do the same and print the nature and thier number of the time to make sure all my functions works prefectly.
