import cv2
import numpy as np
import time
import enum
import requests

URL = 'http://13.125.221.213:5555/fall_down'
data = {'user_id' : '1'}

# Load Yolo
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
blue_color = (255,0,0)
red_color = (0,0,255)

# Open Cam
try:
    print("open cam")
    cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture('/Users/hyunjigonji/yolo_object_detection')
except:
    print("not working")
cap.set(3, 800)
cap.set(4, 600)

class status(enum.Enum):
    standing = 0
    lying = 1
    falldown = 2

origin_time = 0
now_time = 0
beforeStatus = status.standing
nowStatus = status.standing
# Taking video
while True:
    # Loading image
    ret, frame = cap.read()
    #frame = cv2.resize(frame, (600,600), cv2.INTER_AREA)
    height, width, channels = frame.shape
    #height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    #blob = cv2.dnn.blobFromImage(frame)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            if str(classes[class_id]) != 'person': continue
            confidence = scores[class_id]
            if confidence > 0.8:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                if w/2 > h: # detected
                    color = red_color
                    if beforeStatus == status.standing or beforeStatus == status.falldown:
                        nowStatus = status.falldown
                        if origin_time == 0:
                            origin_time = time.time() # count start
                        else:
                            now_time = time.time()
                            if now_time - origin_time >= 5 and origin_time is not 0:
                                #print(args)
                                print("fall down!")
                                res = requests.post(URL, json=data)
                                origin_time = 0
                                
                    else:
                        nowStatus = status.lying
                        origin_time = 0
                elif w > h:
                    nowStatus = status.lying
                    color = blue_color
                else:
                    nowStatus = status.standing
                    color = blue_color
                    origin_time = 0
                #label = str(classes[class_ids[i]])
                #color = colors[i]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                #cv2.putText(frame, label, (x, y + 30), font, 3, color, 3)
                #boxes.append([x, y, w, h])
                #confidences.append(float(confidence))
                #class_ids.append(class_id)
                beforeStatus = nowStatus
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    '''for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            if w > h:
                #print("fall down!!")
                color = red_color
                if origin_time == 0:
                    origin_time = time.time()
                else:
                    now_time = time.time()
                    if now_time - origin_time >= 5:
                        print("fall down!")
                        origin_time = 0
            else:
                color = blue_color
                origin_time = 0
            #label = str(classes[class_ids[i]])
            #color = colors[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            #cv2.putText(frame, label, (x, y + 30), font, 3, color, 3) '''
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27: break
    time.sleep(1)
cv2.destroyAllWindows()
