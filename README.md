# HAFT (Human Assisted Framework For Topic Modelling of Research Papers)
This is a Topic Modeling tool developed as  a part of my Masters thesis at University of L'Aquila, Italy and Amrita University, India

## Required packages
The tool is built using Python 2.7 and it depends on the following packages for it to run :

nltk(complete installation) , itertools, numpy, Scipy, gesim, wordcloud, unicodedata, random, beautiful soup, Tkinter and ttk

## Instructions to use the tool
* Once you have the above installed, make sure that all the python files are kept in the same folder
* Type python gui.py from the folder where this files are kept
* The above will open the gui of the tool
* The tool provides two ways to perform topic modeling, one is for an entire conference and another is for each induvidual        abstract in the conference
* The file to be used can be selected using the Open file button which allows to select .csv file which is the file formated accepted by the tool
* Make sure that the delimitter used to separate the columns in csv is a semi-colon (;) as that is the format for which the tool has been written. This change can be done from a normal comma separated file by opening it in MS Excel or Libre office and the delimitter character can be changed while saving the file
* The index of the coumn containing the title has to be given in the third field similarly the index containing the abstract has to given in the fourth filed. Please note that the index stars from 0.
* Now select which option is needed, whether the tool needs to model the topics for the whole conference (select the whole conference option) or for induvidual abstract (select the Induvidual abstract option)
* Press the Get Topics button to see the output. In the case of Induvidual abstract option the output will be displayed as a csv file with a column for topics and columns with topic names denoting the count of the topic in each abstract and in the case of whole conference option, a word cloud showing the importance of different topics will be displayed.
* The important part of the tool is the first field Enter the keywords and last field Enter the words to be removed. Both of this allows the user to add as well as remove topics froim the output. This shall be used by an expert so that the dictionary of the tool keeps improving
