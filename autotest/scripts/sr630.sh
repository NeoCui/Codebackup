#!/bin/bash

sh /mnt/scripts/PCIID.sh

#sh /mnt/scripts/Pstate.sh

sh /mnt/scripts/CDN.sh

python 8.6.1.py > /mnt/8.6.1.log

python 8.6.2.py > /mnt/8.6.2.log
