#!/usr/bin/python

import sys
import os
import subprocess
import argparse
import glob

rsync = "/usr/bin/rsync"
parser = argparse.ArgumentParser(description='Make a system clone',fromfile_prefix_chars='@')
if(len(sys.argv) == 1):
  parser.print_help()
  sys.exit(1)

parser.add_argument("-r","--root",dest='rootDir',help='root dir to clone')
parser.add_argument("-t","--target",dest='target',help='target dir for the cloned system')
parser.add_argument("-b","--mountboot",dest='mb',action='store_true',help='mount the boot partion : y/n')
parser.add_argument("-x","--exclude",dest='exclude',help='list of comma seperated files/directories to exclude')
parser.add_argument("-l","--makelink",dest='makeLink',help='make links - comma seperated list with colon as a delimiter for linkTarget:linkName')
parser.add_argument("-m","--makedir",dest='makeDir',help='comma seperated list of directories:owner%perm to make with colon and % as a delimiter for dirName:owner%perm')
parser.add_argument("-e","--emptytree",dest='emptyTree',help='comma seperated list of directories to empty all files leaving the tree structure intact')
parser.add_argument("-n","--srchost",dest="srchost",help='src host')
parser.add_argument("-p","--protocol",dest="prot",help='use rsh or ssh as the backend transport protocol')
args = parser.parse_args()

root_dir = os.path.abspath(str(args.rootDir))
target = os.path.abspath(str(args.target))


print("root       : "+ str(args.rootDir))
print("target     : "+ str(args.target))
print("exclude    : "+ str(args.exclude))
print("makeLink   : "+ str(args.makeLink))
print("makeDir    : "+ str(args.makeDir))
print("mountboot  : "+ str(args.mb))


make_dirs = {}
link_dict = {}
make_dirs_perms = {}

if(args.exclude):
  xclude = [os.path.join(root_dir,str(x).lstrip("/").rstrip("/")) for x in str(args.exclude).split(",")]
  xclude_option = "--exclude="+" --exclude=".join(xclude)
else:
  xclude_option = ""



if(args.makeDir):
  pass1 = args.makeDir.split(",")
  for x in pass1:
    make_dirs[os.path.join(target,str(x.split(":")[0]).lstrip("/").rstrip("/"))] =  x.split(":")[1].split("%")[0]
    try:
      make_dirs_perms[os.path.join(target,str(x.split(":")[0]).lstrip("/").rstrip("/"))] = x.split(":")[1].split("%")[1]
    except:
      print(os.path.join(target,str(x.split(":")[0]).lstrip("/").rstrip("/")) +" : perm not defined")

if(args.makeLink):
  pass1 = args.makeLink.split(",")
  for x in pass1:
    link_dict[x.split(":")[0]] = os.path.join(target,x.split(":")[1].lstrip("/"))
  
  
if(args.srchost):
  root_dir_h = args.srchost.rstrip().lstrip() +":"+ root_dir
else:
  root_dir_h = root_dir
  
if(args.prot):
  p = "--rsh="+ args.prot.rstrip().lstrip()
else:
  p = "--rsh=rsh"

os.system(rsync +" -avHAX "+ root_dir_h +" "+ target +" "+ xclude_option +" "+ p)


if(args.makeDir):
  for x in make_dirs:
    os.system("mkdir -vp "+ x)
    os.system("chown "+ make_dirs[x] +":"+ make_dirs[x] +" "+ x)
  if(make_dirs_perms):
    for x in make_dirs_perms:
      os.system("chmod "+ make_dirs_perms[x]+" "+ x)
    
    
if(link_dict):
  for x in link_dict:
    os.system("ln -vs "+ x +" "+ link_dict[x])

    
if(args.emptyTree):
  for x in args.emptyTree.split(","):
    mptyDir = os.path.join(target,x.rstrip("/").lstrip("/"))
    print("to delete : "+ str(mptyDir))
    tree1 = subprocess.check_output(["tree","-aif","--noreport",mptyDir,"|","gawk","-F","'->'","'{print $1}'"]).split("\n")
    for y in tree1:
      if(os.path.isfile(y)):
        os.system("rm -fv "+ y)
 
    
    
    
    
    
    
    