import os
import zipfile

path =  r'C:\Users\kc\Desktop\_tmp\rootFolder'

def zipdir(path):
  for root, dirs, files in os.walk(path):
    print dirs

if __name__ == '__main__':
  #zipf = zipfile.Zipfile('test.zip','w',zipfile.ZIP_DEFLATED)
  zipdir(path)
