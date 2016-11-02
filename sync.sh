#!/bin/sh
mkdir -p /dell1-pool/tempprojdump
mount stor1:/dell1-pool/stor2/stor1/prod/projdump /dell1-pool/tempprojdump
mv /dell1-pool/tempprojdump/pythonTestWindoze.DONOTDELETE/rbhus /dell1-pool/tempprojdump/pythonTestWindoze.DONOTDELETE/rbhus.`date +%Y_%B_%A_%d_%H-%M-%S`
rsync -av ./ /dell1-pool/tempprojdump/pythonTestWindoze.DONOTDELETE/rbhus/ --delete --exclude=*.pyc --exclude=.git
cd /dell1-pool/tempprojdump/pythonTestWindoze.DONOTDELETE/rbhus/ ; ./clean.sh ; cd -
chown root:root /dell1-pool/tempprojdump/pythonTestWindoze.DONOTDELETE/rbhus/ -Rv
chmod 755 /dell1-pool/tempprojdump/pythonTestWindoze.DONOTDELETE/rbhus/ -Rv
umount /dell1-pool/tempprojdump


