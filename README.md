# piblock
Fork of the jcblock junk call blocker to add features and changes that may be useful.

This is a fork of the jcblock project by Walter S. Heath (http://jcblock.sourceforge.net/jcblock.html)

I run piblock on a raspberrypi3 using an dedicated iphone4, running the Reflection SSH client, 
(https://itunes.apple.com/us/app/reflection-for-unix-ssh-client/id920472514?mt=8ht), as a ssh terminal and display.

07/01/16 - Initial commit

1) Added text output formated to iphone ssh screen to display program status and call handling information.

2) Added code to perform an additional check. Upon receiving a call from a number that is not already on either 
   the whitelist or the blacklist, the program checks to see if the number has been reported at 800notes.com. 
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

8) Added softlink of 800notes.txt to 800notes.html, so that the last matched caller's internet data can easily 
   be viewed locally. I installed lynx on the raspberrypi3 to view the file over a SSH connection. 


   
