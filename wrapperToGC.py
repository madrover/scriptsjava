#!/usr/bin/python
import sys

if len(sys.argv) != 2 and sys.stdin.isatty():
	print "SYNTAX: " + sys.argv[0] + " wrapper.log"
	sys.exit(1)


try:
	inputlog = sys.argv[1]
	f = open(inputlog)
	line = f.readline()
except:
	try:
		f = sys.stdin
		line = f.readline()
	except:
		print "Problem reading stdin or input file"
		sys.exit(1)

gc=''
date = ''
while line:
	daten = line[20:30].replace("/","")
	if date != daten:
		date = daten
	out=line[42:]
	if (out.find("GC")>0) and (out.find("->")>0):
		print out,
		#gcf.write(out)
	if (out.find("GC")>0) and not (out.find("->")>0):
		gc=out
	if not (out.find("GC")>0) and (out.find("->")>0):
		out = gc + out
		out = out.replace("\n","").replace("\r","")
		if (out.find("GC")>0) and (out.find("->")>0):
			print out
			#gcf.write(out + "\n")
	#if (out.find("->")>0:
	#		print gc
	line = f.readline()
f.close()

