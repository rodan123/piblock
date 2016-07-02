"""
 *  Library radio
 *
 *  Copyright:  Copyright 2014 David Brown
 *
 *  Radio is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You may view a copy of the GNU General Public License at:
 *             <http://www.gnu.org/licenses/>.
 *
 *  Description:
 *  This is a sample python client for the radio library included with
 *  jcblock. This example client prints to stdout some parts of the received callerID
 *  record. From that point downward you can use other system integration tools
 *  to provide user feedback. Other languages have similar socket API, and
 *  not much modification is required to adapt this sample to them. I picked
 *  python because on my desktop OS there are notification tools with python
 *  bindings.
 *
 *  Remember when you post code, you never know who might need it and how much
 *  they might truly appreciate it. Even if it's just to hang up on people.
 *
"""
from socket import *
import re

# sample input: --DATE = 032914--TIME = 1007--NMBR = 8005551212--NAME = SOMESCUMSUCKERS--
pattern = re.compile('.-DATE = (.*)--TIME = (.*)--NMBR = (.*)--NAME = (.*)--')

s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 9753))
print 'udp ready!'
BUFSIZE = 512
while True:
    data, addr = s.recvfrom(BUFSIZE)
    print('server received %r from %r' % (data, addr))
    result = pattern.match(data)
    if result:
        print "Number to look up: "
        print result.group(3)
        print "If you had an address book API, you do a case insensitive lookup:"
        print result.group(4)

