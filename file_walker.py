import os

path_string='/Users/kerem/test2'
res = os.walk(path_string)

size_total = 0
for path,directories,files in res:
    for f in files:
        size = os.stat(os.path.join(path,f)).st_size
        gid = os.stat(os.path.join(path,f)).st_gid
        print 'the file %s has a size of %i bytes' % (f,size)
        size_total = size_total + size
        print 'the user: %s' % os.stat(os.path.join(path,f)).st_uid
        print 'the group: %s' % gid
        print '-'*10
print size_total
print size_total / 1024

import grp,sys
print grp.getgrnam('staff')

#gid =g.gr_gid for g in grp.getgrall()
#if g.gr_name==gname][:1]
#    print gid