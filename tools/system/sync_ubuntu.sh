#!/bin/sh
mv -v --no-clobber /usr/share/polkit-1/actions/org.freedesktop.udisks2.policy /usr/share/polkit-1/actions/org.freedesktop.udisks2.policy.old
rsync -av ubuntu/ /

