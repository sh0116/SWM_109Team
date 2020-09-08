import cv2
import numpy as np
import time
import enum
from picamera import PiCamera
from picamera.array import PiRGBArray
import re
from tflite_runtime.interpreter import Interpreter
from datetime import datetime


#time_URL = 'http://13.125.221.213:5000/wake_up'
day = ['월요일','화요일','수요일', '목요일', '금요일', '토요일', '일요일']
cal_day = datetime.today().weekday()

sleep_check = 0
wake_check = 0

def day_sleep_time():
    sleep_hour = int(nowTuple.tm_hour) 
    sleep_min = int(nowTuple.tm_min)
    seconds = (pre_time.hour * 60 + pre_time.minute) * 60 + pre_time.second
    sleep_time = seconds/3600
    data = {'user_id' : '1', 'graph' : sleep_time,'day':day[cal_day]}
    print("취침일시 : {}-{}-{} {}:{}:{}".format(pre_time.year, pre_time.month, pre_time.day
                                            ,pre_time.hour,pre_time.minute,pre_time.second))
    print("잠들었습니다. %d",sleep_time,day[cal_day])
    #res = requests.post(time_URL, json=data)

    
def day_wake_time():
    wake_up_hour = int(nowTuple.tm_hour)
    wake_up_min = int(nowTuple.tm_min)
    seconds = (pre_time.hour * 60 + pre_time.minute) * 60 + pre_time.second
    wake_up_time = seconds/3600
    if seconds >= 14400 and seconds<=27000:
        data = {'user_id' : '3', 'graph' : wake_up_time,'day':day[cal_day]}
        print("기상일시 : {}-{}-{} {}:{}:{}".format(pre_time.year, pre_time.month, pre_time.day
                                                ,pre_time.hour,pre_time.minute,pre_time.second))
        print("깨어났네요 %d",wake_up_time,day[cal_day])
        #res = requests.post(time_URL, json=data)



class status(enum.Enum):
    standing = 0
    lying = 1
    falldown = 2
    
blue_color = (255,0,0)
red_color = (0,0,255)
green_color = (0,255,0)

min_confidence = 0.6
margin = 30
label_name = "coco_labels.txt"
model_name = "detect.tflite"

def load_labels(path):
  """Loads the labels file. Supports files with or without index numbers."""
  with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
      pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
      if len(pair) == 2 and pair[0].strip().isdigit():
        labels[int(pair[0])] = pair[1].strip()
      else:
        labels[row_number] = pair[0].strip()
  #print(labels)
  return labels

def set_input_tensor(interpreter, image):
  """Sets the input tensor."""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image

def get_output_tensor(interpreter, index):
  """Returns the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor

def detect_objects(interpreter, image, threshold):
  """Returns a list of detection results, each a dictionary of object info."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # Get all output details
  boxes = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  scores = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  results = []
  for i in range(count):
    if scores[i] >= threshold:
      result = {
          'bounding_box': boxes[i],
          'class_id': classes[i],
          'score': scores[i]
      }
      results.append(result)
  return results


# Load tflite
labels = load_labels(label_name)
interpreter = Interpreter(model_name)
interpreter.allocate_tensors()
_, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

# Open cam
cap = PiCamera()
try:
    cap.framerate = 32
    cap.resolution = (320,240)
except:
    print("cannot open cam")
rawCapture = PiRGBArray(cap, size=(320, 240))
rawCapture.truncate(0)

pre_time = datetime.now()
nowTuple = pre_time.timetuple()

origin_time = 0
now_time = 0
sleeptime=0



beforeStatus = status.standing
nowStatus = status.standing

standing_time = time.time()
lying_time = time.time()
falldown_time = time.time()

hasPrinted = False

# Detecting objects
for frame in cap.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    start_time = time.time()
    img = np.asarray(frame.array)
    height, width, channels = img.shape
    img = cv2.resize(img, (300,300))

    outs = detect_objects(interpreter, img, min_confidence)

    for out in outs:
        if out['class_id'] == 0 and out['score'] > min_confidence:
            # Convert the bounding box figures from relative coordinates
            # to absolute coordinates based on the original resolution
            ymin, xmin, ymax, xmax = out['bounding_box']
            xmin = int(xmin * width)
            xmax = int(xmax * width)
            ymin = int(ymin * height)
            ymax = int(ymax * height)
            w = xmax - xmin
            h = ymax - ymin
            
            if w/2 > h: # fall down
                now_time = time.time()
                diff_time = now_time - standing_time
                if diff_time <= 1:
                    falldown_time = time.time()
                    nowStatus = status.falldown
                    color = red_color
                    print("fall down 111")
                    #play_mp3_question()
                elif beforeStatus == status.falldown:
                    if diff_time >= 5 and diff_time < 10:
                        falldown_time = time.time()
                        nowStatus = status.falldown
                        color = red_color
                        if hasPrinted == False:
                            print("fall down 222")
                            #play_mp3_question()
                            hasPrinted2 = True
                    elif diff_time >= 10:
                        falldown_time = time.time()
                        nowStatus = status.falldown
                        color = red_color
                        print("fall down 333")
                        #play_mp3_notice()
                        quit()
                else: # lying
                    lying_time = time.time()
                    nowStatus = status.lying
                    sleeptime = sleeptime+1
                        if sleeptime >= 5:
                            seconds = (pre_time.hour * 60 + pre_time.minute) * 60 + pre_time.second
                            sleep_time = seconds/3600
                            if (seconds >= 75,600 and seconds<=86339) or (seconds >=0 and seconds <=1800) :
                                if sleep_check == 0:
                                    sleep_check +=1
                                    day_sleep_time()
                                else:
                                    continue
                            else:
                                sleep_check = 0

                    color = green_color
            elif w > h: # lying
                lying_time = time.time()
                nowStatus = status.lying
                sleeptime = sleeptime+1
                    if sleeptime >= 5:
                            seconds = (pre_time.hour * 60 + pre_time.minute) * 60 + pre_time.second
                            sleep_time = seconds/3600
                            if (seconds >= 75,600 and seconds<=86339) or (seconds >=0 and seconds <=1800) :
                                if sleep_check == 0:
                                    sleep_check +=1
                                    day_sleep_time()
                                else:
                                    continue
                            else:
                                sleep_check = 0

                color = green_color
            else: # standing
                standing_time = time.time()
                    nowStatus = status.standing
                    if sleeptime >= 10:
                        seconds = (pre_time.hour * 60 + pre_time.minute) * 60 + pre_time.second
                            sleep_time = seconds/3600
                            if seconds >= 14400 and seconds<=27000:
                                if wake_check == 0:
                                    wake_check +=1
                                    day_wake_time()
                                else:
                                    continue
                            else:
                                wake_check = 0
                        
                    color = blue_color
                    origin_time = 0
                    sleeptime=0

            
            label = str(nowStatus)[7:]
            font = cv2.FONT_HERSHEY_PLAIN
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 5)
            cv2.putText(img, label, (xmin, ymin - 5), font, 2, color, 5)
    cv2.imshow("frame", img)
    rawCapture.truncate(0)
    
    end_time = time.time()
    process_time = end_time - start_time
    print("=== A frame took {:.3f} seconds".format(process_time))
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cap.close()
        break
cv2.destroyAllWindows()
