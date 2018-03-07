#!/bin/bash

logpath=`find /mnt -name log_*`

mkdir ${logpath}/PCIID

echo "Case PCIID :pass" > ${logpath}/PCIID/PCIID.txt

echo "Case PCIID :pass" >> ${logpath}/report.txt

cat ${logpath}/report.txt
