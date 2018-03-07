#!/bin/bash

echo -n "Please enter the ISO location:"
read location
cd $location
if [ -f *.iso ];then

  iso=`ls *.iso`

else

  echo "No ISO file found!"
  exit

fi

rm -rf `ls | grep -v $iso` 
#echo "**********"$iso Inbox Driver Information********** >> $iso.txt

mkdir newos
mount -o loop ${location}*.iso newos

ker=`find . -name "kernel-default-[1-9]*.rpm" -o -name "kernel-[1-9]*.rpm"`

echo $ker

rpm2cpio $ker | cpio -di
find lib/ -name *.ko.* > ko.txt
chmod -R 777 lib/

if [ `grep -c "xz" ko.txt` -ne "0" ]; then
  xz -d `find lib/ -name *.ko.xz`
 
fi
  find lib/ -name *.ko > ko.txt

if [ -f ko.txt ]; then
#        echo "**********"$iso Inbox_Driver- Information********** >> $iso.txt
        for ko in $( cat ko.txt | grep ko )
          do
             
             pci=`modinfo $ko | grep 'alias.*pci'`

             if [ -n "$pci" ]; then
              
			   echo "===>ko" >> $iso.txt
	     	   echo $ko >> $iso.txt
#		       echo `modinfo $ko | grep -w "version:"` >> $iso.txt
               echo "===>pciid" >> $iso.txt
	           
               modinfo $ko | grep 'alias.*pci' | while read line
               do(
    
				 id=`echo ${line#*pci:v}`
                 #Vender ID
				 if [ "`echo ${id:0:1}`" == "0" ]; then
					vid=`echo ${id:4:4}`
				 else
					 vid=*
				 fi
                 #Device ID
				 devid=`echo ${id#*d}`
				 if [ "`echo ${devid:0:1}`" == "0" ]; then
					 devid=`echo ${id#*d0000}`
					 devid=`echo ${devid%sv*}`
				 else
					 devid=*
				 fi
				 #SubVender ID
				 subvid=`echo ${id#*sv}`
				 if [ "`echo ${subvid:0:1}`" == "0" ]; then
					 subvid=`echo ${id#*sv0000}`
					 subvid=`echo ${subvid%sd*}`
				 else
					 subvid=*
				 fi

 				 #SubDevice ID
				 subdevid=`echo ${id#*sd}`
				 if [ "`echo ${subdevid:0:1}`" == "0" ]; then
					 subdevid=`echo ${id#*sd0000}`
					 subdevid=`echo ${subdevid%bc*}`
				 else
					 subdevid=*
				 fi

				 echo ${vid}:${devid}::${subvid}:${subdevid} >> ${iso}.txt

              )done

             echo "===>modinfo" >> ${iso}.txt
			 modinfo $ko >> ${iso}.txt
             fi


             echo "===>ko" >> $iso.repo
			 echo $ko >> $iso.repo
             modinfo $ko >> ${iso}.repo

          done 
else
        echo "Error: No input file ko.txt found." | tee -a $iso.txt
        exit
fi

umount newos/
rm -rf `ls | grep -v $iso`

if [[ $iso =~ "RHEL" ]]
then
    osv="RedHat"
	os=`echo $iso | awk -F - '{print $2}'`
else
	osv="SUSE"
	if [[ $iso =~ "SP" ]]
	then
		os=`echo $iso | awk -F - '{print $2$3}'`
		os=`echo ${os//'SP'/'.'}`
	else
		os=`echo $iso | awk -F - '{print $2}'`
	fi
fi
mv $iso.* /home/information/drivers/${osv}/${os}/

python /root/Project/autotest/dbstore/driver.py -d ${osv}/${os}

python /root/Project/autotest/analyze/pciresult.py -i $iso
