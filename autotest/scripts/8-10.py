import  time,os

#ipmitool = commands.getoutput('rpm -qa ipmi')
#ipmitoolpackage = 

#if ipmitool == False:
#    install = "rpm -qa" + ipmitollpackage
#    install = os.system(install)
ipa = os.popen('ipmitool lan print | grep -i IP | grep -i Address | grep -i 10').read()
#delete \n and space
ipb = ipa.replace(' ','')
ipc = ipb.replace('\n','')
ip = ipc[10::]
#ouput file and return ip address to server
f = open('/bmc_ip.txt','w')

print >>f,ip
f.close()


#machine name
dm = os.popen('dmidecode | grep -i product').read()
print(dm)

fl1 = open('/home/product.log','w')
print >>fl1,dm
fl1.close()

# local ip address


osip1 = os.popen('ifconfig | grep -i inet | grep -i \'192.168.5\'').read()

print(osip1)
osip2 = osip1.replace(' ','')

print(osip2)
osip3  = osip2.find('inet')
osip5 = osip3 + 4
osip6 = osip2.find('netmask')
osip4 = osip2[osip5:osip6]

f21 = open('/home/localip.log','w')
print >>f21,osip4

f21.close()

chrun = os.popen('cat /mnt/scripts/run2.sh').read()
chrun1 = chrun.find('@')
print(chrun1)
chrun5 = chrun1 + 1
chrun2 = chrun[:chrun5] + osip4 + chrun[chrun5:]

print(chrun2)

chrun6 = open('/mnt/scripts/run2.sh','w')

print >>chrun6,chrun2

chrun6.close()




chrun10 = os.popen('cat /mnt/scripts/run3.sh').read()
chrun11 = chrun10.find('@')
print(chrun11)
chrun15 = chrun11 + 1
chrun12 = chrun10[:chrun15] + osip4 + chrun10[chrun15:]

print(chrun12)

chrun16 = open('/mnt/scripts/run3.sh','w')

print >>chrun16,chrun12

chrun16.close()




#bmc_ip.txt transfer to server home

transfer = ('#!/bin/bash\n#!/usr/bin/expect\nScp_ip()\n{\n /usr/bin/expect << EOF\nset time 60 \nspawn scp -r /bmc_ip.txt root@192.168.5.1:/home\nexpect {\n"*yes/no*"\n {send "yes\\r";exp_continue }\n"*assword:"\n{send "111111\\r"}\n{send "\\r"}\n}\nexpect eof\nEOF\n} \n Scp_ip\n')

print(transfer)

transfer1 = os.system(transfer)
    
#else:


transfer2 = ('#!/bin/bash\n#!/usr/bin/expect\nScp_ip()\n{\n /usr/bin/expect << EOF\nset time 60 \nspawn scp -r /mnt/scripts/8-10-1.py root@192.168.5.1:/home\nexpect {\n"*yes/no*"\n {send "yes\\r";exp_continue }\n"*assword:"\n{send "111111\\r"}\n{send "\\r"}\n}\nexpect eof\nEOF\n} \n Scp_ip\n')

print(transfer2)

transfer3 = os.system(transfer2)




transfer4 = ('#!/bin/bash\n#!/usr/bin/expect\nScp_ip()\n{\n /usr/bin/expect << EOF\nset time 60 \nspawn scp -r /home/product.log root@192.168.5.1:/home\nexpect {\n"*yes/no*"\n {send "yes\\r";exp_continue }\n"*assword:"\n{send "111111\\r"}\n{send "\\r"}\n}\nexpect eof\nEOF\n} \n Scp_ip\n')

print(transfer4)

transfer5 = os.system(transfer4)




transfer6 = ('#!/bin/bash\n#!/usr/bin/expect\nScp_ip()\n{\n /usr/bin/expect << EOF\nset time 60 \nspawn scp -r /home/localip.log root@192.168.5.1:/home\nexpect {\n"*yes/no*"\n {send "yes\\r";exp_continue }\n"*assword:"\n{send "111111\\r"}\n{send "\\r"}\n}\nexpect eof\nEOF\n} \n Scp_ip\n')

print(transfer6)

transfer7 = os.system(transfer6)



transfer8 = ('#!/bin/bash\n#!/usr/bin/expect\nScp_ip()\n{\n /usr/bin/expect << EOF\nset time 60 \nspawn scp -r /mnt/scripts/run2.sh root@192.168.5.1:/home\nexpect {\n"*yes/no*"\n {send "yes\\r";exp_continue }\n"*assword:"\n{send "111111\\r"}\n{send "\\r"}\n}\nexpect eof\nEOF\n} \n Scp_ip\n')

print(transfer8)

transfer9 = os.system(transfer8)


transfer10 = ('#!/bin/bash\n#!/usr/bin/expect\nScp_ip()\n{\n /usr/bin/expect << EOF\nset time 60 \nspawn scp -r /mnt/scripts/run3.sh root@192.168.5.1:/home\nexpect {\n"*yes/no*"\n {send "yes\\r";exp_continue }\n"*assword:"\n{send "111111\\r"}\n{send "\\r"}\n}\nexpect eof\nEOF\n} \n Scp_ip\n')

print(transfer10)

transfer11 = os.system(transfer10)




   
run1 = os.system('expect /mnt/scripts/run1.sh')
