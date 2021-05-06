import cv2
import imutils

# Videostreaming o video de entrada
cap = cv2.VideoCapture('rtsp://192.168.0.10:8080/playlist.m3u',cv2.CAP_DSHOW)

# Lectura de la imagen a incrustar en el video
image = cv2.imread('sidd.png', cv2.IMREAD_UNCHANGED)

# Detector de rostros
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

eje = 0

while True:

    ret, frame = cap.read()
    if ret == False: break
    #resolucion de la ventana
    frame = imutils.resize(frame, width=848)

    # Detección de los rostros presentes en el fotograma
    faces = faceClassif.detectMultiScale(frame, 1.3, 5)

    for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),2)
        
        
        # Redimensionar la imagen de entrada de acuerdo al ancho del
        # rostro detectado
        resized_image = imutils.resize(image, width=w)
        #cv2.imshow('frome',resized_image)
        filas_image = resized_image.shape[0]
        #print("filas_image ",resized_image.shape[0])
        col_image = w

        # Determinar una porción del alto de la imagen de entrada 
        # redimensionada
        
        #porcion_alto = filas_image //4 
        porcion_alto = 0
        
        #print(porcion_alto)
        dif = 0
        
        yi = y + porcion_alto + eje 
        yf = y + porcion_alto + filas_image + eje
        
        # Si existe suficiente espacio sobre el rostro detectado
        # para insertar la imagen de entrada resimensionada
        # se visualizará dicha imagen
        if yi >= 0:

            # Tomamos la sección de frame, en donde se va a ubicar
            # el gorro/tiara
            n_frame = frame[yi : yf, x : x + col_image]
        else:
            # Determinamos la sección de la imagen que excede a la del video
            dif = abs(yi) 
            # Tomamos la sección de frame, en donde se va a ubicar
            # el gorro/tiara
            n_frame = frame[0 : yf, x : x + col_image]

        # Determinamos la máscara que posee la imagen de entrada
        # redimensionada y también la invertimos
        mask = resized_image[:, :, 3]
        mask_inv = cv2.bitwise_not(mask)
            
        # Creamos una imagen con fondo negro y el gorro/tiara/2021
        # Luego creamos una imagen en donde en el fondo esté frame
        # y en negro el gorro/tiara/2021
        bg_black = cv2.bitwise_and(resized_image, resized_image, mask=mask)
        bg_black = bg_black[dif:, :, 0:3]
        bg_frame = cv2.bitwise_and(n_frame, n_frame, mask=mask_inv[dif:,:])

        # Sumamos las dos imágenes obtenidas
        result = cv2.add(bg_black, bg_frame)
        if yi >= 0:
            frame[yi : yf, x : x + col_image] = result

        else:
            frame[0 : yf, x : x + col_image] = result

    cv2.imshow('frame',frame)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()