# dbpiblock
Fork of the jcblock_log_to_MySQL program modified to run locally on a raspberrypi with some enhancements.

This is a fork of the jcblock_log_to_MySQL project by Thomas Miller (https://github.com/tomjavamiller/jcblock_log_to_MySQL).

I use it to keep a complete record of the callerID log.  It is run as a prerotation script for logrotate and adds the months callers to a MySQL database. It creates a report showing the all time most persistant blacklisted junk callers.
Like the original author, I have a telephone feature that allows me to block a limited number of calling numbers (10), so that they do not even ring in. I would like to find the most obnoxious and persistant junk callers to include on that short list. Also, keeping a complete callerID history may prove beneficial for other uses in the future.

The program may also be run manually to create a current report.

07/07/16 - Initial commit

1) Changed the callerID retrieval to perform a local copy of the callerID log rather than a remote fetch via scp. Added code to handle piblock's extended call tags and changed sort order so that the most persistant caller is on top. The program will still run with a vanilla jcblock installation.

2) Added an optional command line argument to limit output to callers who have called X number of times. 
   Ex: python getcall.py 4, shows the blacklisted callers who have called 4 or more times historically. Default = 2.
		
3) Created an INSTALL readme for getting the program running on the raspberrypi. It requires the installation of several supporting packages and some initial database administration.

4) Created a /etc/logrotate/piblock config file to run this program before archiving the callerID log and create a current cidreport.log in the program directory.
       

  