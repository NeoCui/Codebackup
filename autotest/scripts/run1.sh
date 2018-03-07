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
spawn ssh  -o "StrictHostKeyChecking no" root@192.168.5.1
expect "*assword"
send "111111\n"
expect "*$*"
send "python /home/8-10-1.py\n"
expect "*assword"
send "111111\n"              
