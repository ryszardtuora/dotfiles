#!/bin/bash

counter=2
p_=p
while :
do
	wallpaper=$(find ~/Wallpapers | sed -n $counter$p_)
	num_wallpapers=$(ls -l ~/Wallpapers | wc -l)
	feh --bg-fill $wallpaper
	counter=$((counter + 1))
	sleep 180s
	if [[ $counter -gt $num_wallpapers ]]; then
		counter=2
	fi
done
