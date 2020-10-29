import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import re
from tflite_runtime.interpreter import Interpreter
import image_processing.image_tf as image_tf
import image_processing.image_falldown as image_falldown
import image_processing.image_sleep as image_sleep
import image_processing.image_activity as image_activity

URL = 'http://13.125.221.213:5000/sensor'

global beforeStatus, nowStatus
beforeStatus = image_falldown.status.standing
nowStatus = image_falldown.status.standing

global BeforeCenterPointX, BeforeCenterPointY
BeforeCenterPointX = 0
BeforeCenterPointY = 0

def draw_rect(frame, xmin, ymin, xmax, ymax, nowStatus, color):
    label = str(nowStatus)[7:]
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 5)
    cv2.putText(frame, label, (xmin, ymin - 5), font, 2, color, 5)

min_confidence = 0.6
def main():
    global beforeStatus
    global BeforeCenterPointX, BeforeCenterPointY
    # Open cam
    cap = PiCamera()
    try:
        cap.framerate = 32
        cap.resolution = (320,240)
    except:
        print("cannot open cam")
    rawCapture = PiRGBArray(cap, size=(320, 240))
    rawCapture.truncate(0)
    interpreter = image_tf.load_interpreter()
    
    # Detecting objects
    for frame in cap.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        #start_time = time.time()
        img = np.asarray(frame.array)
        height, width, channels = img.shape
        img = cv2.resize(img, (300,300))
    
        outs = image_tf.detect_objects(interpreter, img, min_confidence)

        if not outs:
            print("nothing detected")
        for out in outs:
            if out['class_id'] == 0 and out['score'] > min_confidence:
                print("person detected")
                # Convert the bounding box figures from relative coordinates
                # to absolute coordinates based on the original resolution
                ymin, xmin, ymax, xmax = out['bounding_box']
                xmin = int(xmin * width)
                xmax = int(xmax * width)
                ymin = int(ymin * height)
                ymax = int(ymax * height)
                CenterPointX = int((xmin + xmax)/2)
                CenterPointY = int((ymin + ymax)/2)
                w = xmax - xmin
                h = ymax - ymin
                
                if w/2 > h: # fall down
                    nowStatus, color = image_falldown.falldown_process(beforeStatus)
                elif w > h: # lying
                    nowStatus, color = image_falldown.lying_process(beforeStatus)
                else: # standing
                    nowStatus, color = image_falldown.standing_process(beforeStatus)
                    image_activity.realtime_count(CenterPointX, CenterPointY, BeforeCenterPointX, BeforeCenterPointY) # calculate activity 
                beforeStatus = nowStatus
                draw_rect(img, xmin, ymin, xmax, ymax, nowStatus, color)
                # save now center point
                BeforeCenterPointX = CenterPointX
                BeforeCenterPointY = CenterPointY
        cv2.imshow("frame", img)
        rawCapture.truncate(0)
        #end_time = time.time()
        #process_time = end_time - start_time
        #print("=== A frame took {:.3f} seconds".format(process_time))
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            cap.close()
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
