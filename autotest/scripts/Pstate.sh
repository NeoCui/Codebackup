#!/bin/bash

logpath=`find /mnt -name log_*`

mkdir ${logpath}/Pstate

echo "Case Pstate: fail" > ${logpath}/Pstate/Pstate.txt

echo "Case Pstate: fail" >> ${logpath}/report.txt
