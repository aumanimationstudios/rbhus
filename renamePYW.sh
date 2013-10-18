#!/bin/sh
rsync -av ./ /projdump/pythonTestWindoze.DONOTDELETE/rbhus/ --delete --exclude=*.pyc --exclude=.git
cd /projdump/pythonTestWindoze.DONOTDELETE/rbhus/ ; ./clean.sh ; cd -
cd /projdump/pythonTestWindoze.DONOTDELETE/rbhus/rbhusUI/ ; rename .py .pyw * ; cd -
cd /projdump/pythonTestWindoze.DONOTDELETE/rbhus/rbhusUI/guiBin/ ; rename .py .pyw * ; cd -

