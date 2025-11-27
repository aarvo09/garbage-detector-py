import os, sys, argparse , glob , time 
import cv2 , numpy as np 
from ultralytics import YOLO 

parser = argparse.ArgumentParser()
parser.add_argument('--model', required = True)
parser.add_argument('--source', required = True)
parser.add_argument('--thresh', default = 0.5)
parser.add_argument('--resolution', default= None)
parser.add_argument('--record', action = 'store_true')
args = parser.parse_args

# USER INPUT FOR USER 

model_path = args.model
img_source = args.source
min_thresh = args.thresh 
user_res = args.resolution
record = args.record

# CHEKING THAT MODEL FILE EXIST OR NOT AND IT IS VALID FIELE OR NOT 
if (not os.path.exists(model_path, task = 'detect')):
    print('ERROR : model path is in valid or model was not found. Make sure to enter the file correct  ')
    sys.exit(0)

# LOADING THE MODEL INTO MEMORY 
model = YOLO(model_path, task = 'detect')
labels = model.names

img_ext_list = ['.jpg','.JPG','.jpeg','.JPEG','.png','.PNG','.bmp','.BMP']
vid_ext_list = ['.avi','.mov','.mp4','.mkv','.wmv']

if os.path.isdir(img_source ):
    Source_type = 'folder'
elif os.path.isfile (img_source ):
    _, ext = os.path.splitext(img_source)
    if ext in vid_ext_list:
        source_type = 'image'
    elif ext in vid_ext_list:
        source_type = 'video'
    else: 
        print(f'File extension {ext} is not supported')
        sys.exit(0)
elif 'usb' in img_source :
    source_type= 'usb'
    usb_idx = int(img_source[3:])
elif 'picamra' in img_source:
    source_type = 'picamera'
    picam_idx = int(img_source[8:])
else: 
    print(f'Input{img_source} is invalid.try again or check the camera setup')
    sys.exit(0)

