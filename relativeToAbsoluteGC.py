#!/usr/bin/python
import sys,datetime

if len(sys.argv) != 2:
	print "SYNTAX: " + sys.argv[0] + " gc.log"
	sys.exit(1)
	
try:
	inputlog = sys.argv[1]
	f = open(inputlog)
	line = f.readline() + sys.argv[1]
except:
	print "Problem reading "  + sys.argv[1]
	sys.exit(1)	

if (inputlog[:3]=='gc-' and len(inputlog.split("-")[1])==14):
	print inputlog
	starttime = inputlog.split("-")[1]
	starttime = datetime.datetime(int(starttime[0:4]),int(starttime[4:6]),int(starttime[6:8]),int(starttime[8:10]),int(starttime[10:12]),int(starttime[12:14]))
else:
	print "Incorrect input file name format"
	sys.exit(1)	
	
while line:
	if (line.find(": [GC")>0 or line.find(": [Full")>0):
		line = line.split(": [")
		interval = datetime.timedelta(seconds=float(line[0].replace(",",".")))
		gctime = starttime + interval
		line = gctime.strftime("%Y-%m-%d %H:%M:%S") + ": [" + line[1]
	print line[:-1]
	line = f.readline()
f.close()

 

