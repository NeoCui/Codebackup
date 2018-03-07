
#n-->Tar_etc zip etc/*.conf
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
Scp_ip()
{
  /usr/bin/expect << EOF
  set time 60

  spawn scp -r /home/8-10.log root@:/home
  expect {
        "*yes/no*"
          { send "yes\r";exp_continue }
        "*assword:"
          { send "111111\r" }
          { send "\r" }
   }
   expect eof
EOF
}
Scp_ip







