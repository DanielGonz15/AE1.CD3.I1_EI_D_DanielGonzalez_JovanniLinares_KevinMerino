import cv2
import numpy as np
import imutils
import os
Datos = 'CruzBilletes50'
if not os.path.exists(Datos):
    print('Carpeta creada: ',Datos)
    os.makedirs(Datos)
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
x1, y1 = 100, 150
x2, y2 = 490, 398
count = 0
while True:
    ret, frame = cap.read()
    if ret == False: break
    imAux = frame.copy()
    cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
    objeto = imAux[y1:y2,x1:x2]
    #objeto = imutils.resize(objeto,width=38)
    #print(objeto.shape)
    k = cv2.waitKey(1)
    if k == ord('s'):
        cv2.imwrite(Datos+'/cruzBillete50{}.jpg'.format(count),objeto)
        print('Imagen guardada:'+'/caraBillete200{}.jpg'.format(count))
        count = count +1
    if k == ord('q'):
        break
    cv2.imshow('frame',frame)
    cv2.imshow('objeto',objeto)
cap.release()
cv2.destroyAllWindows()