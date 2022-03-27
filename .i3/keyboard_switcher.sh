#!/bin/bash
layout=`setxkbmap -query | grep layout | cut -d ' ' -f 6`
echo $[ "$layout" == "pl" ] >> kok
if [ "$layout" == "pl" ]; then
	setxkbmap -layout ru 
	echo "changing" >> kok
fi

if [ "$layout" == "ru" ]; then	
	setxkbmap -layout pl 
fi
echo $layout >> kok

