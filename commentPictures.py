#!python
# -*- coding: utf-8 -*-
##############################################################
# commentPictures.py
#	add comments to pictures for geocaching logs
#

import os
import re
import sys
import glob
import string

from Tkinter import *
from PIL import ImageTk, Image

replay = 0

if len(sys.argv) > 1:
	myDate=sys.argv[1]
	
if len(sys.argv) > 2:
	if sys.argv[2] == '-r':
		replay = 1
lImages=[]

def scanRepertoire(myDate):
	global fOut, lImages, repertoire

	(year,month,day) = myDate.split('/')
	repertoire='Robin_Photos/%s/%s_%s%s'%(year,year,month,day)
	print myDate, repertoire
	try:
		print "Scanning directory:",repertoire
		with open(repertoire + '/indexImages.txt','r+') as fIn:
			for l in fIn:
				l = l.strip()
				if l <> '':
					print "Split",l.split('|')
					(newDate,newLogId,newPicture,newComment,newDescription) = l.split('|')
					lComments[newPicture] = l
					print l
		
		lImages = glob.glob(repertoire+'/*.jpg')
		lImages = [ re.sub('\\\\','/',l) for l in lImages ]
		print "Nb images",len(lImages)
	except Exception, msg:
		list.insert(END,"No directory for date")
		print msg
		return
	if len(lImages) == 0:
		list.insert(END,"Empty directory for date")
		return
	lImages.sort()
	list.insert(END,"%d pictures"%len(lImages))
	print lComments

idemPattern = re.compile('.*"id')

nImage = 0
lComments = {}

def displayImage(n):
	global lImages
	if len(lImages) == 0:
		print "No image"
		return
	path=lImages[n]
	print path
	fPicture.delete(0,END)
	fPicture.insert(0,path)
	im = Image.open(path)
	baseheight=500.0
	hpercent=(float(baseheight)/float(im.size[1]))
	wsize=int(float(im.size[0])*float(hpercent))
	im.thumbnail((wsize,baseheight), Image.ANTIALIAS)
	img = ImageTk.PhotoImage(im)
	panel.configure(image = img)
	panel.image = img
	
def Reply(name):
	print "Reply:", name

def ChangeDate(newDate):
	global lImages,nImage
	scanRepertoire(newDate)
	nImage = 0
	ChangePicture(0)
	fDate.delete(0,END)
	fDate.insert(END,newDate)

def Quit():
	print "Saving and closing"
	try:
		Save()
	except:
		print "Problem while saving"
	root.destroy()
	
def ChangePicture(increment):
	if fComment.get() <> '':
		description = re.sub('\n','\\n',fDescription.get(1.0,END))
		resu= "%s|%s|%s|%s|%s"%( fDate.get(),fLogId.get(),fPicture.get(),fComment.get(),description)
		print resu
		list.insert(END,resu)
		lComments[fPicture.get()] = resu
	global lImages,nImage
	nImage = (nImage+len(lImages)+increment) % len(lImages)
	displayImage(nImage)
	try:
		resu = lComments[fPicture.get()]
		print "New resu:",resu,
		(newDate,newLogId,newPicture,newComment,newDescription) = resu.split('|')
		print newLogId,newComment
		fLogId.delete(0,END)
		fLogId.insert(0,newLogId)
		newDescription = re.sub('\\n','\n',newDescription)
	except:
		newComment = ''
		newDescription = ''
		print "No comment for",fPicture.get()
	fComment.delete(0,END)
	fComment.insert(0,newComment)
	fDescription.delete(1.0,END)
	fDescription.insert(END,newDescription)

def Save():
	global lComments, repertoire

	import codecs
	print "Saving in directory:", repertoire
	with codecs.open(repertoire + '/indexImages.txt','w','UTF-8') as fOut:
		for d in lComments.keys():
			print lComments[d]

			fOut.write(lComments[d]+'\n')
		print lComments.values()
	return

root = Tk()
root.geometry('930x710+50+20')
root.config(bg = 'RoyalBlue4')
root.protocol("WM_DELETE_WINDOW", Quit)

frame=Frame(root,bg = 'RoyalBlue3')
frame.grid(row=0,columnspan=5,sticky=N+W+E,padx=4,pady=4)

panel = Label(frame)

fDate = Entry(frame, bg = 'white', justify = CENTER, width=10)
fLogId = Entry(frame, bg = 'white', justify = CENTER)
fPicture = Entry(frame,bg = 'white', justify = CENTER, width=52)
fComment = Entry(frame, bg = 'white', width=40)
fDescription = Text(root, bg = 'white', width=100, height=4)

bQuit = Button(root, text = "Quit", command = Quit)
bSave = Button(root, text = "Save", command = Save)
list = Listbox(frame, bg = 'LightBlue3', width=150, fg = 'yellow', height=4)

fComment.bind("<Return>",(lambda event: ChangePicture(+1)))
root.bind("<Up>"    ,(lambda event: ChangePicture(-1)))
root.bind("<Down>"  ,(lambda event: ChangePicture(+1)))
fDate.bind("<Return>",(lambda event: ChangeDate(fDate.get())))


fDate.delete(0,END)
fDate.insert(0,"2016/10/31")
fDate.grid(row=2,column=0,sticky=W,padx=4,pady=4)
lId='9416c723-7a12-40aa-b7e0-d239b5f5a4cc'
lId='_LogUID_-____-____-____-____________'

fLogId.config(width=len(lId))
fLogId.delete(0,END)
fLogId.insert(0,lId)
fLogId.grid(row=2,column=1,sticky=W,padx=4,pady=4)
fPicture.grid(row=2,column=2,sticky=W,padx=4,pady=4)
fComment.grid(row=2,column=3,sticky=W+E,padx=4,pady=4)
fDescription.grid(row=2,columnspan=4,rowspan=2, sticky=W+E+S,padx=4,pady=4)
bSave.grid(row=2,column=4,stick=E,padx=4,pady=4)
bQuit.grid(row=3,column=4,stick=E,padx=4,pady=4)
#panel.pack(side = "bottom", fill = "both", expand = "yes")
panel.grid(row=1, columnspan=5,sticky=N,padx=4,pady=4)
#list.pack()
list.grid(row=0,columnspan=5,sticky=W+E+N,padx=4,pady=4)

ChangeDate(myDate)
displayImage(0)

root.mainloop()

