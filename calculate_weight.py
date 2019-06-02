import os,sys
import pprint
import operator
overall_dict = {}
#TODO enable parameter for pretty print option
pretty_print = False

#TODO write a proper usage text
def usage():
    print 'run the script with a valid foldername'

def check_startpath(s_path):
    #if this folder is a valid directory
    if os.path.isdir(s_path):
        return True


def get_filesize(filename):
    size = os.stat(filename).st_size
    return size 

def create_database(folder_path,num_of_files,num_of_subfolders,folder_size_sum,level,parent,depth):
    if not overall_dict.has_key(folder_path):
        overall_dict[folder_path] = [num_of_files,folder_size_sum,level,parent,num_of_subfolders]
        if level > depth:
            depth = level
    return depth


def recreate_database(depth):
    # take as argument the depth of the tree
    # make a bottom-up iteration over the tree represented in the overall_dict variable
    # use range(depth,-1,-1) to start from the last level # range(5,-1,-1) results to [5, 4, 3, 2, 1, 0]
    # for item in overall_dict:
    #     for i in range(depth,-1,-1):
    for i in range(depth,-1,-1):
        for item in overall_dict:
            # if the item of the dictionary has the depth-level we are looking for
            # get the parent item of the current folder
            # add current folders size to the parent
            if overall_dict[item][2] == i:
                parent = overall_dict[item][3]
                if parent == None:
                    continue
                folder_size = overall_dict[item][1]
                overall_dict[parent][1] += folder_size


def print_dict_sorted(dict):
    sorted_dict_as_list = sorted(dict.items(),key=lambda x:x[1][2])
    l_level = 0
    for i in sorted_dict_as_list:
        level = i[1][2]
        sizeGB = i[1][1] / (1024*1024*1024)
        num_of_files = i[1][0]
        num_of_subfolders = i[1][4]
        folder_path = i[0]

        #TODO remove parent information & calculate weight
        #subfolder number relevant for weight ??

        if level > l_level:
            print '--'
            l_level = level
        print 'sizeGB:%s\t#_files:%s\t#_subfolders:%s\tlevel:%s\t\tpath:%s' % (sizeGB,num_of_files,num_of_subfolders,level,folder_path)



def scan_filesystem(startpath,tree_depth):
    '''
    scans the given file system and creates a database with number of files, folder size, level and parents
    '''
    if pretty_print:
        print 'W:Weight S:Size in KB N:Num of files SF: Num of Subfolders'
        print startpath
        print '##'*20
    
    for folder_path, dirs, files in os.walk(startpath):
        level = folder_path.replace(startpath, '').count(os.sep) +1
        current_dir = folder_path.replace(startpath,'').split(os.sep)[-1]
        #parent = folder_path.replace(current_dir,'').rstrip('/')
        parent = os.sep.join(folder_path.split(os.sep)[:-1])
        if current_dir == '':
            current_dir = '/'
            parent = None
            level = 0
        if folder_path == startpath:
            folder_path = folder_path.rstrip('/')
        
        #DEBUG Commands : use them to understand the loop step
        # print 'folder_path :', folder_path
        # print 'current_dir is :', current_dir
        # print 'level is : ', level
        # print 'subdirs are :', dirs
        # print 'files are :', files
        # print 'parent :' , parent

        # this for-loop iterates over the current directory
        # checks the size of each file #TODO check for other filetypes like links,hardlinks etc..
        # saves the total size of the folder to folder_size_sum
        # it also counts the number of files in the folder
        # using these 2 variables a weight is created
        folder_size_sum = 0        
        for f in files:
            f_fullpath = os.path.join(folder_path,f)
            # skip the file if it is a symlink
            if os.path.islink(f_fullpath):
                continue
            f_size = get_filesize(f_fullpath)
            folder_size_sum += f_size
        # get the number of files in the current folder
        num_of_files = len(files)
        # get the number of subfolders in the current folders
        num_of_subfolders = len(dirs)

        # print the current dir and related information 
        # use indent var. in the formatting to show the depth of the folder
        if pretty_print:
            indent = '-' * 4 * (level)
            print('{}{} - W:{} S:{} N:{} SF:{}'.format(indent, current_dir, weight, folder_size_sum, num_of_files,num_of_subfolders))
        
        tree_depth = create_database(folder_path,num_of_files,num_of_subfolders,folder_size_sum,level,parent,tree_depth)
        #print '-'*20

    return tree_depth


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        exit(1)
    startpath = sys.argv[1]
    if check_startpath(startpath):
        tree_depth = 0
        tree_depth = scan_filesystem(startpath,tree_depth)
    else:
        print '%s is not a valid directory path' % startpath

    recreate_database(tree_depth)
    print_dict_sorted(overall_dict)