import csv
import nltk.data
import unicodedata
import itertools
import scipy
import random
import logging, gensim, bz2
import numpy as np
import matplotlib.pyplot as plt
from gensim import corpora, models, similarities
from numpy import linalg
from nltk.corpus import stopwords
from nltk.collocations import *
from nltk.stem.porter import PorterStemmer
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
from collections import defaultdict
from wordcloud import WordCloud, STOPWORDS
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

def main(strings,fname,abstractCol,titleCol):
	f=open(fname,'ra')
	csv_f=csv.reader(f,delimiter=';')
	documents=[]
	count=0
	target=open("output.txt","w")
	actual_text=""
	documents=[]
	abstractCol=int(abstractCol)
	titleCol=int(titleCol)
	for row in csv_f:
		if(count > 9):
			break;
		if(count > 0):
			#3ctual_text=actual_text + row[8] + row[2]
			# Each abstract is taken as a document
			documents.append(row[abstractCol] + row[titleCol])	
		count=count+1
	#print actual_text
#	example=BeautifulSoup(actual_text,from_encoding="utf-8")
#	example=actual_text
#	s = example.get_text()
	print documents
	for document in documents:
		print document
		document.lower()

	stoplist = set('new not when to be tobe while model using for a of or the and to in the introduce the we that this is more these are on architecture an architectures level as different factors from factor also be software it code by into can which made we how We need cost with The on the of such ) ( in different system In has between model, .'.split())
	lis1=[]
	texts=[[]]
	word=" "
	word_strings=" "
	strings=["formal models","component model","decision-making process","architectural decisions","interface automata","reconfigurable applications","design decisions","wireless sensor networks","software metrics","software components","model driven design", "architectural design process","influence factors","","organizational factors","collective intelligence","architecture viewpoint","architecture framework","hybrid applications","reflective components","refrative components"]
	for document in documents:
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
			
	dictionary = corpora.Dictionary(texts)
	dictionary.save('/tmp/abstracts.dict') 
	corpus = [dictionary.doc2bow(text) for text in texts]
	corpora.MmCorpus.serialize('/tmp/abstracts.mm', corpus)
	corpus = corpora.MmCorpus('/tmp/abstracts.mm')
	tfidf = models.TfidfModel(corpus)


	corpus_tfidf = tfidf[corpus]



	counts={}
	lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, update_every=0, passes=100)
	topics=lda.show_topics(num_topics=10, num_words=3, log=False, formatted=True)

	docTopicProbMat = lda[corpus]
	numpy_matrix = gensim.matutils.corpus2dense(docTopicProbMat,2*len(docTopicProbMat))
	print 'matrix'
	print numpy_matrix
	U, s, Vh = linalg.svd(numpy_matrix)

	print 'The descending order values'
	print s

	#print ' The row values'
	#print U

	final_topics=""
	target.write('Topics : ')
	set_vals=[]
	topic_list=[]
	curr_topic=0
	set_vals=set(set_vals)
	freqs=[]
	for i in topics:
		words=[]
		scores=[]
		score_val=[]
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
			words.append(wor)
			final_topics=final_topics + ' ' + wor
			set_vals.add(wor)
			topic_list.append(wor)
			counter=counter+1
				#target.write(str(final_topics))
				
		print final_topics
		#print 'Scores '
		for sc in final_val:
			score_val=sc.split('*')
			scores.append(float(score_val[0]))		
		#freqs=[]
		for word, score in zip(words, scores):
			freqs.append((word, score))
    	#elements = wordcloud.fit_words(freqs)
    	#wordcloud.draw(elements, "gs_topic_%d.png" % (curr_topic),
         #          width=120, height=120)
		
    	curr_topic=curr_topic+1	
			#print strings
	# Below code generates the Word Cloud
	wc = WordCloud(max_words=20,margin=10,
               color_func=grey_color_func, random_state=3)
# from_freqencies ignores "stopwords" so we have to do it ourselves
	wc.generate_from_frequencies(freqs)
	plt.imshow(wc)
	wc.to_file("%s.png" % (fname))
	plt.axis("off")
	plt.show()		
	list_vals=list(set_vals)
	print 'Final List'
	print list_vals
	for i in list_vals:
		target.write(str(i)+' ')

