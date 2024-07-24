#!/bin/bash

mount /boot
rm -frv /crap/gentooOnesis-network
mkdir -p /crap/gentooOnesis-network

./makeClone_old.py --root / -t /crap/gentooOnesis-network  -b -x var/lib/named/proc,root,proc,dev,sys,blueprod,mnt,/crap,/BACKUP/,run,/etc/udev/rules.d/,tmp,home,.config/,.pulse/,.pulse-cookie,etc/mtab -m root:root,sys:root,home:root,tmp:root%0777,/etc/udev/rules.d/:root,run:root,/dev/:root,/proc/:root,crap:root,mnt/cdrom:root,mnt/livecd:root,crap/LOCAL.crap:root%0777,crap/versionCache:root%0777,crap/mercurial:root%0777 -e var/tmp,var/log,opt/home/bluepixels
cp -av /etc/fstab.clone /crap/gentooOnesis-network/etc/fstab
ssh clonemaster -C "rm -fr /crap/gentooOnesis-network"

rsync -avHX /crap/gentooOnesis-network clonemaster:/crap/
