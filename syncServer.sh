#!/bin/sh
pkill -9 rQ
pkill -9 pD
rsync -av ./ /opt/rbhus/ --delete --exclude=*.pyc --exclude=.git
cd /opt/rbhus/ ; ./clean.sh ; ./rbhusQueen.sh 
cd -



