import time, shutil, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import boto3

class Watcher:

    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self):
        self.observer.schedule(
            self.handler, self.directory, recursive=True)
        self.observer.start()
        print("\nWatcher Running in {}/\n".format(self.directory))
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")

class MyHandler(FileSystemEventHandler):
    
    def on_any_event(self, event):  
        # Function that lets me upload files to specific bucket for this code.
        def TOS3BUCKET(LOCAL_FILE, NAME_FOR_S3):
            AWS_S3_BUCKET_NAME = 'AWS_S3_BUCKET_NAME'
            AWS_REGION = 'AWS_REGION'
            AWS_ACCESS_KEY = 'AWS_ACCESS_KEY'
            AWS_SECRET_KEY = 'AWS_SECRET_KEY'

            s3_client = boto3.client(
                service_name='s3',
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY
            )

            response = s3_client.upload_file(LOCAL_FILE,
                                            AWS_S3_BUCKET_NAME,
                                            NAME_FOR_S3)

        # check event_type
        if str(event.event_type) == "created":
            formats = ["jpg", "jpeg", "png"]
            target_dir = "/monitoring/inputs/"

            name =  str(event.src_path).split("\\")[-1]
            fileFormat = name.split(".")[-1]
            if '"' in fileFormat:fileFormat.replace('"', '')
            if "'" in fileFormat:fileFormat.replace("'", '')
            
            if fileFormat in formats:
                # copying the image file to local dir which is target_dir
                shutil.copy(event.src_path, target_dir)

                # uploading image file to s3 bucket
                TOS3BUCKET(LOCAL_FILE= event.src_path,
                           NAME_FOR_S3 = event.src_path)

if __name__ == '__main__':
    # Ill mount local dir with: /monitoring/images 
    
    DIR = "/monitoring/comingImages"
    w = Watcher(DIR, MyHandler())
    w.run()