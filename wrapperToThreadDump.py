#!/usr/bin/python
import sys

if len(sys.argv) != 2:
	print "SYNTAX: " + sys.argv[0] + " wrapper.log"
	sys.exit(1)
	
try:
	f = open(sys.argv[1])
	line = f.readline() + sys.argv[1]
except:
	print "Problem reading "  + sys.argv[1]
	sys.exit(1)
td=''
tdStart=False
heapStart=False
while line:
	l = f.readline()
	line=l[42:]
	if line.find("Full thread dump") != -1:
		tdStart=True
		tfSecond=l.split(" | ")[2]
		tfName="threadDump." + tfSecond.replace("/","").replace(" ","_").replace(":","") + ".txt"
			
	if tdStart:
		if l.find(tfSecond) != -1:
			if line.find("[GC") == -1 and line.find("[Unloading") == -1 and line.find("->") == -1:
				td = td + line
		else:
			tdStart = False
			print "Creating " + tfName
			tf = open( tfName, "w")
			tf.writelines(td)
			tf.close()
			td = ""

f.close()