#!/bin/sh

if [[ $0 != "/"* ]]; then SCRIPTDIR=`pwd`; else SCRIPTDIR=`dirname $0`;fi
$SCRIPTDIR/wrapperToGC.py $1 > $1.gc
echo $1.gc