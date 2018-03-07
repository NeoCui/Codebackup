#!/bin/bash
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
#=========================================
sed -i '/192.168.5.*/d' /root/.ssh/known_hosts

#function-->Nmap_ip search test machine
Nmap_ip()
{
    [ -f ip.txt ]
    if [ $? -eq 0 ]
    then
        cat /dev/null > ip.txt
    else
        touch ip.txt
    fi
  nmap -n -sP 192.168.5.10-100 | grep 192.168.5 | awk '{print $5}' > ip.txt
}

#======================================
#function-->Scp_ip Copy to every machine
Scp_ip()
{
cat ip.txt | while read line
do
(
  /usr/bin/expect << EOF
  set time 60
  spawn scp -r /home/scp/scp_cli.sh root@$line:/home/
  expect {
        "*yes/no*"
          { send "yes\r";exp_continue }
        "*assword:"
          { send "111111\r" }
	  { send "\r" }
   }
   expect eof
EOF
) &> /dev/null
   if [ $? -eq 0 ]
   then
       echo "Copy to $line Success"
   else
       echo "Copy to $line Fail"
   fi
done
}
 

#Tar_etc

Nmap_ip

if [ -z `cat ip.txt` ] 
then 
  echo "No client"
  exit
else
  Scp_ip
  
  echo "" > /etc/salt/roster
  cat ip.txt | while read line
  do
  (
    echo "" >> /etc/salt/roster
    echo "web$line:" >> /etc/salt/roster 
    echo "    host: $line" >> /etc/salt/roster
    echo "    user: root" >> /etc/salt/roster
    echo "    password: 111111" >> /etc/salt/roster
    echo "    port: 22" >> /etc/salt/roster
  )
  done

fi
