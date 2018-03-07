#!/bin/bash

echo -n "Please enter the kernel location:"
read location

cd $location

#if [ -f linux-*.tar.xz ];then
#
#  sourceXZ=`ls linux-*.tar.xz`
#  xz -d ${sourceXZ}
#  sourceTAR=`ls linux-*.tar`
#  tar xvf ${sourceTAR}
#
#else
#
#  echo "No kernel source package file found!"
#  exit
#
#fi



if [ -f kernel-[1-9]*.rpm ];then

  ker=`ls kernel-[1-9]*.rpm`

else

  echo "No kernel package file found!"
  exit

fi

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
              
	           echo "===>ko" >> $ker.txt
	     	   echo $ko >> $ker.txt
#		       echo `modinfo $ko | grep -w "version:"` >> $ker.txt
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

				 echo ${vid}:${devid}::${subvid}:${subdevid} >> ${ker}.txt

              )done

             echo "===>modinfo" >> ${ker}.txt
			 modinfo $ko >> ${ker}.txt
             fi


             echo "===>ko" >> $ker.repo
			 echo $ko >> $ker.repo
             modinfo $ko >> ${ker}.repo

          done 
else
        echo "Error: No input file ko.txt found." | tee -a $ker.txt
        exit
fi


rm -rf `ls | grep -v $ker`
