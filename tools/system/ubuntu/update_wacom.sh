#!/bin/sh

wget https://projects.kde.org/projects/extragear/base/wacomtablet/repository/revisions/master/raw/data/wacom_devicelist -O ~/wacom_devicelist
cp -v ~/wacom_devicelist /usr/share/kde4/apps/wacomtablet/data/wacom_devicelist
chmod -v 644 /usr/share/kde4/apps/wacomtablet/data/wacom_devicelist