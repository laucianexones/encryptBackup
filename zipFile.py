import os
import zipfile


path = r'C:\Users\kcumhurx\Desktop\na training'
target_file = '%s.zip' % path

zipObject = zipfile.ZipFile(target_file,'w',zipfile.ZIP_DEFLATED)

def zipdir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            fullpath_filename = os.path.join(root, file)
            #print fullpath_filename
            abs_filename = fullpath_filename.replace(path, '')
            #print abs_filename
                       
            zipObject.write(fullpath_filename, abs_filename)

    zipObject.close()
    print "%s created" % target_file
    

zipdir(path)

"""
import os
import stat
import zipfile

archive_num = 1
outfile = zipfile.ZipFile('/zips/archive%s.zip' % archive_num, "w")
zsize = 0

for full_name in filelist:
    full_name_path = os.path.join(full_name, full_path)
    if outfile.fp.tell() > 15728640: # 15mb
        outfile.close()
        archive_num += 1
        outfile = zipfile.ZipFile('/zips/archive%s.zip' % archive_num, "w")

    outfile.write(full_name_path,full_name_path,zipfile.ZIP_DEFLATED)


There is still a couple of "issues":

1) Files larger than 15Mb may not be able to be compressed to fall below the limit.

2) If you are near the 15Mb limit and the next file is very large you have the
same problem.


-Larry

"""
