import os,sys
import pprint
#import operator

#TODO
'''
re-write the whole code
use topdown, skip symlink parameters of os.walker
https://gist.github.com/samuelsh/a8be5bc93fcd7ff256c9
https://www.tutorialspoint.com/python3/os_walk.htm
use the multiprocessing module to parallelize
'''


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

def create_database(folder_path,num_of_files,num_of_subfolders,folder_size_sum,level,parent,depth,fs_tree):

    if not fs_tree.has_key(folder_path):
        fs_tree[folder_path] = [num_of_files,folder_size_sum,level,parent,num_of_subfolders]
        if level > depth:
            depth = level
    return depth,fs_tree


def recreate_database(depth,fs_tree):
    # take as argument the depth of the tree
    # make a bottom-up iteration over the tree represented in the fs_tree variable
    # use range(depth,-1,-1) to start from the last level # range(5,-1,-1) results to [5, 4, 3, 2, 1, 0]
    # for item in overall_dict:
    #     for i in range(depth,-1,-1):
    for i in range(depth,-1,-1):
        for item in fs_tree:
            # if the item of the dictionary has the depth-level we are looking for
            # get the parent item of the current folder
            # add current folders size to the parent
            if fs_tree[item][2] == i:
                parent = fs_tree[item][3]
                if parent == None:
                    continue
                folder_size = fs_tree[item][1]
                fs_tree[parent][1] += folder_size
    return fs_tree

def print_dict_sorted(dict,top_folders):
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

        # normalize the values to use in the weight calculation formula
        values_for_weight = [sizeGB,num_of_files,num_of_subfolders]
        for i in values_for_weight:
            if i == 0:
                ind = values_for_weight.index(i)
                values_for_weight[ind] = 1
        f_folder_size, f_num_of_files, f_num_subfolders = values_for_weight 
        # normalize the number of files by dividing to 100
        weight = f_folder_size * (f_num_of_files/100) * f_num_subfolders


        top_folders.append([weight,sizeGB,num_of_files,num_of_subfolders,folder_path])
        if level > l_level:
            print '--'
            l_level = level
        print 'WeightScore:%s\t\t\tsizeGB:%s\t#_files:%s\t#_subfolders:%s\tlevel:%s\t\tpath:%s' % (weight,sizeGB,num_of_files,num_of_subfolders,\
            level,folder_path)
    
    print '--'*20
    print '--'*20
    print 'printing the top-10 weighted folders..'
    print 'weight,sizeGB,#_files,#_subfolders'
    for i in sorted(top_folders)[::-1][:10]:
        print i


def scan_filesystem(startpath,tree_depth,fs_tree):
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

        # this for-loop iterates over the current directory
        # saves the total size of the folder to folder_size_sum
        # it also counts the number of files in the folder
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

        #TODO fix the the outout of the pretty print
        weight = 0
        # print the current dir and related information 
        # use indent var. in the formatting to show the depth of the folder
        if pretty_print:
            indent = '-' * 4 * (level)
            print('{}{} - W:{} S:{} N:{} SF:{}'.format(indent, current_dir, weight, folder_size_sum, num_of_files,num_of_subfolders))
        
        tree_depth,fs_tree = create_database(folder_path,num_of_files,num_of_subfolders,folder_size_sum,level,parent,tree_depth,fs_tree)
        #print '-'*20

    return tree_depth,fs_tree


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        exit(1)
    startpath = sys.argv[1]
    #do the scan of the filesystem
    if check_startpath(startpath):
        tree_depth,fs_tree = scan_filesystem(startpath,tree_depth=0,fs_tree={})
    else:
        print '%s is not a valid directory path' % startpath
    #do the bottom-up sorting & size calculation of the filesystem tree
    fs_tree = recreate_database(tree_depth,fs_tree)
    
    #print the tree by levels & top-10 weighted directories
    print_dict_sorted(fs_tree,top_folders=[])


