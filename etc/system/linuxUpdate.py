#!/usr/bin/python

import sys
import os
import re

    
    
def gentooUpdate():
  try:
    masterSystem = os.environ['masterSystem']
  except:
    sys.exit(1)
    
  os.environ['PORTAGE_BINHOST'] = "http://"+ str(masterSystem) +"/"
  os.environ['SYNC'] = "rsync://" + str(masterSystem) +"/gentoo-portage"
  syncPortage = os.system("emerge --sync |& tee /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  syncSets = os.system("rsync -av rsync://"+ str(masterSystem) +"/sets /var/lib/portage/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  syncLayman = os.system("rsync -av rsync://"+ str(masterSystem) +"/layman /var/lib/layman/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  syncCbOverlay = os.system("rsync -av rsync://"+ str(masterSystem) +"/cb_overlay /usr/local/portage/cb_overlay/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  syncEtcPortage = os.system("rsync -av rsync://"+ str(masterSystem) +"/etcportage /etc/portage/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0") 
  #syncSystemD = os.system("rsync -av rsync://"+ str(masterSystem) +"/etcsystemd /etc/systemd/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  #syncSystemDsys = os.system("rsync -av rsync://"+ str(masterSystem) +"/syssystemd /usr/lib/systemd/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  syncRsyncD = os.system("rsync -av rsync://"+ str(masterSystem) +"/etcrsyncd /etc/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  syncKernels = os.system("rsync -av rsync://"+ str(masterSystem) +"/kernels /etc/kernels |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  syncModules = os.system("rsync -av rsync://"+ str(masterSystem) +"/kernelmodules /lib/modules |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  if(not syncKernels):
    mountf = os.system("mount /boot")
    kernelf = os.system("rsync -av /etc/kernels/boot/ /boot/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
    grubf = os.system("grub2-mkconfig -o /boot/grub/grub.cfg |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
    if(mountf or kernelf or grubf):
      sys.exit(1)
  else:
    sys.exit(1)
  if(syncPortage or syncSets or syncLayman or syncCbOverlay or syncEtcPortage or syncRsyncD or syncKernels or syncModules):
    sys.exit(1)
  emerge = os.system("emerge --exclude sys-apps/baselayout --deep -G @world |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  systemd = os.system("systemctl enable lm_sensors.service lighttpd.service kdm.service acpid.service autofs.service NetworkManager.service NetworkManager-wait-online.service NetworkManager-dispatcher.service nfsd.service ntpd.service rpc-mountd.servicerpc-statd.service rpcbind.service rsyncd.service sensord.service sshd.service syslog-ng.service upower.service vixie-cron.servicexinetd.service |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  cleanup = os.system("rm -frv /etc/NetworkManager/dispatcher.d/50-local |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  if(emerge or systemd or cleanup):
    sys.exit(0)
  else:
      sys.exit(1)
  sys.exit(0)  
  
p = os.popen("cat /etc/os-release","r")
dets = p.readlines()

for x in dets:
  if(re.search('Gentoo$',x)):
    gentooUpdate()
  
  
  
  
  