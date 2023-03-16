import cv2
from models import Yolov4
import time
import os

model1 = Yolov4(weight_path = 'yolov4.weights', 
               class_name_path = 'class_names/coco_classes.txt')

model = Yolov4(weight_path = 'yolov4-helmet-detection.weights', 
               class_name_path = 'class_names/yolov4_helmet_detection.txt')


ALERT = cv2.imread('descarga_rojo.jpg')
cap = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(0)
cv2.imshow('ALERTA, DETER OPERACIÓN', ALERT)
#cap = cv2.VideoCapture('video.mp4')

start_time = time.time()
print("Start Time: ", start_time)

detect_set = set()
time_temp = 0
time_unstable_temp = 0
current_time_unstable = 0
time_unstable_delay = 0
time_delay = 1
stopped = 0

correct_set1 = {'helmet'}
correct_set2 = set()
status = 'stop'
while True:

    #Frame read
    ret,frame = cap.read()
    ret2, frame2 = cap2.read()

    if not ret or not ret2:
        break
    #Object detetion in the frame using Yolov4

    pred = model.predict(frame)
    pred2 = model1.predict(frame2)

    detect_set = set()
    for index, row in pred.iterrows():
            class_name = row['class_name']
            if class_name == 'helmet':
                detect_set.add('helmet')
            elif class_name == 'person':
                detect_set.add('person')


    detect_set2 = set()
    for index, row in pred2.iterrows():
            class_name = row['class_name']
            if class_name == 'person':
                detect_set2.add('person')

        #Show frame with objects detected

    current_time = time.time()
    
    if (detect_set == correct_set1) and (detect_set2 == correct_set2):
        time_delay += time_unstable_delay
        
        time_unstable_delay = 0

        stopped = 0
        status =  'proceed'
        current_time_unstable = current_time
         

    else:
        status = 'stop'
        if not stopped:

            stopped = 1
            start_time_temp = current_time
        time_unstable_delay = current_time - start_time_temp

    cv2.imshow('planta', model.output_img)
    cv2.imshow('robot', model1.output_img)
    
    elapsed_time = current_time - start_time
    elapsed_time_unstable = elapsed_time - time_delay - time_unstable_delay

    if elapsed_time > time_temp:
        os.system('cls')

        time_temp +=1
        
        if status == 'proceed':
             
            print("CONTINUA LA OPERACION")
            try:
                cv2.destroyWindow('ALERTA, DETER OPERACIÓN')
            except:
                 pass
        else: 
            print("DETENER OPERACION")
            cv2.imshow('ALERTA, DETER OPERACIÓN', ALERT)


        print("TIEMPO REAL: ",time_temp) 
        print("TIEMPO EN OPERACIÓN: ",elapsed_time_unstable)

    if cv2.waitKey(1) == ord('q'):
        break
         
cap.release()
cv2.destroyAllWindows()

cv2.waitKey(0)
cv2.destroyAllWindows()