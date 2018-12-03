#!/bin/bash
if [ "$(whoami)" == "bluepixels" ]; then
        echo "Script cannot be run as bluepixels"
        exit -1
fi
nohup xiccd &
sleep 5
colorprofile=`colormgr find-profile-by-filename /usr/share/color/icc/colord/sRGB.icc | grep -i object | gawk -F ":" '{gsub(/ /,"",$2); print $2}'`
echo "Using sRGB profile "$colorprofile
colormgr get-devices | grep -i object| gawk -v colorprofile=$colorprofile -F ":" '{gsub(/ /,"",$2);print "colormgr device-add-profile "$2" "colorprofile}'| sh -v
wait