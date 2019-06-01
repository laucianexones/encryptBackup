import os,sys
import pprint
import operator
overall_dict = {}

def usage():
    print 'run the script with a valid foldername'

def check_startpath(s_path):
    #if this folder is a valid directory
    if os.path.isdir(s_path):
        return True


def get_filesize(filename):
    size = os.stat(filename).st_size
    return size

#TODO
def accumulate_parent_weight(current_dir,parent,folder_size_sum):
    # write the calculated size of the current_dir to the local dict
    # if the folder has a parent, add the folder size to the parent as well
    if not overall_dict.has_key(current_dir):
        overall_dict[current_dir] = folder_size_sum
    else:
        # this else clause should not happen
        print '#DEBUG ELSE'
        overall_dict[current_dir] = overall_dict[current_dir] + folder_size_sum

    if not overall_dict.has_key(parent):
        overall_dict[parent] = folder_size_sum
    else:
        overall_dict[parent] = overall_dict[parent] + folder_size_sum
    pprint.pprint(overall_dict)
    

def print_dict_sorted(dict):
    sorted_dict = sorted(dict.items(),key=operator.itemgetter(1))
    print 'sorting...'
    pprint.pprint(sorted_dict)


#TODO rename the function - confusing name
def list_files(startpath):
    print 'W:Weight S:Size in KB N:Num of files SF: Num of Subfolders'
    print startpath
    print '##'*20
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        current_dir = root.replace(startpath,'').split(os.sep)[-1]
        parent = root.replace(current_dir,'')
        if current_dir == '':
            current_dir = '/'
            parent = None
        print '#parent : ', parent
        
        # DEBUG Commands : use them to understand the loop step
        # print 'current_dir is :', current_dir
        # print 'level is : ', level
        # print 'subdirs are :', dirs
        # print 'files are :', files

        # this for-loop iterates over the current directory
        # checks the size of each file #TODO check for other filetypes like links,hardlinks etc..
        # saves the total size of the folder to folder_size_sum
        # it also counts the number of files in the folder
        # using these 2 variables a weight is created
        folder_size_sum = 0        
        for f in files:
            f_fullpath = os.path.join(root,f)
            # skip the file if it is a symlink
            if os.path.islink(f_fullpath):
                continue
            f_size = get_filesize(f_fullpath)
            folder_size_sum += f_size
        # calculate the weight of the folder
        num_of_files = len(files)
        weight = float((num_of_files * folder_size_sum) / 1024)

        # get the number of subfolders in the current folders
        num_of_subfolders = len(dirs)

        # print the current dir and related information 
        # use indent var. in the formatting to show the depth of the folder
        indent = ' ' * 4 * (level)
        print('{}{} - W:{} S:{} N:{} SF:{}'.format(indent, current_dir, weight, folder_size_sum, num_of_files,num_of_subfolders))
        
        #TODO fix the parent & current folder names
        #parent :  /Users/kerem/Desktop/testFolder2/level1-F3/
        # L2-F3 - W:174.0 S:22308 N:8 SF:1
        # {None: 0,
        # '/Users/kerem/Desktop/testFolder2/': 22392,
        # '/Users/kerem/Desktop/testFolder2/level1-F3': 22392,
        # '/Users/kerem/Desktop/testFolder2/level1-F3/': 22308,
        # '/Users/kerem/Desktop/testFolder2/level1-F3/L2-F3': 22308}

        accumulate_parent_weight(root,parent,folder_size_sum)
        print '-'*20

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        exit(1)
    startpath = sys.argv[1]
    if check_startpath(startpath):
       list_files(startpath)
    else:
        print '%s is not a valid directory path' % startpath

    print_dict_sorted(overall_dict)

#startpath = r'/Users/kerem/Desktop/testFolder2/'
#list_files(startpath)