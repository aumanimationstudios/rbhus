#!/bin/sh
mv -v --no-clobber /usr/share/polkit-1/actions/org.freedesktop.udisks2.policy /usr/share/polkit-1/actions/org.freedesktop.udisks2.policy.old
chown bluepixels:bluepixels /usr/bin/firefox* ; chmod 700 /usr/bin/firefox*
chown bluepixels:bluepixels /usr/bin/google-chrome* ; chmod 700 /usr/bin/google-chrome*
rsync -av ubuntu/ /

