import time  
import sys
import configparser
import tinys3
import threading
import requests
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler   


class MyHandler(PatternMatchingEventHandler):

    def __init__(self,config):
        super(MyHandler, self).__init__(ignore_patterns=config.get('Configuration', 'extensions').split(";"))
        self.tls = config.get('Configuration', 'tls')
        self.endpoint = config.get('Configuration', 'endpoint')
        self.access_key = config.get('Configuration', 'access_key')
        self.security_key =config.get('Configuration', 'security_key')
        self.bucket_name = config.get('Configuration', 'bucket_name')
        self.log_file = config.get('Configuration', 'logFile')
        self.lock = threading.Lock()

    def uploadFunc(self,file_path):
        conn = tinys3.Connection(self.access_key, self.security_key, self.tls, self.endpoint)
        f = open(file_path,'rb')
        file_name = file_path.split("/")
        try:
            resp = conn.upload(file_name[len(file_name)-1],f,self.bucket_name)
            self.logToFile(file_name[len(file_name)-1], resp.status_code, time.time())
        except requests.exceptions.HTTPError as e: 
            self.logToFile(file_name[len(file_name)-1],e.response.status_code, time.time())
        except:# cleanup
            f.close()

    def logToFile(self, file_name, success, epoch_time):
        self.lock.acquire()
        f = open(self.log_file, 'a+') 
        print(file_name, ' ', success, ' ', epoch_time , file=f)
        f.close()
        self.lock.release()

    def process(self, event):
        if event.event_type == 'created': # TODO handle delete
            threading.Thread(target=self.uploadFunc,args=(event.src_path,)).start()
        
    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)




if __name__ == '__main__':
    args = sys.argv[1:]
    config = configparser.ConfigParser()
    observer = Observer()


    config.read(args[0])
    inf = config.get('Configuration', 'input')
    observer.schedule(MyHandler(config), path=inf)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
