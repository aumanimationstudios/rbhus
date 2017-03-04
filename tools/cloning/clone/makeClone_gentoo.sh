#!/bin/bash

mount /boot
rm -frv /crap/gentooOnesis
mkdir /crap/gentooOnesis

/home/shrinidhi/bin/gitHub/sys/clone/makeClone.py --root / -t /crap/gentooOnesis  -l /blueprod/STOR1/CRAP.serv/:/crap/STOR1.crap,/blueprod/STOR1/backup1/:/crap/incoming -b -x usr/portage,proc,dev,sys,blueprod,mnt,/crap,/BACKUP/,run,/etc/udev/rules.d/,tmp,home,.config/,.pulse/,.pulse-cookie,/etc/conf.d/hostname,etc/mtab -m sys:root,home:root,tmp:root%0777,/etc/udev/rules.d/:root,run:root,/dev/:root,/proc/:root,crap:root,mnt/cdrom:root,mnt/livecd:root,crap/LOCAL.crap:root%0777,crap/versionCache:root%0777,crap/mercurial:root%0777 -e var/tmp,var/log
rsync -av /crap/gentooOnesis/etc/skel/ /crap/gentooOnesis/root/ ; chown root:root /crap/gentooOnesis/root/ -Rv
cp -av /etc/fstab.clone /crap/gentooOnesis/etc/fstab


