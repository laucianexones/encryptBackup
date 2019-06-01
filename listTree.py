import os
import platform
import sys

""" print platform.platform()
print sys.getfilesystemencoding()
print sys.getdefaultencoding()
print sys.stdout.encoding """


"""
C:\Users\kc\Documents\Python-Projects\encryptBackup>python listTree_test.py
Saved Pictures/
    20170131_081744.jpg - 2.9 MB
    subfolder1/
        20170131_081728.jpg - 3.9 MB
        20170131_081730.jpg - 4.1 MB
    subfolder2/
        20170131_081735.jpg - 3.1 MB
        20170131_081743.jpg - 3.0 MB

"""

def getFilesize(filename):
    size = os.stat(filename).st_size
    return size

def file_size(file_path):
    #print os.path.dirname(file_path)
    #print '%s has type %s' % (file_path, type(file_path))

    if not os.path.isfile(file_path):
        print "file %s not found" % file_path
        exit(1)
    file_info = os.stat(file_path)
    return convert_bytes(file_info.st_size)


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def list_files(startpath):
    print startpath
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        #print 'level is ', level
        indent = ' ' * 4 * (level)
        #print "indent: ", len(indent)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for d in dirs:
            #print d
            print('{}{}'.format(subindent,os.path.join(root,d)))
        # for f in files:
        #     #print f, repr(f)
        #     #f = f.decode('cp850').encode('utf-8')
        #     print('{}{} - {}'.format(subindent, f,file_size(os.path.join(root,f))))
        #     #print 'leaving subfolder'

startpath = r'/Users/kerem/Desktop/testFolder2/'
#startpath = r'C:\\Users\\kc\\Desktop\\testFolder'
list_files(startpath)
