# jcadmin-piblock
Fork of the jcadmin program modified to work with piblock's handling of callerID rotation and tag additions.

This is a fork of the jcadmin project by Don Cross (https://github.com/cosinekitty/jcadmin). It monitors the callerID log and experimentally allows entries to be modified.

07/01/16 - Initial commit

1) Changed handling of log files to allow system log rotation. jcadmin will load and display the current
   callerID.dat log file and the log from the previous month. (Must use the logrotate naming convention from piblock)

2) Added an "Internet" icon to tag entries that were matched on 800notes.com. Modified the "neutral" icon to not 
   be a blank icon.	

3) Added two screenshots to show the modified app home screen.

07/04/16

4) Modified jcclient.js SanitizeSpaces function to not remove whitespace from within. It was causing classification 
   mismatches for callerID names that contained multiple spaces. ex; (_=sp): DIR_ASSIST___CA
       

  