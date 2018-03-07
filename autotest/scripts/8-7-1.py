import os,time,subprocess

kernelname = os.popen('uname -a').read()

print(kernelname)

cpuinfo = os.popen('lscpu').read()

print(cpuinfo)

cpuidleinfo = os.popen('cpupower -c all idle-info').read()
print(cpuidleinfo)
#cpumonitor1 = 'timeout 10 watch -n 1 cpupower monitor;exit'
#os.system('timeout 10 watch -n 1 cpupower monitor | tee -a /home/a.txt')
for i in range(10):
    if i <10:
       cpumonitor1 = os.system('cpupower monitor >> /home/a.txt')
       cpumonitor = os.popen('cpupower monitor').read()
       print(cpumonitor)

cpumonitor3 = os.popen('cat /home/a.txt').read()
cpumonitor4 = 'watch cpupower monitor\n=======================================================================================================================================================================================\n'+ cpumonitor3
cpumonitor2 = str(cpumonitor4)


#if os.popen('watch -n 1 cpupower monitor').read() == True:
#   killwatch()
print(cpumonitor2)
#cpumonitor = os.popen('cat /home/cpupower.txt').read()
#print(cpumonitor)
#break
#def killwatch():
#    watch1 = os.popen('ps -a | grep -i watch').read()
#    watch2 = watch1[1:5]
#    print(watch2)
#    kill2 = 'kill -SIGINT' + watch2
#    time.sleep(10)

#kill1 = os.system(kill2)
#quit1 = os.popen('ctrl + c').read()
log = kernelname + cpuinfo + cpuidleinfo + cpumonitor2

f1 = open('/home/8-7-1.log','w')

print >>f1,log
f1.close()


# add boot
rclocal = os.popen('find /etc/ -name rc.local | grep -i rc.d').read()
#print(rclocal)
rclocal5 = rclocal.replace('\n','')
rclocal6 = 'cat '+ rclocal5 
#print(rclocal6)
rclocal1 = os.popen(rclocal6).read()
#print(rclocal1)
rclocal4 = rclocal1 + '\n' + 'python /mnt/scripts/8-7-2.py\n'
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



