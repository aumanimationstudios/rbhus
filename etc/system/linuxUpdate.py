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
  syncPortage = os.system("emerge --sync |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  os.system("echo \"exit status = "+ str(syncPortage) +"\" |& tee -a /tmp/rbhusSystemUpdates")
  syncSets = os.system("rsync -av rsync://"+ str(masterSystem) +"/sets /var/lib/portage/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  os.system("echo \"exit status = "+ str(syncSets) +"\" |& tee -a /tmp/rbhusSystemUpdates")
  syncLayman = os.system("rsync -av rsync://"+ str(masterSystem) +"/layman /var/lib/layman/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  os.system("echo \"exit status = "+ str(syncLayman) +"\" |& tee -a /tmp/rbhusSystemUpdates")
  syncCbOverlay = os.system("rsync -av rsync://"+ str(masterSystem) +"/cb_overlay /usr/local/portage/cb_overlay/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  os.system("echo \"exit status = "+ str(syncCbOverlay) +"\" |& tee -a /tmp/rbhusSystemUpdates")
  syncEtcPortage = os.system("rsync -av rsync://"+ str(masterSystem) +"/etcportage /etc/portage/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0") 
  os.system("echo \"exit status = "+ str(syncEtcPortage) +"\" |& tee -a /tmp/rbhusSystemUpdates")
  #syncSystemD = os.system("rsync -av rsync://"+ str(masterSystem) +"/etcsystemd /etc/systemd/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  #syncSystemDsys = os.system("rsync -av rsync://"+ str(masterSystem) +"/syssystemd /usr/lib/systemd/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  syncRsyncD = os.system("rsync -av rsync://"+ str(masterSystem) +"/etcrsyncd /etc/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  os.system("echo \"exit status = "+ str(syncRsyncD) +"\" |& tee -a /tmp/rbhusSystemUpdates")
  syncKernels = os.system("rsync -av rsync://"+ str(masterSystem) +"/kernels /etc/kernels |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  os.system("echo \"exit status = "+ str(syncKernels) +"\" |& tee -a /tmp/rbhusSystemUpdates")
  syncModules = os.system("rsync -av rsync://"+ str(masterSystem) +"/kernelmodules /lib/modules |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  os.system("echo \"exit status = "+ str(syncModules) +"\" |& tee -a /tmp/rbhusSystemUpdates")
  #if(syncPortage or syncSets or syncLayman or syncCbOverlay or syncEtcPortage or syncRsyncD or syncKernels or syncModules):
    #sys.exit(1)
  
  mountf = os.system("mount /boot")
  kernelf = os.system("rsync -av /etc/kernels/boot/ /boot/ |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  grubf = os.system("grub2-mkconfig -o /boot/grub/grub.cfg |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  systemservices = ['lm_sensors.service', 
                    'lighttpd.service', 
                    'kdm.service', 
                    'acpid.service', 
                    'autofs.service', 
                    'NetworkManager.service', 
                    'NetworkManager-wait-online.service', 
                    'NetworkManager-dispatcher.service', 
                    'nfsd.service', 'ntpd.service', 
                    'rpc-mountd.servicerpc-statd.service', 
                    'rpcbind.service', 'rsyncd.service', 
                    'sensord.service', 
                    'sshd.service', 
                    'syslog-ng.service', 
                    'upower.service', 
                    'vixie-cron.service', 
                    'xinetd.service']
  
  emerge = os.system("emerge --exclude sys-apps/baselayout --deep -GK @world |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
  
  if(not emerge):
    for x in systemservices:
      systemd = os.system("env-update; source /etc/profile; systemctl enable "+ str(x) +" |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
    sensord = os.system("yes | sensors-detect")
    cleanup = os.system("rm -frv /etc/NetworkManager/dispatcher.d/50-local |& tee -a /tmp/rbhusSystemUpdates ; test ${PIPESTATUS[0]} -eq 0")
    sys.exit(0)  
  else:
    sys.exit(1)
  
  
p = os.popen("cat /etc/os-release","r")
dets = p.readlines()

for x in dets:
  if(re.search('Gentoo$',x)):
    gentooUpdate()
  
  
  
  
  