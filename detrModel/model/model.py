import time, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image
import json

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
        #check event_type
        if str(event.event_type) == "created":
            formats = ["jpg", "jpeg", "png"]

            name =  str(event.src_path).split("\\")[-1]
            fileFormat = name.split(".")[-1]
            if '"' in fileFormat:fileFormat.replace('"', '')
            if "'" in fileFormat:fileFormat.replace("'", '')
            
            if fileFormat in formats:
                # Model Works
                outputDir = "/detrModel/outputs"
                model_path = "/detrModel/model"

                # Load the processor and model from the saved directory
                processor = DetrImageProcessor.from_pretrained(model_path)
                model = DetrForObjectDetection.from_pretrained(model_path)

                image = Image.open(event.src_path).convert("RGB")

                inputs = processor(images=image, return_tensors="pt")
                outputs = model(**inputs)
                
                objDetResults = f"{outputDir}/detections.json"

                # convert outputs (bounding boxes and class logits) to COCO API
                # let's only keep detections with score > 0.9
                target_sizes = torch.tensor([image.size[::-1]])
                results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

                detections = []

                # Check if the JSON file already exists
                if os.path.exists(objDetResults):
                    # Load existing detections
                    with open(objDetResults, "r") as f:
                        try:
                            detections = json.load(f)
                        except json.JSONDecodeError:
                            detections = []  # Start fresh if file is corrupt or empty
                else:
                    detections = []

                # Iterate over the detected objects
                for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
                    if score >= 0.9:  # Only keep high-confidence predictions
                        detection = {
                            "image_source": event.src_path,
                            "label": label.item(),
                            "label_name":model.config.id2label[label.item()],
                            "confidence": score.item(),
                            "bounding_box": box.tolist()  # Convert tensor to list for JSON compatibility
                        }
                        detections.append(detection)

                with open(objDetResults, "w") as f:
                    json.dump(detections, f, indent=4)

if __name__ == '__main__':
    DIR = "/detrModel/inputs"
    w = Watcher(DIR, MyHandler())
    w.run()