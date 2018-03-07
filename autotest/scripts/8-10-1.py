import os,time



#dm = os.popen('dmidecode | grep -i product').read()
#print(dm)

#fl1 = open('/home/product.log','w')
#print >>fl1,dm
#fl1.close()

nam1 = os.popen('cat /home/product.log').read()
print(nam1)

nam2 = nam1.find('System')
print(nam2)


if nam2 == -1:
    BMC_ip1 = os.popen('cat /home/bmc_ip.txt').read()
    BMC_ip = BMC_ip1.replace('\n','')
    BMC = 'ipmitool -I lanplus -H '+ BMC_ip + ' -U lenovo -P len0vO'+' bmc info'
    print(BMC)
    #BMC_info command
    BMC_info = os.popen(BMC).read()

    #power off
    poweroff = 'ipmitool -I lanplus -H '+ BMC_ip + ' -U lenovo -P len0vO'+' power off'
    poweroff1 = poweroff +'\n'
    power_off = os.popen(poweroff).read()
    print(power_off)

    print('wait 5 minutes shutdown this machine')

    time.sleep(100)



    poweron = 'ipmitool -I lanplus -H '+ BMC_ip + ' -U lenovo -P len0vO'+' power on'
    poweron1 = poweron +'\n'
    power_on = os.popen(poweron).read()
    print(power_on)

    log = BMC_info  + poweroff1 + power_off + poweron1 + power_on

    f1 = open('/home/8-10.log','w')

    print >>f1,log

    f1.close()
    #time.sleep(300)
    loip1 = os.popen('cat /home/localip.log').read()
    loip2 = loip1.replace('\n','')
    loip3 = loip2.replace(' ','')
    loip4 = 'ping ' + loip3 + ' -c 10'


    while 1:
          ping1 = os.popen(loip4).read()
          ping2 = ping1.find('ttl=')
          print(ping2)
          if ping2 != -1:
             time.sleep(300)
             sc1 = os.system('sh /home/run2.sh')
             sc3 = os.system('expect /home/run3.sh')
             mv1 = os.system('rm -rf /home/8-10.log 8-10.py bmc_ip.txt localip.log product.log run2.sh run3.sh')
             print('pass')
             break
    #sc1 = os.system('sh /home/run2.sh')
else:
    BMC_ip11 = os.popen('cat /home/bmc_ip.txt').read()
    BMC_ip10 = BMC_ip11.replace('\n','')
    BMC10 = 'ipmitool -I lanplus -H '+ BMC_ip10 + ' -U USERID -P PASSW0RD'+' bmc info'
    print(BMC10)
    #BMC_info command
    BMC_info10 = os.popen(BMC10).read()

    #power off
    poweroff10 = 'ipmitool -I lanplus -H '+ BMC_ip10 + ' -U USERID -P PASSW0RD'+' power off'
    poweroff11 = poweroff10 +'\n'
    power_off10 = os.popen(poweroff10).read()
    print(power_off10)

    time.sleep(100)

    print('wait 5 minutes shutdown this machine')

    poweron10 = 'ipmitool -I lanplus -H '+ BMC_ip10 + ' -U USERID -P PASSW0RD'+' power on'
    poweron11 = poweron10 +'\n'
    power_on10 = os.popen(poweron10).read()
    print(power_on10)

    log = BMC_info10 + poweroff11 + power_off10 + poweron11 + power_on10

    f11 = open('/home/8-10.log','w')

    print >>f11,log

    f11.close()
    #time.sleep(300)

    #time.sleep(300)
    loip11 = os.popen('cat /home/localip.log').read()
    loip12 = loip11.replace('\n','')
    loip13 = loip12.replace(' ','')
    loip14 = 'ping ' + loip13 + ' -c 10'


    while 1:
          ping11 = os.popen(loip14).read()
		  fi1 = open('/home/e.log','w')
		  print >>fi1,ping11
		  fi1.close()
          ping12 = ping11.find('ttl=')
          print(ping12)
          if ping12 != -1:
             time.sleep(120)
             sc2 = os.system('sh /home/run2.sh')
             sc4 = os.system('expect /home/run3.sh')
             mv2 = os.system('rm -rf /home/8-10.log 8-10.py bmc_ip.txt localip.log product.log run2.sh run3.sh')
             print('pass')
             break
    #sc1 = os.system('sh /home/run2.sh')

    #sc2 = os.system('sh /home/run2.sh')

    #tran = os.system(''scp xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx)


