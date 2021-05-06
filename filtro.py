import cv2
import imutils

# Capturar video, cambiar parametros segun nuestra camara
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

#Imagen a añadir/sobreponer
image = cv2.imread('sidd.png', cv2.IMREAD_UNCHANGED)

# Detector de rostros
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

eje = 0
