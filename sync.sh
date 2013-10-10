#!/bin/sh
rsync -av ./ /projdump/pythonTestWindoze.DONOTDELETE/rbhus/ --delete --exclude=*.pyc --exclude=.git
cd /projdump/pythonTestWindoze.DONOTDELETE/rbhus/ ; ./clean.sh ; cd -
cd -


