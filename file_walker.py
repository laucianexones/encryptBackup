import os
#TODO fix the tab size
#TODO change the code python3

path_string='/Users/kerem/test2'
res = os.walk(path_string)

def getFilesize(filename):
    size = os.stat(filename).st_size
    return size

def getPermissions():
    pass


size_total = 0
for path,directories,files in res:
    for f in files:
        full_filepath = os.path.join(path,f)
        #size = os.stat(os.path.join(path,f)).st_size
        size = getFilesize(full_filepath)
        gid = os.stat(os.path.join(path,f)).st_gid
        print 'the file %s has a size of %i bytes' % (f,size)
        permissions = oct(os.stat(full_filepath).st_mode)
        print 'the file %s has the permissions %s' % (f,permissions)
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