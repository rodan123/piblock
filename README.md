# piblock
Fork of the jcblock junk call blocker to add features and changes that may be useful.

This is a fork of the jcblock project by Walter S. Heath (http://jcblock.sourceforge.net/jcblock.html)
I run this project, piblock, on a raspberrypi3 using an iphone4 as a ssh terminal and display.

07/01/16 - Initial commit
1) Added text output formated to iphone ssh screen to display program status and call handling information.
2) Added code to perform an additional check. Upon recieving a call from a number not already on either the whitelist or blacklist,
   the program checks to see if the number has been reported at 800notes.com. The program is brutal if the number has been reported.
   It terminates the call and added the caller's name to the blacklist.
3) Added code to properly record, in the callerID.dat logfile, a call that goes to voicemail/ansering machine.
   Original program failed to record calls that were not answered within four rings when using the answering machine option.
4) Extended blacklist truncation time to one year. Removed callerID.dat truncation and wrote config to use system logrotate to
   rotate callerID logs. Logrotate retains callerID logs for one year, rotates monthly, and archived logs are labeled by month.
   Example: callerID.dat.06 is the archived log from June past. Copy the repo's logroate.d/piblock file to /etc/logrotate.d/piblock
   and edit the path to calledID.dat within.
5) Added two new callerID.dat flags, in addition to W (whitelist) B (blacklist) and - (Answered), added I (Internet match) and 
   M (Missed)

   
