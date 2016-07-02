#!/bin/sh
cd ~/jcadmin-piblock
node jcadmin.js 9292 /home/pi/piblock/ >> jcadmin.log &
clear
cd ~/piblock
sleep 5
./piblock

