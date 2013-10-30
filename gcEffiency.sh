#!/bin/sh

if [ "$#" -eq 1 ]
then
    GCLOG=$1
    CSV=FALSE
elif [ "$#" -eq 2 -a "$1" = "-c" ]
then
    GCLOG=$2
    CSV=TRUE
else
    echo "USAGE; $0 [-c] gc.log"
    exit 1
fi

cat "$GCLOG" | awk -v CSV=$CSV -v GCLOG=$GCLOG '
    BEGIN{
        TOTALGCCOUNT=0
        TOTALGCTIME=0
        TOTALGCAVERAGE=0
        GCCOUNT=0
        GCTIME=0
        GCAVERAGE=0
        FULLGCCOUNT=0
        FULLGCTIME=0
        FULLGCAVERAGE=0
        EFFICIENCY=0
    };
    {
        TOTALAPPTIME=substr($1, 1, length($1-1))
        TOTALGCTIME=TOTALGCTIME+$(NF-1)
        TOTALGCCOUNT=TOTALGCCOUNT+1
        where = match($0, "Full")
        if (where){
            FULLGCCOUNT=FULLGCCOUNT+1
            FULLGCTIME=FULLGCTIME+$(NF-1)
        }else{
            GCCOUNT=GCCOUNT+1
            GCTIME=GCTIME+$(NF-1)
    }    
    }
    END{
        
        if (TOTALGCCOUNT>0){TOTALGCAVERAGE=TOTALGCTIME/TOTALGCCOUNT}
        if (GCCOUNT>0){GCAVERAGE=GCTIME/GCCOUNT}
        if (FULLGCCOUNT>0){FULLGCAVERAGE=FULLGCTIME/FULLGCCOUNT}
        if (TOTALGCCOUNT>0){EFFICIENCY=1-(TOTALGCTIME/TOTALAPPTIME)}
        
        if (CSV=="FALSE"){
            print GCLOG
            print "TOTAL APP TIME    " TOTALAPPTIME
            print "EFFICIENCY        " EFFICIENCY
            print "TOTAL GC"
            print "     COUNT        " TOTALGCCOUNT
            print "     TIME         " TOTALGCTIME
            print "     AVERAGE      " TOTALGCAVERAGE
            print "NON FULL GC "
            print "     COUNT        " GCCOUNT
            print "     TIME         " GCTIME
            print "     AVERAGE      " GCAVERAGE
            print "FULL GC     "
            print "     COUNT        " FULLGCCOUNT
            print "     TIME         " FULLGCTIME
            print "     AVERAGE      " FULLGCAVERAGE
        }
        else
        {
            print "GCLOG;TOTALAPPTIME;EFFICIENCY;TOTALGCCOUNT;TOTALGCTIME;TOTALGCAVERAGE;GCCOUNT;GCTIME;GCAVERAGE;FULLGCCOUNT;FULLGCTIME;FULLGCAVERAGE"
            print GCLOG ";" TOTALAPPTIME ";" EFFICIENCY ";" TOTALGCCOUNT ";" TOTALGCTIME ";" TOTALGCAVERAGE ";" GCCOUNT ";" GCTIME ";" GCAVERAGE ";" FULLGCCOUNT ";" FULLGCTIME ";" FULLGCAVERAGE
        }
    }'