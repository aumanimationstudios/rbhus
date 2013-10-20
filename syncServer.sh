#!/bin/sh
rsync -av ./ /opt/rbhus/ --delete --exclude=*.pyc --exclude=.git
cd /opt/rbhus/ ; ./clean.sh ; cd -


