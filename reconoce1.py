
import cv2
import os


def crear_dataset(nombre_persona, num_muestras=100):
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    carpeta = f'dataset/{nombre_persona}'
    os.makedirs(carpeta, exist_ok=True)
    camara = cv2.VideoCapture(0)
    contador = 0

    while True:
        ret, frame = camara.read()
        if not ret:
            break
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rostros = detector.detectMultiScale(gris, 1.3, 5)

        for (x, y, w, h) in rostros:
            rostro = gris[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (200, 200))
            cv2.imwrite(f"{carpeta}/{contador}.jpg", rostro)
            contador += 1

        cv2.imshow('Recolectando rostros', frame)

        if cv2.waitKey(1) == 27 or contador >= num_muestras:  # Tecla ESC
            break

    camara.release()
    cv2.destroyAllWindows()

# Ejemplo de uso
#crear_dataset("isa", num_muestras=50)
