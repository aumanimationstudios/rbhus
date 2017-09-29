#!/usr/bin/env bash
# This script requires:
# - that the program socat be installed
# - that you start mpv with the IPC socket feature pointing at /tmp/mpvsocket
#   I recommend an alias in your .bashrc or equivalent file if starting from cmd:
#       alias mpv="mpv input-ipc-server=/tmp/mpvsocket"
#   Otherwise add input-ipc-server=/tmp/mpvsocket to mpv.conf file

Socket="/tmp/mpv.sock"
Command=""

if [ -n "$1" ];then
	case "$1" in
		-h|--help|h|help) less "$0" ;;
		--pause|pause) Command="{ \"command\": [\"set_property\", \"pause\", true] }" ;;
		--play|play) Command="{ \"command\": [\"set_property\", \"pause\", false] }" ;;
		--stop|stop) Command="{ \"command\": [\"quit\"] }" ;;
		--cycle_pause|cycle_pause) Command="{ \"command\": [\"cycle\", \"pause\"] }" ;;
		--sub-fps|sub-fps) Command="{ \"command\": [\"set_property\", \"sub-fps\", \"$2\"] }" ;;
		--next|next) Command="playlist_next" ;;
		--previous|previous) Command="playlist_prev" ;;
		*) echo "Invalid Parameter" && exit ;;
	esac
echo "${Command}" | socat - "${Socket}"
else
echo "No parameters found. "
fi
