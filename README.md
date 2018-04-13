# piblock
Fork of the jcblock junk call blocker to add features and changes that may be useful.

This is a fork of the jcblock project by Walter S. Heath (http://jcblock.sourceforge.net/jcblock.html)

I run piblock on a raspberrypi3 using an dedicated iphone4, running the Reflection SSH client, 
(https://itunes.apple.com/us/app/reflection-for-unix-ssh-client/id920472514?mt=8ht), as a SSH terminal and display.

07/01/16 - Initial commit

1) Added text output formated to iphone screen to display program status and call handling information.

2) Added code to perform an additional check. Upon receiving a call from a number that is not already on either 
   the whitelist or the blacklist, the program checks to see if the number has been reported at 800-----.com. 
   The program is brutal, if the number has been reported, it terminates the call and adds the caller's name
   to the blacklist.

3) Added code to properly record, in the callerID.dat logfile, a call that goes to voicemail/answering machine.
   Original program failed to record calls that were not answered within four rings when using the answering machine
   option.
   
4) Extended blacklist truncation time to one year. Removed callerID.dat truncation and use the system logrotate to
   handle callerID logs. Logrotate retains callerID logs for one year, rotates monthly, and archived logs are
   labeled by month. Example: callerID.dat.06 is the archived log from June past. 
   Copy the repo's logroate.d/piblock file to /etc/logrotate.d/piblock and edit the path to callerID.dat within.
   
5) Added two new callerID.dat tags, in addition to "W" (whitelist) "B" (blacklist) and "-" (Answered), 
   added "I" (Internet match) and "M" (Missed/VMail)

6) Added fork of the jcadmin program by Don Cross (https://github.com/cosinekitty/jcadmin) modified to work with 
   piblock's handling of callerID log rotation and tag additions.

7) Created a runpiblock.sh script to startup jcadmin and piblock. 
   Copy to your home directory and edit the program paths within as necessary.  

8) Added softlink of 800-----.txt to 800-----.html, so that the last matched caller's internet data can easily 
   be viewed locally. I installed lynx on the raspberrypi3 to view the file over a SSH connection. 

07/07/16

9) Added fork of the jcblock_log_to_MySQL project by Thomas Miller (https://github.com/tomjavamiller/jcblock_log_to_MySQL) to the dbpiblock directory.

07/15/16

10) Added error handling to the 800-----.com check to skip it if the website is unavailable.

08/01/16

11) Added a small bit of code to write out an unclassified callers name to hand off to IBM Bluemix. Does nothing, only useful with the node-red extension (see wiki)

08/14/16

12) Added code to change handling of short blacklist entries. Changed the behavior to require that any blacklist entry of less than 5 characters must match the callerID name exactly. Pure numeric blacklist entries are exempted and blacklist entries of 5 or more characters will still match as a substring. 

08/15/16

13) Added code to prevent blacklist entries from matching the date and time fields in the callerID string.
  
09/02/16

14) Improved 800----- junk call detection.

10/10/16

15) Added headers to curl query to get past recently implemented 800----- octonet filter. Removed references to 800----- from README.md in the unlikely event that curl was filtered on the site because of piblock automated queries.

10/18/16

16) Changes on the 800----- website, they changed wording on phone lookup. Modified program to work with it. 

04/13/18

17) New branch that contains modifications to work with VOIP callerID. VOIP displays an 11 digit number vs the POTS 10 numbers. Many other minor changes to improve functionality. Whitelist entries announced by IBM Bluemix using the data from the entries comment field if terminated withe an asterisk.
