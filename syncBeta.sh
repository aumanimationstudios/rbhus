#!/bin/bash
rsync -av ./ /projdump/pythonTestWindoze.DONOTDELETE/rbhusBeta/ --delete --exclude=*.pyc --exclude=.git
cd /projdump/pythonTestWindoze.DONOTDELETE/rbhusBeta/ ; ./clean.sh ; cd -
cd -


