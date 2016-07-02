#!/bin/sh
cd ~/jcadmin
node jcadmin.js 9292 /home/pi/piblock/ >> jcadmin.log &
clear
cd ~/piblock
sleep 5
./piblock

