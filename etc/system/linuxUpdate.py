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
  syncSystemD = os.system("rsync -av rsync://"+ str(masterSystem) +"/etcsystemd /etc/systemd/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  syncSystemDsys = os.system("rsync -av rsync://"+ str(masterSystem) +"/syssystemd /usr/lib/systemd/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  syncRsyncD = os.system("rsync -av rsync://"+ str(masterSystem) +"/etcrsyncd /etc/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  syncKernels = os.system("rsync -av rsync://"+ str(masterSystem) +"/kernels /etc/kernels |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  
  if(not syncKernels):
    os.system("mount /boot")
    os.system("rsync -av /etc/kernels/boot/ /boot/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
    os.system("tar -xvf /etc/kernels/modules -C / |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
    os.system("grub2-mkconfig -o /boot/grub/grub.cfg |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
    
  else:
    sys.exit(1)
  if((not syncPortage) and (not syncSets) and (not syncLayman) and (not syncCbOverlay) and (not syncEtcPortage) and (not syncSystemD) and (not syncSystemDsys) and (not syncRsyncD)):
    emerge = os.system("emerge --exclude sys-apps/baselayout --deep -g @world |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
    if(not emerge):
      sys.exit(0)
    else:
      sys.exit(1)
  else:
    sys.exit(1)
    
  
p = os.popen("cat /etc/os-release","r")
dets = p.readlines()

for x in dets:
  if(re.search('Gentoo$',x)):
    gentooUpdate()
  
  
  
  
  