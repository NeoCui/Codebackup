#!/usr/bin/env python
import os,re,time,shutil
def Chk_RetCode (Commands):
    ret=os.system(Commands)
    ret=int(ret)>>8
    if ret <> 0:
        print "Error: %s    Execution failed, Error code %s" %(Commands,ret)
        val = '8.15.2: fail Execution Commands error'
        f5 = open('/mnt/report.txt','a')
        print >>f5,val
        f5.close()
        exit (1)
os.chdir("/mnt/scripts/lnvgy_utl_onecli_tcli04q-1.1.0_rhel7_x86-64")
Chk_RetCode ("chmod 777 *")
Chk_RetCode ("./OneCli config set SystemOobCustom.MemoryRasTest enable --override")
os.chdir("/mnt/scripts")
Chk_RetCode ("chmod 777 *")
#Chk_RetCode ("./Init.sh")
os.system("./Init.sh")
Chk_RetCode ("./einj_mem_uc > /mnt/1.txt")
fp = open('/mnt/1.txt', "r")
while 1:
    line = fp.readline()
    if not line:
        break
    if "paddr = " in line:
        index = line.find("paddr = ")
        Info = line                                                                                                                     
index = index + len("paddr = ")                                                                                                            
num = Info[index:index+6]                                                                                                                  
print (Info[index:index+6])                                                                                                                
Chk_RetCode ('dmesg | grep -i "%s"'%(num))
Chk_RetCode ("dmesg | grep -i 'mce'")
Chk_RetCode ("mcelog --client")
Path=os.popen('ls /mnt/ | grep ^log_')
log_path='/mnt/'+Path.read().split('\n')[0]+'/'
log_file='/mnt/8.15.2.log'
print (log_path)
shutil.copy (log_file,log_path)
fp1 = open('/mnt/8.15.2.log', "r")
Info=None
while 1:
    line = fp1.readline()
    if not line:
        break
    if "ADDR " in line:
        index = line.find("ADDR ")
        Info = line

if Info is None:
    val = '8.15.2: fail No ADDR has been found'
    f5 = open('/mnt/report.txt','a')
    print >>f5,val
    Path=os.popen('ls /mnt/ | grep ^log_')
    log_path='/mnt/'+Path.read().split('\n')[0]+'/'
    log_file='/mnt/8.15.2.log'
    print (log_path)
    shutil.copy (log_file,log_path)
    exit (2)

index = index + len("ADDR ")
num1 = Info[index:index+10]
#print (Info[index:index+10])
fp2 = os.popen("cat /mnt/8.15.2.log").read()
val1 = fp2.count('%s'%(num1))
#print "Val1 is %s" %val1
if val1 ==1:
        val = '8.15.2: pass'
        f5 = open('/mnt/report.txt','a')
        print >>f5,val
        f5.close()
else:
        val = '8.15.2: fail'
        f5 = open('/mnt/report.txt','a')
        print >>f5,val
        f5.close()

os.system("rm -f /mnt/8.15.2.log")
