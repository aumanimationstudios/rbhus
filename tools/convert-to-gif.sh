#!/usr/bin/env bash
palette="./palette.png"
filtersPalete="fps=24,scale=480:-1:flags=lanczos"
filtersGif="fps=24,scale=480:-1:flags=lanczos"

ffmpeg -i $1 -vf "$filtersPalete,palettegen" -y $palette
ffmpeg -i $1 -i $palette -lavfi "$filtersGif [x]; [x][1:v] paletteuse" -y $1.gif
