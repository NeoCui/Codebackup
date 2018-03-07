#coding=utf-8


import os,time




# create log directory
fd1 = os.popen('find /mnt/  -name log_*').read()
print(fd1)


fd2 = fd1.replace('\n','')

delfd3 = os.popen('find /mnt -name BMC-8-10').read()
print(delfd3)
delfd4 = bool(delfd3)
print(delfd4)

if delfd4 == False:
     fd5 = 'mkdir ' + fd2 +'/'+ 'BMC-8-10'
     print(fd5)
     fd8 = os.system(fd5)

else:
     fd6 = 'rm -rf ' + fd2 +'/'+ 'BMC-8-10'
     fd7 = os.system(fd6)
     fd9 = 'mkdir ' + fd2 +'/'+ 'BMC-8-10'
     print(fd9)
     fd10 = os.system(fd9)



fd20 = str(fd2)
# move log to /mnt/log****
mv1 = 'cp /home/8-10.log ' + fd20 +'/BMC-8-10/' + 'BMC-8-10.log'
print(mv1)

mv2 = os.system(mv1)
                      
