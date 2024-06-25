#!/bin/bash

mount /boot
rm -frv /crap/gentooOnesis-arch
mkdir /crap/gentooOnesis-arch

/opt/rbhus/tools/cloning/clone/makeClone.py --root / -t /crap/gentooOnesis-arch  -l /blueprod/CRAP/crap:/crap/crap.server -b -x root,var/cache/pacman,proc,dev,sys,blueprod,mnt,/crap,/BACKUP/,run,/etc/udev/rules.d/,tmp,home,.config/,.pulse/,.pulse-cookie,/etc/conf.d/hostname,etc/mtab -m root:root,sys:root,home:root,tmp:root%0777,/etc/udev/rules.d/:root,run:root,/dev/:root,/proc/:root,crap:root,mnt/cdrom:root,mnt/livecd:root,crap/LOCAL.crap:root%0777,crap/versionCache:root%0777,crap/mercurial:root%0777 -e var/tmp,var/log,opt/home/bluepixels
cp -av /etc/fstab.clone /crap/gentooOnesis-arch/etc/fstab
ssh clonemaster -C "rm -fr /crap/gentooOnesis-arch"
rsync -avHX /crap/gentooOnesis-arch clonemaster:/crap/


