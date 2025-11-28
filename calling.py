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

# User input for user

model_path = args.model
img_source = args.source
min_thresh = args.thresh 
user_res = args.resolution
record = args.record

# cheking for the file formate and that file exist or not 
if (not os.path.exists(model_path, task = 'detect')):
    print('ERROR : model path is in valid or model was not found. Make sure to enter the file correct  ')
    sys.exit(0)

# loading the yollo11s model in memory
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

# user specific display resolution 
resize = False 
if user_res:
    resize = True 
    resW, resH = int(user_res.split('x')[0]), int(user_res.split('x')[1])

# checking for recording 
if record :
    if source_type not in ['video','usb']:
        print("Recording only works for vedios and live camera ")
        sys.exit(0)
    if not user_res:
        print("please specify the resolutin to record the vedio at .")
        sys.exit(0)
    
    recording_name = input('enter the file name for recording ')
    record_fps = 30 
    recorder = cv2.VideoWriter(recording_name , cv2.VideoWriter_fourcc(*'MJPG'),record_fps,(resW,resH))
# loading correcct input source 

if source_type == 'image' :
    imgs_list = [img_source]

elif source_type == 'folder' :
    imgs_list = []
    filelist = glob.glob(img_source + '/*')
    for file in filelist :
        _, file_ext = os.path.splitext(file)
        if file_ext in img_ext_list:
            imgs_list.append(file)
elif source_type == 'video' or source_type == 'usb':
    if source_type == 'video': cap_arg = img_source
    elif source_type == 'usb' : cap_arg = usb_idx
    cap = cv2.VideoCapture(cap_arg)

    if user_res:
        cap.set(3,resW)
        cap.set(4,resH)

# handling rasberry pi camera 
 
elif source_type == 'picamera':
    from picamera2 import Picamera2
    cap = Picamera2()
    cap.configure(cap.create_video_configuration(main={"format" : 'XRGB888', "size":(resW,resH)}))
    cap.start()

bbox_colors = [(164,120,87), (68,148,228), (93,97,209), (178,182,133), (88,159,106)]
avg_frame_rate = 0 
frame_rate_buffer = []
img_count = 0 

t_start = time.perf_counter
if source_type == 'image' or source_type == 'folder':
    if img_count >= len (imgs_list):
        print('All images processed ')
        sys.exit(0)
    frame = cv2.imread(imgs_list[img_count])
    img_count += 1
elif source_type == 'vedio' or source_type == 'usb':
    ret , frame = cap.red()
    if not ret : break 

# same thing but for pi camera 

elif source_type == 'picamera' :
    frame = cv2.cvtColor(cap.capture_array(), cv2.COLOR_BGRA2BGR)

#resizing and run infrence 
    if resize: frame = cv2. resize  (frame,resW , resH)
    results = model (frame,verbose = False)
    detections = results[0].boxes

# Drawing the results 
object_count = 0 

for i in range (len(detections)):

    xyxy = detections[i].xyxy.cpu().numpy().squeeze()
    xmin,ymin,xmax,ymax = xyxy.astype(int)

    classidx = int (detections[i].cls.item())
    classname = labels[classidx]
    conf = detections[i].conf.item()

    if conf > float(min_thresh):
        color = bbox_colors[classidx % len (bbox_colors)]
        cv2.rectangle (frame,(xmin,ymin),(xmax,ymax),color,2)

        label = f'{classname}: {int(conf*100)} %'
        cv2.putText (frame, label, (xmin, ymin - 10 ), cv2.FONT_HERSHEY_SIMPLEX,0.5, color,2)
        object_count +=1 
        




