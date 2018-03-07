#!/usr/bin/expect
#============================================
#function-->Tar_etc zip etc/*.conf
#============================================
#Tar_etc()
#{
#    tar jcvf /tmp/test.tar.bz2 /etc/*.conf  &> /dev/null
#    if [ $? -eq 0 ]
#    then
#       echo "zip ok"
#    else
#       echo "zip fail"
#    fi
#}

#======================================
#function-->Scp_ip Copy to every machine



set time 60
spawn ssh  -o "StrictHostKeyChecking no" root@
expect "*assword"
send "111111\n"
expect "*$*"
send "python /mnt/scripts/8-10-2.py\n"
expect "*assword"
send "111111\n"              



