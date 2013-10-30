#!/bin/sh
if [[ $0 != "/"* ]]; then SCRIPTDIR=`pwd`; else SCRIPTDIR=`dirname $0`;fi

for i in `cat $1 | grep jvm | awk '{print $6}' | egrep ".*/.*/.*" | sort | uniq`
do
	LOG=wrapper.gc.`echo $i | tr / -`
	echo $LOG
	grep $i $1 | $SCRIPTDIR/wrapperToGC.py > $LOG
done
