#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import sys
import os
import re
import time
import argparse

fileDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
baseDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-4])

sys.path.append(baseDir)

import rbhus.utilsPipe
import rbhus.debug
import rbhus.constantsPipe
import rbhus.dbPipe

#TODO: Implement below code
#rsync -av -f"+ */" -f"- *" "AndePirki_se01_ep005_missingEgg" "bluepixels@stor6:/dell2-pool/stor6/test_backup_recovery/"

parser = argparse.ArgumentParser()
parser.add_argument("-a","--all",dest='all',action="store_true")
parser.add_argument("-d","--dryrun",dest='dryrun',action="store_true",help="do a test run without actually backing up anything")
parser.add_argument("-p","--projects",dest='projects',help="comma seperated list of projects to backup")
args = parser.parse_args()


def sortKey(value):
    try:
        return(float(value.split(os.sep)[-1]))
    except:
        print("wtf")
        return(0.0)

def getTimeSortedDirs(dirPath):
    try:
        all_subdirs = [os.path.join(dirPath,x) for x in os.listdir(dirPath) if(os.path.isdir(os.path.join(dirPath,x)))]
        print(all_subdirs)

        if(all_subdirs):
            latest_subdir = sorted(all_subdirs, key=sortKey, reverse=True)
            return(latest_subdir)
        else:
            return(False)
    except:
        print(str(sys.exc_info()))


try:
    allProj = []
    if(args.projects):
        print(args.projects)
        projects = args.projects.split(",")
        for p in projects:
            projDet = rbhus.utilsPipe.getProjDetails(p.strip())
            if(projDet):
                allProj.append(projDet)
            else:
                print("bad project name : "+ str(p))
    else:
        projects = ['ep001_beautyAndTheFeast', 'ep002_eggUntouchable', 'ep003_haveAbite', 'ep004_logIn', 'ep005_chickenHunt', 'pipeTest1', 'pipeTest5', 'short001_andeCrabBite', 'short002_pirkiEggChase', 'short004_andepirkiCowboy', 'study_ap_chickenHunt', 'study_ap_lightLayout', 'test_ap_2021', 'test_ap_HideAndSeek', 'test_ap_candyThief', 'test_ap_getTheDart', 'test_ap_hatAttack', 'test_ap_hypnocity', 'test_ap_rightBrothers', 'test_ap_shot_TheNextDay']
        for p in projects:
            projDet = rbhus.utilsPipe.getProjDetails(p.strip())
            if(projDet):
                allProj.append(projDet)
            else:
                print("bad project name : "+ str(p))
    print(allProj)
    for proj in allProj:
        print(proj['projName'])
        
        createProjDirCmd = "rsync -av -f\"+ */\" -f\"- *\" \"kryptos@stor2:/dell1-pool/stor2/{0}\" \"/blueprod/STOR2/stor2/\"".format(proj['projName'])
        print(createProjDirCmd)
        os.system(createProjDirCmd)

        allAssets = rbhus.utilsPipe.getProjAsses(proj['projName'])
        if(allAssets):
            for x in allAssets:
                dirMapDets = rbhus.utilsPipe.getDirMapsDetails(x['backupDir'])
                # print(dirMapDets)
                pathSrcBackup = rbhus.utilsPipe.getAbsPath(x['path']).rstrip(os.sep) + os.sep
                print(pathSrcBackup)
                # pathDestBackup = os.path.join(dirMapDets['linuxMapping'],x['projName'],x['assetId'],str(time.time())).rstrip(os.sep) + os.sep
                # print(pathDestBackup)

                # dirMapDets = rbhus.utilsPipe.getDirMapsDetails(x['backupDir'])
                # print(dirMapDets)

                pathDestBackupBase = os.path.join(dirMapDets['linuxMapping'],x['projName'],x['assetId'])
                print(pathDestBackupBase)
                
                sortedPaths = getTimeSortedDirs(pathDestBackupBase)
                if(sortedPaths):
                    print(sortedPaths[0])
                
                    cmdFinal = "rsync -avzHXWhPs "+ sortedPaths[0] +os.sep+"* "+ pathSrcBackup
                    print(cmdFinal)
                    try:
                        os.system(cmdFinal)
                    except:
                        print(str(sys.exc_info()))
except:
    print(str(sys.exc_info()))
