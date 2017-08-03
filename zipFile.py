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
