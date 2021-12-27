import threading
from ftplib import FTP
from tqdm import tqdm

class myThread(threading.Thread):
    def __init__(self, threadID, dir_name, file_list):
        ###############
        #Add ftp connection here!
        self.ftp = FTP('ftp.wwpdb.org')   # connect to host, default port
        self.ftp.login()               # user anonymous, passwd anonymous@   
        print(f'#{threadID} login successfully')
        ################
        self.threadID = threadID
        self.dir_name = dir_name
        self.file_list = file_list
        threading.Thread.__init__(self)
    def run(self):
        for file in tqdm(self.file_list, position=self.threadID):
            downloadFile(self, file, self.dir_name + file, self.threadID)

def downloadFile(self, dst, path, threadID):    
    try:
        with open(dst, 'wb') as f:
            self.ftp.retrbinary('RETR ' + path, f.write)
    except:
        with open(f'{self.threadID}.err', 'a') as f:
            print(f'{path}', file=f)


with open('filelist.txt') as f:
    target_list = [i.strip() for i in f.readlines()]
    target_list = [f'pdb{i}.ent.gz' for i in target_list]

num_thread = 15
length = len(target_list) // num_thread + 1

remote_dirname = '/pub/pdb/data/structures/all/pdb/'
threads = [myThread(i, remote_dirname, target_list[i*length:(i+1)*length]) for i in range(num_thread)]


for t in threads:
    t.start()
for t in threads:
    t.join()
