#!/bin/sh
mkdir -p /mnt/tempprojdump
mount stor1:/mnt/stor2/stor1/prod/projdump /mnt/tempprojdump

rsync -av ./ /mnt/tempprojdump/pythonTestWindoze.DONOTDELETE/rbhus/ --delete --exclude=*.pyc --exclude=.git
cd /mnt/tempprojdump/pythonTestWindoze.DONOTDELETE/rbhus/ ; ./clean.sh ; cd -
chown root:root /mnt/tempprojdump/pythonTestWindoze.DONOTDELETE/rbhus/ -Rv
chmod 755 /mnt/tempprojdump/pythonTestWindoze.DONOTDELETE/rbhus/ -Rv
umount /mnt/tempprojdump


