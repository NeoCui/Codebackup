#!/bin/bash
#!/usr/bin/expect

product=`dmidecode | grep Product`

host=`hostname`

echo $product > product

if [ `grep -i -c "ST550" product` -eq '1' ];then
  mach=`echo st550`
elif [ `grep -i -c "SR630" product` -eq '1' ];then
  mach=`echo sr630`

elif [ `grep -i -c "SR550" product` -eq '1' ];then
  mach=`echo sr550`

elif [ `grep -i -c "SR590" product` -eq '1' ];then
  mach=`echo sr590`

elif [ `grep -i -c "x3650 M5" product` -eq '1' ];then
  mach=`echo  x3650m5`

elif [ `grep -i -c "x3550 M5" product` -eq '1' ];then
  mach=`echo  x3550m5`

fi

function sos()
{
{
 /usr/bin/expect << EOF
 set timeout 300 
 spawn sosreport -a
 expect {
  "Press ENTER to continue, or CTRL-C to*"
    { send "ENTER\r";exp_continue }
  "Please enter your first initial and last na*"
   { send "$os\r";exp_continue }
  "Please enter the case id that you are generatin*"
  { send "$mach\r " }
 }
 expect eof
EOF
}
}
mkdir /var/log/logcheck
if [ -e /etc/redhat-release ];then
    sleep 60 
    os=RedHat_`cat /etc/redhat-release | awk '{print $7}'`  
    

    sos
    cp `find /var/ -name "sosreport-*.tar.xz"` /var/log/logcheck/
    image=`egrep "*.iso" /etc/rc.d/rc.local`
	echo ${image###} >> /mnt/OS_image
	cp /tmp/rc.local /etc/rc.d/rc.local
else
  os=SUSE_`lsb-release -r | awk '{print $2}'`

  supportconfig 
  

  cp `find /var/log/ -name "*$hostname*.tbz"` /var/log/logcheck/

   dmesg > /var/log/dmesg
   image=`egrep "*.iso" /etc/rc.d/boot.local`
   echo ${image###} >> /mnt/OS_image
   cp /tmp/boot.local /etc/rc.d/boot.local

fi

cp /var/log/messages /var/log/logcheck/
cp /var/log/dmesg /var/log/logcheck/

mkdir /mnt/log_`date +%Y%m%d%H%M%S`_`echo $mach`_$os

logname=`find /mnt/ -name log_*`/
chmod -R 777 $logname

cp -prvf /var/log/logcheck $logname

sh /mnt/scripts/${mach}.sh

sh /mnt/scripts/scp_cli.sh
