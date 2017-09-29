#!/bin/bash

mount /boot
rm -frv /crap/gentooOnesis-gentoo
mkdir /crap/gentooOnesis-gentoo

/home/shrinidhi/bin/gitHub/sys/clone/makeClone.py --root / -t /crap/gentooOnesis-gentoo  -l /blueprod/STOR2/stor2/stor1/crap:/crap/STOR1.crap -b -x root,usr/portage,proc,dev,sys,blueprod,mnt,/crap,/BACKUP/,run,/etc/udev/rules.d/,tmp,home,.config/,.pulse/,.pulse-cookie,/etc/conf.d/hostname,etc/mtab -m root:root,sys:root,home:root,tmp:root%0777,/etc/udev/rules.d/:root,run:root,/dev/:root,/proc/:root,crap:root,mnt/cdrom:root,mnt/livecd:root,crap/LOCAL.crap:root%0777,crap/versionCache:root%0777,crap/mercurial:root%0777 -e var/tmp,var/log,opt/home/bluepixels
cp -av /etc/fstab.clone /crap/gentooOnesis-gentoo/etc/fstab

rsync -avHX /crap/gentooOnesis-gentoo clonemaster:/crap/


