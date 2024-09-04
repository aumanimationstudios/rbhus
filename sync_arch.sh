#!/bin/bash
mkdir -p /dell2-pool/tempprojdump
mount stor6:/dell2-pool/stor6/stor1/prod/projdump /dell2-pool/tempprojdump
mv /dell2-pool/tempprojdump/pythonTestWindoze.DONOTDELETE/arch/rbhus /dell2-pool/tempprojdump/pythonTestWindoze.DONOTDELETE/arch/rbhus.`date +%Y_%B_%A_%d_%H-%M-%S`
rsync -av ./ /dell2-pool/tempprojdump/pythonTestWindoze.DONOTDELETE/arch/rbhus/ --delete --exclude=*.pyc --exclude=.git
cd /dell2-pool/tempprojdump/pythonTestWindoze.DONOTDELETE/arch/rbhus/ ; ./clean.sh ; cd -
chown root:root /dell2-pool/tempprojdump/pythonTestWindoze.DONOTDELETE/arch/rbhus/ -Rv
chmod 755 /dell2-pool/tempprojdump/pythonTestWindoze.DONOTDELETE/arch/rbhus/ -Rv
umount /dell2-pool/tempprojdump


