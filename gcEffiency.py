#!/usr/bin/env python

#
# This script is used calculate the efficiency of the Garbage Collector.
# It analyzes the input java garbage collector and calculates how much time the JVM is spending doing garbage collection
# This script can be used to define a garbage collection baseline and to find how different tuning are affecting its effiency
#
import sys, os
import argparse


def analyzeLog(log):
	totalgccount=shortgccount=fullgccount=0
	totalgctime=shortgctime=fullgctime=0
	apptime=previoustime=0

	with open(log) as f:
		for line in f:
			line = line.replace("\r","").replace("\n","")
			#print line
			try:
				totalgccount += 1
				pos = line.find(" secs]")
				if pos != -1: 
					line = line[:pos]
					time = float(line.split(" ")[-1])
					currenttime = float(line.split(" ")[0][:-1])

					totalgctime += time
					# print time
					if line.find("[GC") != -1:
						shortgccount += 1
						shortgctime += time
					if line.find("[Full GC") != -1:
						fullgccount += 1
						fullgctime += time

					if previoustime != 0:
						if previoustime < currenttime:
							apptime += (currenttime - previoustime)
						else:
							#If JVM has restarted
							apptime += currenttime
					previoustime = currenttime

				
			except Exception as e:
				print "Error processing line: " + line
				print e


	efficency = "{0:.4f}".format(1 - (totalgctime/apptime))

	if totalgccount != 0:
		totalgcavg = "{0:.4f}".format(totalgctime/totalgccount)
	else:
		totalgcavg = "0"
	totalgctime = "{0:.4f}".format(totalgctime)
	totalgccount = str(totalgccount)

	if shortgccount != 0:
		shortgcavg = "{0:.4f}".format(shortgctime/shortgccount)
	else:
		shortgcavg = "0"
	shortgctime = "{0:.4f}".format(shortgctime)
	shortgccount = str(shortgccount)

	
	if fullgccount != 0:
		fullgcavg = "{0:.4f}".format(fullgctime/fullgccount)
	else:
		fullgcavg = "0"
	fullgctime = "{0:.4f}".format(fullgctime)
	fullgccount = str(fullgccount)

	apptime = "{0:.4f}".format(apptime)
	
	if args.csv:
		print log + ";" + efficency + ";" + apptime + ";" + totalgccount + ";" + totalgctime + ";" + totalgcavg + ";" + shortgccount + ";" + shortgctime + ";" + shortgcavg + ";" + fullgccount + ";" + fullgctime + ";" + fullgcavg + ";"

	else:
		print "Log: " + log
		print "Application execution time = " + apptime + " secs"
		print "Efficency = " + efficency + "%"
		print "Total GC:    Count = " + totalgccount.ljust(8) + " Total time = " + totalgctime + " secs".ljust(8) + " Average time = " + totalgcavg + " secs".ljust(8)
		print "Short GC:    Count = " + shortgccount.ljust(8) + " Total time = " + shortgctime + " secs".ljust(8) + " Average time = " + shortgcavg + " secs".ljust(8)
		print "Full GC:     Count = " + fullgccount.ljust(8) + " Total time = " + fullgctime + " secs".ljust(8) + " Average time = " + fullgcavg + " secs".ljust(8)


parser = argparse.ArgumentParser(description='Calculate the GC efficency for Java GC logs.')
parser.add_argument('logs', metavar='log', type=str, nargs='+',
                   help='garbage logs')
parser.add_argument('-c','--csv', dest='csv', action='store_true',
                   # const=sum, default=max,
                   help='Show output as CSV')

args = parser.parse_args()
#print args.accumulate(args.integers)

if args.csv:
	print "log;efficency;apptime;totalgccount;totalgctime;totalgcavg;shortgccount;shortgctime;shortgcavg;fullgccount;fullgctime;fullgcavg;"

for log in args.logs:
	if os.path.exists(log):
		analyzeLog(log)