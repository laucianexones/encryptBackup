# Walk Over the File System

## understanding the generator object os.walk returns

how the file sytem looks like

```bash
bash-3.2$ tree /Users/kerem/test/ | less
/Users/kerem/test/
├── 2742OS_1_05.sh
├── Chapter\ 1
│   └── 2742OS_01_Code
│       ├── 2742OS_1_01.sh
│       ├── 2742OS_1_02.sh
│       ├── 2742OS_1_03.sh
│       ├── 2742OS_1_04.sh
│       ├── 2742OS_1_05.sh
│       ├── 2742OS_1_06.sh
│       ├── 2742OS_1_07.sh
│       ├── 2742OS_1_08.sh
│       ├── 2742OS_1_09.sh
│       └── 2742OS_1_10.sh
├── Chapter\ 2
│   └── 2742OS_02_Code
│       ├── 2742OS_2_01.sh
│       ├── 2742OS_2_02.sh
│       ├── 2742OS_2_03.sh
│       ├── 2742OS_2_04.sh
│       └── 2742OS_2_05.sh
..
..
├── arrays.md
├── bashTutorial
│   ├── Redirections.md
│   ├── alias.md
│   ├── arrays.md
│   ├── dates.md
│   ├── pics
│   │   └── tty.png
│   └── terminal.md
├── cleanup
├── data
│   ├── messages
│   └── wtmp
├── date.py
├── file1
├── iterate
└── pass_cp
```

let's iterate over the path - running the .next() shows the folders,files and path on the first level

```python
>>> import os
>>> gen = os.walk('/Users/kerem/test')
>>> type(gen)
<type 'generator'>
>>> gen.next()
('/Users/kerem/test', ['Chapter 7', 'Chapter 9', 'bashTutorial', 'Chapter 8', 'Chapter 1', 'Chapter 3', 'Chapter 4', 'Chapter 5', 'Chapter 2', 'data'], ['2742OS_1_05.sh', '.DS_Store', 'iterate', 'pass_cp', 'cleanup', 'arrays.md', 'file1', 'date.py'])
```

running next() again will go one level deeper (and again..and again..)

```python

>>> gen.next()
('/Users/kerem/test/Chapter 7', ['2742OS_07_Code'], []) # this is level 2
>>> gen.next() # this goes to level 3
('/Users/kerem/test/Chapter 7/2742OS_07_Code', [], ['2742OS_7_04.sh', '2742OS_7_05.sh', '2742OS_7_01.sh', '2742OS_7_06.sh', '2742OS_7_02.sh', '2742OS_7_03.sh'])
```

## counting the files on the file system

this is how the file system structure looks like

```bash
bash-3.2$ tree /Users/kerem/test2/
/Users/kerem/test2/
├── file1
├── file2
├── sub1
│   └── file3
└── sub2
    └── file4

2 directories, 4 files
```

the python script to count the files
```python
path_string='/Users/kerem/test2'
res = os.walk(path_string)

count = 0
for path,directories,files in res:
    for f in files:
        print 'file is %s' % os.path.join(path,f)
        count += 1
print 'there are in %i files' % count
```

## to get file level information

```python
for path,directories,files in res:
    for f in files:
        if f == 'file1':
            print f
            print os.stat(os.path.join(path,f))

## OUTPUT
file1
posix.stat_result(st_mode=33188, st_ino=2583505, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=0, st_atime=1553029612, st_mtime=1553029612, st_ctime=1553029612)
```

details on stat_results can be found [here](https://docs.python.org/2/library/stat.html)

An example gist to calculate the total size of the files
```python
size_total = 0
for path,directories,files in res:
    for f in files:
        size = os.stat(os.path.join(path,f)).st_size
        print 'the file %s has a size of %i bytes' % (f,size)
        size_total = size_total + size

print size_total 
print size_total / 1024 
```

notice the difference between 77KB and 80KB. This is how much the file block allocates on disk

```bash
# OUTPUT
the file file2 has a size of 26846 bytes
the file file1 has a size of 52772 bytes
the file file3 has a size of 0 bytes
the file file4 has a size of 0 bytes
79618 (bytes)
77 (KB)


bash-3.2$ du -h
  0B	./sub1
  0B	./sub2
 80K	.
```

here is the block size allocation explained
```bash
bash-3.2$ echo 'a' > sub1/file3 
bash-3.2$ ls -la sub1/file3 
-rw-r--r--  1 kerem  staff  2 Mar 19 22:40 sub1/file3
bash-3.2$ du -h
4.0K	./sub1
  0B	./sub2
 84K	.
```

the file 'sub1/file3' has only 1 character, in total it is 2 bytes, but on disk usage the allocation shows 4.0K for that block.

## get the user & group name

```python
for path,directories,files in res:
    for f in files:
        size = os.stat(os.path.join(path,f)).st_size
        print 'the file %s has a size of %i bytes' % (f,size)
        size_total = size_total + size
        print 'the user: %s' % os.stat(os.path.join(path,f)).st_uid
        print 'the group: %s' % os.stat(os.path.join(path,f)).st_gid
        print '-'*10

## 
the file file4 has a size of 0 bytes
the user: 501
the group: 20


bash-3.2$ id -nu 501
kerem
 #TODO 
 import grp,sys
print grp.getgrnam('staff')

#gid =g.gr_gid for g in grp.getgrall()
#if g.gr_name==gname][:1]
#    print gid
```