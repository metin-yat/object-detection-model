# Dockerizing Object Detection Model

I worked with 3 container;

### First ontainer contains a website which enables me to upload images,
I used Flask for the website.
### Second container stores the uploaded images to a local file and also uploads those images to AWS S3 Bucket.
When the images from the website is stored, this container takes those images to the another folder and also loads the images to specified S3 Bucket.
### Third and the last container contains the obj. det. model and saves outputs in a json file.
I used weights of the facebook/detr-resnet-50 from Hugginface's models.

Purpose of this system is to prove that I am capable of making a fully integrated machine learning pipeline, from web-based image upload and storage to real-time object detection and cloud-based deployment, demonstrating proficiency in Flask web development, Docker containerization, cloud storage (AWS S3), and deep learning (object detection with DETR) using PyTorch and Hugging Face.
