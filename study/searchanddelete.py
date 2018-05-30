import os,sys,shutil

def search(rootdir,search_dir_name):
    if os.path.isdir(rootdir):
        list_new = os.listdir(rootdir)
        for  it in list_new:
            if it == search_dir_name: 
                #os.rmdir(os.path.join(rootdir,it)) #不能删除有文件的文件夹
                shutil.rmtree(os.path.join(rootdir, it))
            else:
                search(os.path.join(rootdir,it),search_dir_name)
    else:
        return

search("D:/Projects/github/python/study/cc","aa")