#!/bin/bash
mount /boot                                                                                                                                                                                                                        
rm -frv /crap/gentooOnesis                                                                                                                                                                                                  
mkdir /crap/gentooOnesis        

/home/shrinidhi/bin/gitHub/sys/clone/makeClone.py --root / -t /crap/gentooOnesis/  -l /blueprod/STOR1/CRAP.serv/:/crap/STOR1.crap,/blueprod/STOR1/backup1/:/crap/incoming -b -x proc,dev,sys,blueprod,mnt,/crap,/BACKUP/,run,/etc/udev/rules.d/,tmp,home,.config/,root/,.pulse/,.pulse-cookie,/etc/conf.d/hostname,etc/mtab -m root:root,sys:root,home:root,tmp:root,/etc/udev/rules.d/:root,run:root,/dev/:root,/proc/:root,/crap:root,mnt/cdrom:root,mnt/livecd:root,/crap/LOCAL.crap:root%0777 -e var/tmp,var/log
rsync -av /crap/gentooOnesis/etc/skel/ /crap/gentooOnesis/root/ ; chown root:root /crap/gentooOnesis/root/ -Rv




