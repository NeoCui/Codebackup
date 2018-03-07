#!/bin/bash

logpath=`find /mnt -name log_*`

mkdir ${logpath}/CDN

echo "Case CDN :pass" > ${logpath}/CDN/CDN.txt

echo "Case CDN :pass" >> ${logpath}/report.txt

