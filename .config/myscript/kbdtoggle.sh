#!/bin/bash

curlayout=`setxkbmap -query | awk 'FNR==3 {print $2}'`

if [ $curlayout == "us" ]; then
	setxkbmap it
else
	setxkbmap us
fi
