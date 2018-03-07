import os,time,subprocess

kernelname = os.popen('uname -a').read()

print(kernelname)

cpuinfo = os.popen('lscpu').read()

print(cpuinfo)

cpuidleinfo = os.popen('cpupower -c all idle-info').read()
print(cpuidleinfo)

for i in range(10):
    if i <10:
       cpumonitor1 = os.system('cpupower monitor >> /home/a2.txt')
       cpumonitor = os.popen('cpupower monitor').read()
       print(cpumonitor)

cpumonitor3 = os.popen('cat /home/a2.txt').read()
cpumonitor4 = 'watch cpupower monitor\n=======================================================================================================================================================================================\n'+ cpumonitor3
cpumonitor2 = str(cpumonitor4)

print(cpumonitor2)
log1 = kernelname + cpuinfo + cpuidleinfo + cpumonitor2

f2 = open('/home/8-7-2.log','w')
print >>f2,log1
f2.close()

path = os.popen('find /boot/ -name grub.cfg').read()
f1 = path.replace('\n','')
file = open(f1,'r')
content = file.read()
file.close()
pos = content.find( "LANG" )
if pos != -1:
    content = content[:pos] + "intel_idle.max_cstate=0 " + content[pos:]
    file = open( f1, "w+" )
    file.write( content )
    file.close()
#remove 8-7-2.py form rc.local

# remove add auto test script
removel = os.popen('find /etc/ -name rc.local | grep -i rc.d').read()
print(removel)
remove5 = removel.replace('\n','')
remove6 = 'cat '+ remove5 
print(remove6)
remove8 = os.popen(remove6).read()
remove2 = remove8.find('python')
remove3 = remove8[:remove2]

remove7 = open(remove5,'w+')
print(remove7)
remove7.write(remove3)
remove7.close()





    

# add boot
rclocal = os.popen('find /etc/ -name rc.local | grep -i rc.d').read()
#print(rclocal)
rclocal5 = rclocal.replace('\n','')
rclocal6 = 'cat '+ rclocal5 
#print(rclocal6)
rclocal1 = os.popen(rclocal6).read()
#print(rclocal1)
rclocal4 = rclocal1 + '\n' + 'python /mnt/scripts/8-7-2-reboot.py\n'
#print(rclocal4)
#type(rclocal4)
#rclocal4 = rclocal1.read()
#print(rclocal4)
#rclocal2 = rclocal1.append( '\\n')
#rclocal3 = rclocal2.append('pyhton 8-2-3-reboot.py')
rclocal2 = open(rclocal5,'w+')
print(rclocal2)
rclocal2.write(rclocal4)
rclocal2.close()
rclocal3 = 'chmod 777 ' + rclocal5
rclocal7 = os.system(rclocal3)
rclocal8 = os.system('reboot')






def reboot1():
    max_cstate = os.popen('cat /sys/module/intel_idle/parameters/max_cstate').read()
    if max_cstate == 0:
       for i in range(10):
            if i <10:
               cpumonitor1 = os.system('cpupower monitor >> /home/a1.txt')
               cpumonitor = os.popen('cpupower monitor').read()
               print(cpumonitor)
    else:
        print('max_csate is not 0,test Fail')
     
    cpumonitor3 = os.popen('cat /home/a.txt').read()
    cpumonitor4 = 'watch cpupower monitor\n=======================================================================================================================================================================================\n'+ cpumonitor3
    cpumonitor2 = str(cpumonitor4)




#import os
#path = os.popen("find /boot/ -name grub.cfg")
#f1=path.read()[:-1]
#file = open(f1, "r" )
#content = file.read()
#file.close()
#pos = content.find( "LANG" )
#if pos != -1:
    
#content = content[:Pos] + "intel_idle.max_cstate=0 " + content[pos:]
#file = open( f1, "w+" )
#file.write( content )
#file.close()

