import os, sys, argparse , glob , time 
import cv2 , numpy as np 
from ultralytics import YOLO 

parser = argparse.ArgumentParser()
parser.add_argument('--model', required = True)
parser.add_argument('--source', required = True)
parser.add_argument('--thresh', default = 0.5)
parser.add_argument('--resolution', default= None)
parser.add_argument('--record', action = 'store_true')
args = parser.parse_args()

# User input for user

model_path = args.model
img_source = args.source
min_thresh = args.thresh 
user_res = args.resolution
record = args.record

# cheking for the file formate and that file exist or not 
if (not os.path.exists(model_path)):
    print('ERROR : model path is in valid or model was not found. Make sure to enter the file correct  ')
    sys.exit(0)

# loading the yollo11s model in memory
model = YOLO(model_path, task = 'detect')
labels = model.names

img_ext_list = ['.jpg','.JPG','.jpeg','.JPEG','.png','.PNG','.bmp','.BMP']
vid_ext_list = ['.avi','.mov','.mp4','.mkv','.wmv']

if os.path.isdir(img_source ):
    source_type = 'folder'
elif os.path.isfile (img_source ):
    _, ext = os.path.splitext(img_source)
    if ext in img_ext_list:
        source_type = 'image'
    elif ext in vid_ext_list:
        source_type = 'video'
    else: 
        print(f'File extension {ext} is not supported')
        sys.exit(0)
elif 'usb' in img_source :
    source_type= 'usb'
    usb_idx = int(img_source[3:])
elif 'picamera' in img_source:
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
    recorder = cv2.VideoWriter(recording_name, cv2.VideoWriter_fourcc(*'MJPG'), record_fps, (resW,resH))
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
        ret = cap.set(3, resW)
        ret = cap.set(4, resH)

# handling rasberry pi camera 
 
elif source_type == 'picamera':
    from picamera2 import Picamera2
    cap = Picamera2()
    cap.configure(cap.create_video_configuration(main={"format": 'XRGB8888', "size": (resW, resH)}))
    cap.start()
#takking frames and giving it to the model 
bbox_colors = [(164,120,87), (68,148,228), (93,97,209), (178,182,133), (88,159,106), 
              (96,202,231), (159,124,168), (169,162,241), (98,118,150), (172,176,184)]
avg_frame_rate = 0 
frame_rate_buffer = []
fps_avg_len = 200
img_count = 0 

while True:
    t_start = time.perf_counter()
    if source_type == 'image' or source_type == 'folder':
        if img_count >= len (imgs_list):
            print('All images processed ')
            sys.exit(0)
        frame = cv2.imread(imgs_list[img_count])
        img_count += 1
    elif source_type == 'video':
        ret , frame = cap.read()
        if not ret :
            print('Reached end of the video file. Exiting program.')
            break
    
    elif source_type == 'usb':
        ret , frame = cap.read()
        if (frame is None) or (not ret):
            print('Unable to read frames from the camera. This indicates the camera is disconnected or not working. Exiting program.')
            break 

    # same thing but for pi camera 
    elif source_type == 'picamera' :
        frame_bgra = cap.capture_array()
        frame = cv2.cvtColor(np.copy(frame_bgra), cv2.COLOR_BGRA2BGR)
        if (frame is None):
            print('Unable to read frames from the Picamera. This indicates the camera is disconnected or not working. Exiting program.')
            break

    #resizing and run infrence 
    if resize: frame = cv2.resize(frame, (resW, resH))
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

            label = f'{classname}: {int(conf*100)}%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            label_ymin = max(ymin, labelSize[1] + 10)
            cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), color, cv2.FILLED)
            cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            object_count +=1 
    
    # displaying , fps and cleanup
    if source_type == 'video' or source_type == 'usb' or source_type == 'picamera':
        cv2.putText(frame, f'FPS: {avg_frame_rate:0.2f}', (10,20), cv2.FONT_HERSHEY_SIMPLEX, .7, (0,255,255), 2)
    
    cv2.putText(frame, f'Number of objects: {object_count}', (10,40), cv2.FONT_HERSHEY_SIMPLEX, .7, (0,255,255), 2)
    cv2.imshow('YOLO Results', frame )
    if record : recorder.write(frame)
    
    if source_type == 'image' or source_type == 'folder':
        key = cv2.waitKey()
    elif source_type == 'video' or source_type == 'usb' or source_type == 'picamera':
        key = cv2.waitKey(5)
    
    if key == ord('q') or key == ord('Q'):
        break
    elif key == ord('s') or key == ord('S'):
        cv2.waitKey()
    elif key == ord('p') or key == ord('P'):
        cv2.imwrite('capture.png',frame) 

    #fps calculation
    t_stop = time.perf_counter()
    frame_rate_calc = float(1/(t_stop - t_start))
    
    if len(frame_rate_buffer) >= fps_avg_len:
        temp = frame_rate_buffer.pop(0)
        frame_rate_buffer.append(frame_rate_calc)
    else:
        frame_rate_buffer.append(frame_rate_calc)
    
    avg_frame_rate = np.mean(frame_rate_buffer)

#cleanup 
print(f'Average pipeline FPS: {avg_frame_rate:.2f}')
if source_type == 'video' or source_type == 'usb':
    cap.release()
elif source_type == 'picamera':
    cap.stop()
if record: recorder.release()
cv2.destroyAllWindows()
        





