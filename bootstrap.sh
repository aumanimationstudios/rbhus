#!/usr/bin/env bash
rm -rf rbhus-env
python2 -m virtualenv rbhus-env
source rbhus-env/bin/activate
unset PYTHONPATH
python2 -m pip install -r requirements.txt
ln -s /usr/lib/python2.7/site-packages/PyQt4 /opt/rbhus/rbhus-env/lib/python2.7/site-packages/PyQt4
ln -s /usr/lib/python2.7/site-packages/PyQt5 /opt/rbhus/rbhus-env/lib/python2.7/site-packages/PyQt5
ln -s /usr/lib/python2.7/site-packages/sip.so /opt/rbhus/rbhus-env/lib/python2.7/site-packages/sip.so
#echo "----- Created venv -------"
