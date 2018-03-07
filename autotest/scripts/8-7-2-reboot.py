import os,time


max_cstate1 = os.popen('cat /sys/module/intel_idle/parameters/max_cstate').read()
max_cstate2 = max_cstate1.replace('\n','')
max_cstate = int(max_cstate2)
print(max_cstate)
if max_cstate == 0:
   for i in range(10):
        if i <10:
           cpumonitor1 = os.system('cpupower monitor >> /home/a3.txt')
           cpumonitor = os.popen('cpupower monitor').read()
           print(cpumonitor)
else:
    print('max_csate is not 0,test Fail')
#command1 = os.system('echo cat/sys/module/intel_idle/parameters/max_cstate >a1.txt')
 
cpumonitor3 = os.popen('cat /home/a3.txt').read()
cpumonitor4 = 'cat/sys/module/intel_idle/parameters/max_cstate\n'+'0\n'+'watch cpupower monitor\n=======================================================================================================================================================================================\n'+ cpumonitor3
cpumonitor2 = str(cpumonitor4)
log1 = cpumonitor2
f2 = open('/home/8-7-2-1.log','w')

print >>f2,log1
f2.close()




# open 8-7-1-log file and check status
clog = os.popen('cat /home/8-7-1.log').read()

print(clog)

flog = clog.find('Idle_Stats')
flog1 = bool(flog)
print(flog1)




# open 8-7-2-1-log file and check status
clog21 = os.popen('cat /home/8-7-2-1.log').read()

print(clog21)

flog22 = clog21.find('Idle_Stats')

print(flog22)
#flog23 = bool(flog)
#print(flog23)



if flog1 == True:
   if flog22 == -1:
	  a1 = '8-7-PASS'
	  b1 = '8-7-Fail'
	  f2 = open('/home/8-7.log','w')
	  print >>f2,a1
	  f2.close()
      #print('PASS')
   else:
      f3 = open('/home/8-7.log','w')
      print >>f3,b1
      f3.close()
      #print('Fail')
else:
   c1 = '8-7-Fail'
   f4 = open('/home/8-7.log','w')
   print >>f4,c1
   f4.close()
   #print('Fail')






# remove add auto test script
rclocal = os.popen('find /etc/ -name rc.local | grep -i rc.d').read()
print(rclocal)
rclocal5 = rclocal.replace('\n','')
rclocal6 = 'cat '+ rclocal5 
print(rclocal6)
rclocal8 = os.popen(rclocal6).read()
rclocal2 = rclocal8.find('python')
rclocal3 = rclocal8[:rclocal2]

rclocal7 = open(rclocal5,'w+')
print(rclocal7)
rclocal7.write(rclocal3)
rclocal7.close()


# remove parameter form gurb.cfg
grub1 = os.popen('find /boot/ -name grub.cfg').read()
grub2 = grub1.replace('\n','')
print(grub2)
grub = open(grub2,'r')
content = grub.read()
grub.close()
local = content.find('intel_idle.max_cstate=0')
local1 = content.find('LANG')
if local != -1:
    content = content[:local] + content[local1:]
    #global grub2
    grub = open(grub2,'w+')
    print(grub)
    grub.write(content)
    grub.close()





# create log directory
fd1 = os.popen('find /mnt/  -name log_*').read()
print(fd1)


fd2 = fd1.replace('\n','')

delfd3 = os.popen('find /mnt -name c-state-8-7').read()
print(delfd3)
delfd4 = bool(delfd3)
print(delfd4)

if delfd4 == False:
     fd5 = 'mkdir ' + fd2 +'/'+ 'c-state-8-7'
     print(fd5)
     fd8 = os.system(fd5)

else:
     fd6 = 'rm -rf ' + fd2 +'/'+ 'c-state-8-7'
     fd7 = os.system(fd6)
     fd9 = 'mkdir ' + fd2 +'/'+ 'c-state-8-7'
     print(fd9)
     fd10 = os.system(fd9)



#fd3 = 'mkdir ' + fd2 +'/'+ 'c-state-8-7'

#print(fd3)

#fd4 = os.system(fd3)
fd20 = str(fd2)
# move log to /mnt/log****
mv1 = 'cp /home/8-7-1.log ' + fd20 +'/c-state-8-7/' + 'c-state-8-7-1.log'
print(mv1)

type(mv1)

mv2 = os.system(mv1)



mv3 = 'cp /home/8-7-2.log ' + fd20 +'/'+ 'c-state-8-7' +'/' + 'c-state-8-7-2.log'
print(mv3)

mv4 = os.system(mv3)


mv5 = 'cp /home/8-7-2-1.log ' + fd20 +'/'+ 'c-state-8-7' +'/' + 'c-state-8-7-2-1.log'
print(mv5)

mv6 = os.system(mv5)

fil0 = os.popen('cat /home/8-7.log').read()
fil1 = open('/mnt/report.txt','a')

print >>fil1,fil0

fil1.close()

#remov1 = os.system('rm -rf')

