import os
import zipfile


path = r'C:\Users\kcumhurx\Desktop\na training'
target_file = '%s.zip' % path
pwd = b'kerem'
print type(pwd)
LIMIT_SIZE = 10485760 # 10MB

zipObject = zipfile.ZipFile(target_file,'w',zipfile.ZIP_DEFLATED)
zipObject.setpassword(pwd)

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

num = 0
def zipdir(path, zipObject, num):
    for root, dirs, files in os.walk(path):
        for file in files:
            fullpath_filename = os.path.join(root, file)
            #print fullpath_filename
            abs_filename = fullpath_filename.replace(path, '')
            #print abs_filename

            print type(zipObject)            
            file_size = zipObject.fp.tell()
            if not file_size >= LIMIT_SIZE:
                zipObject.write(fullpath_filename, abs_filename)
                print '%s compressed' % abs_filename
                print zipObject.fp.tell()
                print '\n'
            else:
                print 'new archieve file'
                zipObject.close()
                num += 1
                zipObject = zipfile.ZipFile('%s_%s.zip' % (path, num), 'w', zipfile.ZIP_DEFLATED)
                zipObject.write(fullpath_filename, abs_filename)
                print '%s compressed' % abs_filename
                print zipObject.fp.tell()
                print '\n'

    
    file_size = zipObject.fp.tell()
    file_size_human_readable = convert_bytes(file_size)
    
    print 'size is: ', file_size_human_readable
    zipObject.close()
    print "%s created" % target_file
    


zipdir(path, zipObject, num)

