#!/usr/bin/python

import Tkinter
from Tkinter import *
import topic_paper
import abstract_topic
import os
import tkFileDialog 
import ttk
root = Tkinter.Tk()
root.wm_title("Topic Modeling Tool")
#frame=Frame(root)
#frame.pack()

#middleframe=Frame(root)
#middleframe.pack(side=LEFT)

#bottomframe = Frame(root)
#bottomframe.pack( side = BOTTOM )

root.geometry('600x200')

#L1 = Label(frame, text="Enter the Keywords")
#L1.pack( side = LEFT)

L1 = Label(root, text="Enter the Keywords").grid(row=0)
#L1.pack( side = LEFT)


labelTitle = Label (root,text="Mention the coloumn of title").grid(row=2)

labelAbstract = Label (root,text="Coloum of Abstract").grid(row=3)



#E1 = Entry(frame, bd =5)
#E1.pack(side = LEFT)

E1=Entry(root,bd=5)
E1.grid(row=0,column=1)

labelFile = Label(root, text="Select the file").grid(row=1)
#labelFile.pack(side=LEFT)

fileName = Entry (root, bd=5)
#fileName.pack(side=LEFT)
fileName.grid(row=1,column=1)
fname='/home/karthik'
strings=["formal models","component model","decision-making process","architectural decisions","interface automata","reconfigurable applications","design decisions","wireless sensor networks","software metrics","software components","model driven design", "architectural design process","influence factors","","organizational factors","collective intelligence","architecture viewpoint","architecture framework","hybrid applications","reflective components","refrative components"]

abstractCol=0
titleCol=0

titleRow = Entry (root,bd=5)
titleRow.grid(row=2,column=1)

abstractRow = Entry(root,bd=5)
abstractRow.grid(row=3,column=1)

labelOption = Label (root,text="Select an option").grid(row=4)
v=IntVar()
Radiobutton(root, text="Induvidual Abstract", variable=v, value=1).grid(row=4, column=1)
Radiobutton(root, text="Whole Conference", variable=v, value=2).grid(row=4, column=2)

def addKeywords():

	# This is to get the user input of the keyword list. So this will be basically stored for the future use as a dictionary
	string=E1.get()
	E1.delete(0,'end')
   	print string
   	strings.append(string)
	print strings

def openFile():
	ftypes = [('CSV files', '*.csv'), ('All files', '*')]
	dlg = tkFileDialog.Open(root, filetypes = ftypes)
	global fname
	fl = dlg.show()
	fname=fl
	fileName.insert(0,fname)

	print fname

#ButtonTopics = Tkinter.Button(frame, text ="Add more", command = addKeywords)
#ButtonTopics.pack(side=BOTTOM)

ButtonTopics = Tkinter.Button(root, text ="Add more", command = addKeywords)
ButtonTopics.grid(row=0,column=2)

ButtonOpenFile = Tkinter.Button(root,text="Open File", command = openFile)
ButtonOpenFile.grid(row=1,column=2)


def getTopics():
	abstractCol=abstractRow.get()
   	titleCol=titleRow.get()
	if(v.get()==1):
		# If the user selects to see the topics to be generated for each of the induvicual abstracts
		print fname
		topic_paper.main(strings,fname,abstractCol,titleCol)
   		#os.system("gedit output.txt")
   		os.system("libreoffice final_list.csv")
   	else:
   		abstract_topic.main(strings,fname,abstractCol,titleCol)
   		os.system("leafpad output.txt")



ButtonTopics = Tkinter.Button(root, text ="Get Topics", command = getTopics)

ButtonTopics.grid(row=5,column=1)

ttk.Separator(root,orient=HORIZONTAL).grid(row=6, columnspan=8, sticky="ew")
root.mainloop()