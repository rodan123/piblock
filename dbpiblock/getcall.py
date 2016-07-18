#!/usr/bin/python
########################################################################################
# 1. Copies jcblock's callerid.dat file from raspberry pi
# 2. loop though each line of the callerid.dat file
#    2.1 parse the line using regex
#    2.2 print to standard out the information in CSV format
#    2.3 using sqlalchemy, add row to MySQL table (if not there already)
# 3. Query the table 
#
# Reason:
# The phone company will block 25 phone numbers for me, therefore
# with this script, I can quickly add the caller id's to the database and 
# display the most likely numbers that I should add, if any.
#
#  Copyright (C) 2015  Thomas Miller
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################################
import re
import os
import sys
import datetime
import phonenumbers

from tabulate import tabulate
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func, BLOB, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# ********* EDIT the paths below to suit installation
# Home directory of piblock/jcblock
piblockdir = "/home/pi/piblock/"
# Home directory of the getcall.py program
dbdir = "/home/pi/dbpiblock/"
# Phone number format
country = "US"

#Set min call total to display, default to all.
calltotal = 0
logmode ="simple"
header = ["number", "name", "last call", "count"]
if len(sys.argv) > 1:
    if sys.argv[1].isdigit():
        calltotal = int(sys.argv[1]) - 1
    else:
        if sys.argv[1].lower() == "html":
            logmode = "html"
            header = ["number", " ","name", " ", "last call", " ", "count"]
    if len(sys.argv) > 2:
        if sys.argv[2].lower() == "html":
            logmode = "html"
            header = ["number", " ","name", " ", "last call", " ", "count"]
        
#setup sqlalchemy
Base = declarative_base()
# ********* EDIT username:password (pi:password) to contain local user's database credentials
engine = create_engine("mysql+pymysql://pi:piblock@localhost/callerid?charset=utf8&use_unicode=0")
#engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# define the callerid table objects:
class callerid(Base):
    __tablename__ = 'callerid'

    timestamp = Column(TIMESTAMP, primary_key=True )
    number = Column(String(10))
    name = Column(String(15))
    code = Column(String(1))

    def __init__(self, timestamp, number, name, code):
        self.timestamp = timestamp
        self.number = number
        self.name = name
        self.code = code

    def __str__(self):
        name = self.__class__.__name__ + ': '
        attrs = [ '->{}<-=->{}<-'.format(k,v) for (k,v) in sorted(self.__dict__.items()) ]
        return name + ',\n'.join(attrs)

def createCallerIdTable():
    #print('create_table')
    Base.metadata.create_all(engine)
    #print('create_table end')

def readCallLog():
    #open the copied caller id log file from Raspberry Pi
    f = open(dbdir+'callerID.dat', 'rU')
    #out = open('callerID.csv', 'a')

    #setup the lastdate
    lastdate = datetime.datetime.now()
    secs = 0

    #read each line from file:
    for line in f:

        # each line is like: B-DATE = 010215--TIME = 1024--NMBR = 8003310500--NAME = TOLL FREE      --
        #                    B-DATE = 012915--TIME = 1321--NMBR = 7707692444--NAME = MARKETING--
        #                    W-DATE = 022115--TIME = 0801--NMBR = 7195555555--NAME = JIM JOHNSON    --
        #                    --DATE = 022115--TIME = 1003--NMBR = 7198888888--NAME = COLORADO       --
        match = re.search('(.)-DATE = (\d\d)(\d\d)(\d\d)--TIME = (\d\d)(\d\d)--NMBR = (.*?)--NAME = (.*?)--', line)
        #now group(1) is 'W', 'B', or '-'  whitelist, blacklist, none
        #    group(2) is month
        #    group(3) is day
        #    group(4) is 2 digit year
        #    group(5) is hour
        #    group(6) is minute
        #    group(7) is number
        #    group(8) is name

        # print out the line in CSV format
        # print('"%s","20%s/%s/%s %s:%s:00","%s","%s"'%(match.group(1),match.group(4),match.group(2),match.group(3),
        #                                              match.group(5),match.group(6),match.group(7),match.group(8)))

        # create the date
        thedate = datetime.datetime(int('20'+match.group(4)),int(match.group(2)),int(match.group(3)),int(match.group(5)),
                                                    int(match.group(6)))

        #if this datetime is the same as the last datetime, add a second
        if lastdate == thedate:
            secs += 1
            thedate = thedate.replace(second=secs)
        else:
            secs = 0
            lastdate = thedate

        try:
            #Create new callerid with this information
            aCall = callerid(thedate,match.group(7),match.group(8),match.group(1))
            #merge it into the database and commit
            session.merge(aCall)
            session.commit()
        except:
            #print('dup')
            pass

    f.close()

def queryB():
    #           and c2.timestamp > DATE_SUB(NOW(), INTERVAL 365 DAY)) \
    # count all the calls from numbers that called recently with a b (blacklisted):
    query = "select number, name, count(*), max(timestamp) from callerid c1 \
            where exists (select * from callerid c2 where c1.number = c2.number and (c2.code = 'B' or c2.code = 'I')) \
            and not exists (select * from callerid b where c1.number = b.number and b.code is null) \
        group by number \
        having count(*) > "+str(calltotal)\
        +" order by count(*) desc, max(timestamp) desc, name"
        
    #print a table of output:
    results = engine.execute(query)
    # print("\n")
    # print("+----------------+-----------------+----------+")
    # print("| number         | name            | count(*) |")
    # print("+----------------+-----------------+----------+")
    #for row in results:
    #    results[0] = phonenumbers.format_number(phonenumbers.parse(row[0].decode(), country), phonenumbers.PhoneNumberFormat.NATIONAL)
    #     print("| %-10.10s | %-15.15s | %8d |"%(row[0].decode(), row[1].decode(), row[2]) )
    # print("+----------------+-----------------+----------+")
    result = [r for r in results]
    results = []
    for r in result:
        x = r[0]
        d = str.split(str(r[3]))
        x = phonenumbers.format_number(phonenumbers.parse(x, country), phonenumbers.PhoneNumberFormat.NATIONAL)
        if logmode == "simple":
            x = [x, r[1], d[0], r[2]]
        else:
            x = [x, "&ensp;", r[1], "&ensp;", d[0], "&ensp;", r[2]]
        results.append(x)
    print tabulate(results, header, tablefmt=logmode)

#define a main in order to comment out the main call in order to import in interactive python
def main():
    #copy the phone call log from pi
    #pi ip needs to be in known hosts
    #ssh auth keys need to be setup for no password
    #Running locally on pi ignore above, do a simple copy
    os_command = "cp "+piblockdir+"callerID.dat "+dbdir+"callerID.dat"
    #print(os_command)
    os.system(os_command)

    #create table if it does not exist
    createCallerIdTable()

    #read call log and put info in the table
    readCallLog()

    #print a sub-query
    queryB()

main()
