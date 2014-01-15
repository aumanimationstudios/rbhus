#!/bin/bash
mount /boot                                                                                                                                                                                                                        
rm -fr /crap/gentooOnesis.bak.old                                                                                                                                                                                                            
mv /crap/gentooOnesis.bak /crap/gentooOnesis.bak.old                                                                                                                                                                                         
mv /crap/gentooOnesis /crap/gentooOnesis.bak                                                                                                                                                                                                 
mkdir /crap/gentooOnesis        

/home/shrinidhi/bin/gitHub/sys/clone/makeClone.py --root / -t /crap/gentooOnesis/  -l /blueprod/STOR1/CRAP.serv/:/crap/STOR1.crap,/blueprod/STOR1/backup1/:/crap/incoming -b -x prod,proc,dev,sys,blueprod,mnt,/crap,/BACKUP/,/usr/portage,run,/etc/udev/rules.d/,tmp,home,.config/,.pulse/,.pulse-cookie,/etc/conf.d/hostname,etc/mtab -m sys:root,home:root,tmp:root,/etc/udev/rules.d/:root,run:root,/dev/:root,/proc/:root,/crap:root,mnt/cdrom:root,mnt/livecd:root,/usr/portage:portage,/crap/LOCAL.crap:root%0777 -e /var/cache/,/var/log/,var/tmp,var/spool




