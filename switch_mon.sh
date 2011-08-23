#!/usr/bin/env bash
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# The script activates a monitor connected to the VGA port and
# turns off the laptop LCD panel, changing the wallpaper afterwards
##############

MAXRES=`xrandr | grep -A 1 VGA | sed '1d' | awk '{print $1}'`
WALL="/home/herself/Obrazy/Tapety/Fractal_Nebula_Tile_by_jennabee25.png"

xrandr --auto --noprimary --output VGA1 --mode $MAXRES --above LVDS1
if [[ $? -eq 0 ]]
then
	xrandr --output LVDS1 --off
fi

feh --bg-tile $WALL
