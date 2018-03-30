#!/usr/bin/env bash
palette="./palette.png"
filtersPalete="fps=24,scale=640:-1:flags=lanczos"
#filtersPalete="fps=12"
filtersGif="fps=24,scale=640:-1:flags=lanczos"

#ffmpeg -ss 00:00:01 -i $1 -vf "$filtersPalete,palettegen=stats_mode=diff" -y $palette
ffmpeg -ss 00:00:01 -i $1 -vf "$filtersPalete,palettegen=stats_mode=full" -y $palette
ffmpeg -i $1 -i $palette -lavfi "$filtersGif [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=3" -y $1.gif
