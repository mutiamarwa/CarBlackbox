import os
def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size
size=get_size()
print(size)

if (size>100000):
    path='/Users/hanschristian/Desktop/testfolder'
    oldest=min(os.listdir(path), key=os.path.getmtime)
    print(oldest)
    os.remove(oldest)
else:
    print('File not removed')

