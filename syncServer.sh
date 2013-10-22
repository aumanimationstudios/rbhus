#!/bin/sh
pkill -9 rQ
rsync -av ./ /opt/rbhus/ --delete --exclude=*.pyc --exclude=.git
cd /opt/rbhus/ ; ./clean.sh ; ./rbhusQueen.sh
cd -



