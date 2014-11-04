#!/usr/bin/python
# coding=utf-8
# filename: commentsParser.py
##################################
# @author yinxj
# @date 2013-03-13
import sys, optparse, re

def parseComments(fileName):
	f=open(fileName)
	content=f.read()
	f.close()
	return parseCommentsFromContent(content)
	
def parseCommentsFromContent(content):
	# "
	doubleQuoteStarted=False
	# /* ... */
	starCommentStarted=False

	# get comments position
	commentsPos=[]
	length=len(content)
	i=-1
	while True:
		i=i+1
		if i>=length:
			break
		c=content[i]
		if c=='"':
			# escape
			if i>1 and content[i-1]=='\\':
				continue
			if starCommentStarted:
				continue
			doubleQuoteStarted=not doubleQuoteStarted
		if c=='/':
			if doubleQuoteStarted:
				continue
			if starCommentStarted:
				if i>1 and content[i-1]=='*':
					if i+1<length-1 and content[i+1]=='\n':
						commentsPos.append(i+1)
					else:
						commentsPos.append(i)
					starCommentStarted=False
				continue
			if i<length-1:
				if content[i+1]=='/' and not starCommentStarted:
					# comment use: //
					commentsPos.append(i)
					i=content.find('\n',i)
					if i<0:
						commendPos.append(length-1)
						break
					commentsPos.append(i)
				elif content[i+1]=='*':
					commentsPos.append(i)
					starCommentStarted=True
					# considering: /*/
					if i+3<length-1:
						i=i+3
				continue
	# end with /*
	if starCommentStarted:
		commentsPos.append(length-1)
	if len(commentsPos)%2!=0:
		print "exception in parse comments"
		exit(-1)

	# get comments
	comments=''
	i=0
	while True:
		if i>len(commentsPos)-2:
			break
		comments=comments+content[commentsPos[i]:commentsPos[i+1]+1]
		i=i+2

	# get content without comments
	nocomments=''
	i=0
	while True:
		if i>len(commentsPos)-1:
			break
		if i==0:
			if commentsPos[i]!=0:
				nocomments=nocomments+content[0:commentsPos[i]]
		elif i==len(commentsPos)-1:
			if commentsPos[i]!=len(content)-1:
				nocomments=nocomments+content[commentsPos[i]+1:]
		elif i%2==1:
			nocomments=nocomments+content[commentsPos[i]+1:commentsPos[i+1]]
		i=i+1
	return commentsPos,comments,nocomments


if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	help='''\npython commentsParser.py [-f] fileName\nonly java files currently'''
	parser=optparse.OptionParser(usage=help)
	parser.add_option("-f", "--file_name",action="store", type="string", dest="file_name")
	options,args=parser.parse_args(sys.argv[1:])
	if options.file_name==None or len(args)!=0:
		parser.print_help()
		exit(-1)
	fileName=options.file_name.strip()
	if not fileName.endswith('.java') and not fileName.endswith('.js'):
		parser.print_help()
		exit(-1)
	commentsPos,comments,nocomments=parseComments(fileName)
	print "content without comments:"
	print nocomments
