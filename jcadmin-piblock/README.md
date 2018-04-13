# jcadmin-piblock
Fork of the jcadmin program modified to work with piblock's handling of callerID rotation and tag additions.

This is a fork of the jcadmin project by Don Cross (https://github.com/cosinekitty/jcadmin). It monitors the callerID log and experimentally allows entries to be modified.

07/01/16 - Initial commit

1) Changed handling of log files to allow system log rotation. jcadmin will load and display the current
   callerID.dat log file and the log from the previous month. (Must use the logrotate naming convention from piblock)

2) Added an "Internet" icon to tag entries that were matched on 800-----.com. Modified the "neutral" icon to not 
   be a blank icon.	

3) Added two screenshots to show the modified app home screen.

07/04/16

4) Modified jcclient.js SanitizeSpaces function to not remove whitespace from within. It was causing classification 
   mismatches for callerID names that contained multiple spaces.

08/25/16

5) Merged a few changes from the master repository. (https://github.com/cosinekitty/jcadmin) Particularly; Fixed #38 - Added horizontal line between history rows that cross calendar dates. Eliminated redundant copy of function FormatDateTime. Fixed #42 - make sure there is a newline delimiting appended record.

08/28/16

6) Merge; Fixed #39 - Allow user to cycle through showing all, blocked, safe, neutral on history display. 

10/10/16

7) Added an "asterisk" icon to tag entries that were manually blacklisted using the star key from a handset.
       

  