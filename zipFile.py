import os
import zipfile

path = r'C:\Users\kc\Desktop\_tmp\Saved Pictures'

def zipdir(path, ziph):
  for root, dirs, files in os.walk(path):
    for file in files:
      ziph.write(os.path.join(root,file))

if __name__ == '__main__':
  zipf = zipfile.ZipFile('test.zip', 'w', zipfile.ZIP_DEFLATED)
  zipdir(path, zipf)
  zipf.close()
