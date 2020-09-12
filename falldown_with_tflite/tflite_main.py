import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import re
from tflite_runtime.interpreter import Interpreter
import tflite_tf
import tflite_falldown

#time_URL = 'http://13.125.221.213:5000/wake_up'

sleep_check = 0
wake_check = 0

global beforeStatus, nowStatus
beforeStatus = tflite_falldown.status.standing
nowStatus = tflite_falldown.status.standing

def draw_rect(frame, xmin, ymin, xmax, ymax, nowStatus, color):
    label = str(nowStatus)[7:]
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 5)
    cv2.putText(frame, label, (xmin, ymin - 5), font, 2, color, 5)

min_confidence = 0.6
def main():
    global beforeStatus
    # Open cam
    cap = PiCamera()
    try:
        cap.framerate = 32
        cap.resolution = (320,240)
    except:
        print("cannot open cam")
    rawCapture = PiRGBArray(cap, size=(320, 240))
    rawCapture.truncate(0)
    interpreter = tflite_tf.load_interpreter()
    
    # Detecting objects
    for frame in cap.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        #start_time = time.time()
        img = np.asarray(frame.array)
        height, width, channels = img.shape
        img = cv2.resize(img, (300,300))
    
        outs = tflite_tf.detect_objects(interpreter, img, min_confidence)

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
                    nowStatus, color = tflite_falldown.falldown_process(beforeStatus)
                elif w > h: # lying
                    nowStatus, color = tflite_falldown.lying_process(beforeStatus)
                else: # standing
                    nowStatus, color = tflite_falldown.standing_process(beforeStatus)
                beforeStatus = nowStatus
                draw_rect(img, xmin, ymin, xmax, ymax, nowStatus, color)
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
