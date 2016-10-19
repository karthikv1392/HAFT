# Tool to generate topics from abstracts
# Thesis : Karthik Vaidhyanathan
# Guide : Dr. Henry Muccini  Mrs. Sandhya Harikumar
# University : University of L'Aquila, Italy and Amrita University, India
# This contains the functions to perform lda on the abstracts obtained 
import csv
import nltk.data
import unicodedata
import itertools
import scipy
import logging, gensim, bz2
import numpy as np
from gensim import corpora, models, similarities
from numpy import linalg
from nltk.collocations import *
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# This fuction prints the number of times a particular topic is presnent in a particular topic . This indicates 1 if a topic is present in a particular abstract
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def csvTopicCount(unique_topics,count):
	f=open("output.csv","rb")
	csv_f=csv.reader(f,delimiter=';',quotechar='"')
	f1=open("final_list.csv","wb+")
	writer=csv.writer(f1,delimiter=';',quoting=csv.QUOTE_NONE)
	counter=0; # This keeps a check of the counter 
	i=0;
	valueMap={}
	value=""
	unique=[]
	unique=list(unique_topics)
	unique.remove('')
	for row in csv_f:
		if(counter==9):
			break;
		if(counter>=1):
			try:
				topics=row[count].split(',');
				print topics;
			except IndexError:
				topics='null';
			for topic in unique:
				if topic in topics:
					print topic;
					valueMap[topic]=1;
				else:
					valueMap[topic]=0;
		row.append("")
		for i in valueMap:
			row.append(valueMap[i])
		writer.writerow(row)
		valueMap.clear();
		counter=counter+1;


# This function appends the unique topics obtained in seperate coloumns to get count
def writeToCsv(unique_topics):
	f=open("out.csv","ra")
	csv_f=csv.reader(f,delimiter=';')
	count=0
	fd = open("output.csv","wb+")			
	list_vals=[] # This is the list vals created to store the topics generated
	tabWriter = csv.writer(fd, delimiter=';', quoting=csv.QUOTE_NONE)
	for row in csv_f:
		if(count>=1):
			tabWriter.writerow(row)
		else:
			for topic in unique_topics:
				row.append(topic)
			tabWriter.writerow(row)
		count=count+1
	fd.close()
	print "rows"
	print 'Total number of Columns'
	fd = open("out.csv","r")	
	reader1, reader2 = itertools.tee(csv.reader(fd, delimiter=';'))
	columns = len(next(reader1))
	print columns
	len_count=columns - 1

	del reader1

    # This is to give the length of the number of columns of the rows to find the topics
	
	csvTopicCount(unique_topics,len_count)


def main(strings,fname,abstractCol,titleCol):
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	trigram_measures = nltk.collocations.TrigramAssocMeasures()
	print fname
	f=open(fname,'ra')
	abstractCol=int(abstractCol)
	titleCol=int(titleCol)
	csv_f=csv.reader(f,delimiter=';')
	documents=[]
	count=0
	target=open("output.txt","w")
	fd = open("out.csv","wb+")	
	topic_list=[]		
	list_vals=[] # This is the list vals created to store the topics generated
	tabWriter = csv.writer(fd, delimiter=';', quoting=csv.QUOTE_NONE,escapechar='\\')   # This is for writing the csv file
	listToAppend=[]  # This is the list to be appeneded after finding the unique topics as separate coloumn in csv
	target.truncate()  # This is to make sure that everytime the test file has a new value
	for row in csv_f:
		if(count==9):
			break;
		if(count>=1):
			#print '\n-----\n'.join(tokenizer.tokenize(row[4]))
			actual_text=row[abstractCol] + row[titleCol]  # To join the abstract and title
			example=BeautifulSoup(actual_text,from_encoding="utf-8")   # to remove unwanted characters
			s = example.get_text()
			documents=tokenizer.tokenize(s)
			for document in documents:
				document.lower()

			#stops = set(stopwords.words('english'))
			stoplist = set('new not when to be tobe while model using for a of or the and to in the introduce the we that this is more these are on architecture an architectures level as different factors from factor also be software it code by into can which made we how We need cost with The on the of such ) ( in different system In has between model, .'.split())
			lis1=[]
			texts=[[]]
			word=" "
			word_strings=" "
			#strings=["formal models","component model","decision-making process","architectural decisions","interface automata","reconfigurable applications","design decisions","wireless sensor networks","software metrics","software components","model driven design", "architectural design process","influence factors","","organizational factors","collective intelligence","architecture viewpoint","architecture framework","hybrid applications","reflective components","refrative components"]
			for document in documents:
				#if strings in document:
				#	word_list.append(strings)
				word_list=nltk.word_tokenize(document.lower())
				word_list = [ word for word in word_list if word not in stoplist]
				for item in strings:
					if item in document:
						word_list.append(item)
					lis_rem=item.split()
					for string in lis_rem:
						if string in word_list:
							word_list.remove(string)
				
				texts.append(word_list)
			from collections import defaultdict
			frequency = defaultdict(int)
			#print ('*****************************************************************************')
			for text in texts:
				#print text
				for token in text:
					frequency[token] += 1
			texts = [[token for token in text if frequency[token] > 1]
	        	 	for text in texts]

			from pprint import pprint   # pretty-printer
			#pprint(texts)
			dictionary = corpora.Dictionary(texts)
			dictionary.save('/tmp/abstracts.dict') # store the dictionary, for future reference
#	print(dictionary)


	#print('*****************************printing the tokens********************************************')
	#print(dictionary.token2id)

	#**************************************************************** To get the postion of a keyword from a Corups *********************************""
	#new_doc = "software"
	#new_vec = dictionary.doc2bow(new_doc.lower().split())
	#print(new_vec)

			corpus = [dictionary.doc2bow(text) for text in texts]
			corpora.MmCorpus.serialize('/tmp/abstracts.mm', corpus) # store to disk, for later use
			#print(corpus)


			corpus = corpora.MmCorpus('/tmp/abstracts.mm')
			#print(corpus)

     # To create the Tf-idf Matrix

			tfidf = models.TfidfModel(corpus)

		#	print (' ')
		#	print('********************************************Working with Tf-idf Matrix****************************************************************')

			corpus_tfidf = tfidf[corpus] # This will create the tf-idf matrix from the Corpus

	
			lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=4, update_every=0, passes=100)
			topics=lda.show_topics(num_topics=4, num_words=2, log=False, formatted=True)

			docTopicProbMat = lda[corpus]
			numpy_matrix = gensim.matutils.corpus2dense(docTopicProbMat,2*len(docTopicProbMat))
			print 'matrix'
			print numpy_matrix
			U, s, Vh = linalg.svd(numpy_matrix)

			print 'Thr descending order values'
			print s

			print ' The row values'
			print U

			final_topics=""
			target.write('Topics : ')
			set_vals=[]
			set_vals=set(set_vals)
			for i in topics:	
				counter=0 # to ensure that the formatting is done properly
				final_val=i[1].split('+')
				for wor in final_val:
					for char in wor:
						if(char.isdigit() or char=='*' or char==',' or char=='.' or char==' ' or char==''):
							wor=wor.replace(char,"")
					#final_topics is the variable to concatenate the topic and store
					if(counter==0):
						final_topics=final_topics+wor
						set_vals.add(wor)
						topic_list.append(wor)
					final_topics=final_topics + ' ' + wor
					set_vals.add(wor)
					topic_list.append(wor)
					counter=counter+1
				#target.write(str(final_topics))
				
				print final_topics
				
			#print strings
			list_vals=list(set_vals)
			print 'Final List '
			print list_vals
			#row.append(list_vals)
        	
        	topic_text="" # This is later append to the end of the csv file
        	for i in list_vals:
        		#target.write(str(i)+' ')


        		#listToAppend.append(str(i))
        		#txt=str(i).decode("utf-8","replace")
        		txt=str(i)
        		listToAppend.append(txt)
        		topic_text=topic_text + txt + ','
        	row.append(topic_text)     # This writes the topics on to a separate coloumn
        	tabWriter.writerow(row)
        	del topic_list[:]

		count=count+1
	print set(listToAppend)    # To print all the unique topics among all the abstracts
	writeToCsv(set(listToAppend))
	return
#
def caller():
	# This function keeps calling the main function in a loop by passing the list with the added item so that it can keep learning and the dictionary keeps increasing
	strings=["formal models","component model","decision-making process","architectural decisions","interface automata","reconfigurable applications","design decisions","wireless sensor networks","software metrics","software components","model driven design", "architectural design process","influence factors","","organizational factors","collective intelligence","architecture viewpoint","architecture framework","hybrid applications","reflective components","refrative components"]
	main(strings)
	
#caller() 