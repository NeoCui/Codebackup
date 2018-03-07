import os,time
#change grub file add intel_iommu=on
grub1 = os.popen('find /boot/ -name grub.cfg').read()
grub2 = grub1.replace('\n','')
print(grub2)
grub = open(grub2,'r')
content = grub.read()
grub.close()
local = content.find('LANG')
if local != -1:
    content = content[:local] + 'intel_iommu=on ' + content[local:]
    #global grub2
    grub = open(grub2,'w+')
    print(grub)
    grub.write(content)
    grub.close()
rclocal = os.popen('find /etc/ -name rc.local | grep -i rc.d').read()
#print(rclocal)
rclocal5 = rclocal.replace('\n','')
rclocal6 = 'cat '+ rclocal5 
#print(rclocal6)
rclocal1 = os.popen(rclocal6).read()
#print(rclocal1)
rclocal4 = rclocal1 + '\n' + 'python /mnt/scripts/8-2-3-reboot.py\n'
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
def test():
        id1 = os.popen('lspci | grep -i ethernet | awk \'{print $1}\'')#print all pci id
        #print(id1)


        for i in id1:#acquire module name
                    #print(i)
                    i = i.replace('\n','')
                    vol2 = 'lspci -s  ' + i + ' -vvv | grep -i \'SR-IOV\''#acquire first SRIOV
                    print(vol2)
                    vol3 = os.popen(vol2).read()
                    print(vol3)
                    print(vol3.find('SR-IOV'))
                    if vol3.find('SR-IOV') != -1:
                           print('pass')
                           global vol5
                           vol5 = i
                           global name6
                           #id1 = os.popen('lspci | grep -i ethernet').read()
                           id2 = vol5[:7]
                           id3 = 'lspci -ks '+id2
                           name1 = os.popen(id3).read()
                           name2 = name1.find('Kernel modules')
                           name3 = int(name2)
                           name4 = name3 + 16
                           name5 = name1[name4:]
                           name6 = name5.replace('\n','')#acquire device module name
                           print(name6)
                           break
                        


        #id1 = os.popen('lscpi | grep -i ethernet | awk \'{print $1}\'')
        #print(id1)

        num0 = 'find /sys/ -name sriov_totalvfs | grep -i ' + vol5 
        num7 = vol5[:5]
        num5 = 'find /sys/ -name sriov_totalvfs | grep -i '+ num7 + ' |wc -l'
        num6 = os.popen(num5).read()
        num7 = num6.replace('\n','')
        num8 = int(num7)
        print(num8)
        num1 = os.popen(num0).read()#acquire max_vfs number
        hang = num1.find('\n')
        num2 = num1[:hang]
        print(num1)
        num3 = 'cat ' + num2
        vol1 = os.popen(num3).read()
        vol = vol1.replace('\n','')
        print(vol)
        vol2 = int(vol)
        print(vol2)

        if vol !=0:
            remove1 = 'modprobe -r ' + name6 #remove module
            removemodule = os.system(remove1)
            vfs1 = 'modprobe ' + name6 + ' max_vfs='+ vol#
            vfs = os.system(vfs1)

        virtual = os.popen('lspci | grep -i virtual').read()#check virtual network number
        virtualnum = virtual.count('Virtual')
        #virtualnum = virtualnum1.replace('\n','')
        print(virtualnum)

        module1 = 'modprobe -r ' + name6
        module2 = 'modprobe ' + name6
        print(vol2,num8)
        if  vol2 * num8 == virtualnum:
            log = 'Pass'
            f3 = open('8-2-3.log','w')
            print >>f3,log
            f3.close()
            module3 = os.system(module1)
            module4 = os.system(module2)
        else:
            log1 = 'Fail'
            f2 = open('8-2-3.log','w')
            print >>f2,log1
            f2.close()
            module5 = os.system(module1)
            module6 = os.system(module2)





