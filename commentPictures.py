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
	global lImages

	(year,month,day) = myDate.split('/')
	repertoire='Robin_Photos/%s/%s_%s%s'%(year,year,month,day)
	print myDate, repertoire
	global fOut, lImages
	fOut = open(repertoire + '/indexImages.txt','w')

	lImages = glob.glob(repertoire+'/*.jpg')
	print "Nb image",len(lImages)
	if len(lImages) == 0:
		return
	lImages.sort()

idemPattern = re.compile('.*"id')

nImage = 0

def displayImage(n):
	global lImages
	if len(lImages) == 0:
		print "No image"
		return
	path=lImages[n]
	print len(path), path
	picture.delete(0,END)
	picture.insert(0,path)
	im = Image.open(path)
	baseheight=500.0
	print im.size,
	hpercent=(float(baseheight)/float(im.size[1]))
	wsize=int(float(im.size[0])*float(hpercent))
	print hpercent, wsize
	im.thumbnail((wsize,baseheight), Image.ANTIALIAS)
	#im.thumbnail((400,300), Image.ANTIALIAS)
	img = ImageTk.PhotoImage(im)
	panel.configure(image = img)
	panel.image = img
	
def Reply(name):
	print "Reply:", name

def ChangeDate(newDate):
	global lImages,nImage
	scanRepertoire(newDate)
	nImage = 0
	displayImage(0)
	

	
def ChangePicture(increment):
	if comment.get() <> '':
		resu= "%s|%s|%s|%s"%( date.get(),logId.get(),comment.get(),picture.get())
		print resu
		list.insert(END,resu)
	global lImages,nImage
	nImage = (nImage+len(lImages)+increment) % len(lImages)
	displayImage(nImage)
	comment.delete(0,END)


def Insert():
	name = date.get()
	name2 = logId.get()

	list.insert(END, name)
	list.insert(END, name2)
	date.delete(0,END)	
	logId.delete(0,END)

root = Tk()
root.geometry('1000x700+50+20')

panel = Label(root)

date = Entry(root, bg = 'white')
logId = Entry(root, bg = 'white')
picture = Entry(root,bg = 'white')
picture.config(width=50)
comment = Entry(root, bg = 'white')
comment.config(width=40)
comment.bind("<Return>",(lambda event: ChangePicture(+1)))
comment.bind("<Up>"    ,(lambda event: ChangePicture(-1)))
comment.bind("<Down>"  ,(lambda event: ChangePicture(+1)))
date.bind("<Return>",(lambda event: ChangeDate(date.get())))

button = Button(root, text = "Quit", command = Insert)

f = Frame(root, width=950, bg="blue")
f.grid(row=0,columnspan=5,sticky=N)
list = Listbox(f, bg = 'darkblue', width=165, fg = 'yellow', height=5)



#date.pack(side="left")
#logId.pack(side="left")
#button.pack(side="left", padx = 4, pady = 4, anchor= E)
date.config(width=11)
date.delete(0,END)
date.insert(0,"2016/10/31")
date.grid(row=2,column=0,sticky=W)
lId='9416c723-7a12-40aa-b7e0-d239b5f5a4cc'
logId.config(width=len(lId))
logId.delete(0,END)
logId.insert(0,lId)
logId.grid(row=2,column=1,sticky=W)
picture.grid(row=2,column=2,sticky=W)
comment.grid(row=2,column=3,sticky=W+E)
button.grid(row=2,column=4,stick=E)
#panel.pack(side = "bottom", fill = "both", expand = "yes")
panel.grid(row=1, columnspan=5,sticky=N)
list.pack()
#list.grid(row=0,columnspan=4,sticky=W+E+N)

scanRepertoire(date.get())
displayImage(0)

root.mainloop()

