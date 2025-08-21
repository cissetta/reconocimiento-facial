import cv2
#import mediapipe as mp
import numpy as np
import sqlite3
from datetime import datetime

# Inicializar Mediapipe
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh

# ------------------ BASE DE DATOS ------------------
conn = sqlite3.connect("sistema_acceso.db")
cursor = conn.cursor()


# ------------------ FUNCIONES ------------------

# Guardar acceso
def registrar_acceso(docente_id, nombre, autorizado):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO accesos (docente_id, nombre, fecha, autorizado) VALUES (?, ?, ?, ?)",
                   (docente_id, nombre, fecha, autorizado))
    conn.commit()

# Convertir embedding a binario para la DB
def embedding_to_blob(embedding):
    return embedding.tobytes()

def blob_to_embedding(blob):
    return np.frombuffer(blob, dtype=np.float32)

# Calcular "embedding" simple de un rostro (con face mesh: puntos faciales)
def calcular_embedding(face_landmarks):
    coords = []
    for lm in face_landmarks.landmark:
        coords.append([lm.x, lm.y, lm.z])
    embedding = np.array(coords, dtype=np.float32).flatten()
    return embedding / np.linalg.norm(embedding)  # normalizamos

# Comparar embeddings (distancia coseno)
def comparar_embeddings(emb1, emb2, threshold=0.3):
    sim = np.dot(emb1, emb2)
    return sim > (1 - threshold)

# ------------------ CAPTURA Y RECONOCIMIENTO ------------------

def reconocimiento():
    cap = cv2.VideoCapture(0)

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as face_mesh:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                embedding_actual = calcular_embedding(face_landmarks)

                # Buscar coincidencia en la DB
                cursor.execute("SELECT id, nombre, embedding FROM docentes")
                docentes = cursor.fetchall()

                nombre = "desconocido"
                autorizado = "DENEGADO"
                docente_id = None

                for d_id, d_nombre, d_embedding in docentes:
                    emb_guardado = blob_to_embedding(d_embedding)
                    if comparar_embeddings(embedding_actual, emb_guardado):
                        nombre = d_nombre
                        autorizado = "OPEN"
                        docente_id = d_id
                        break

                registrar_acceso(docente_id, nombre, autorizado)

                color = (0,255,0) if autorizado == "OPEN" else (0,0,255)
                cv2.putText(frame, f"{autorizado} - {nombre}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            else:
                registrar_acceso(None, "desconocido", "DENEGADO")
                cv2.putText(frame, "DENEGADO - desconocido", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            cv2.imshow("Acceso con reconocimiento", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

# ------------------ AGREGAR NUEVOS DOCENTES ------------------

def agregar_docente(nombre):
    cap = cv2.VideoCapture(0)
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as face_mesh:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                embedding = calcular_embedding(face_landmarks)

                cursor.execute("INSERT INTO docentes (nombre, embedding) VALUES (?, ?)",
                               (nombre, embedding_to_blob(embedding)))
                conn.commit()
                print(f"✅ Docente {nombre} agregado a la base")
                break

            cv2.imshow("Captura para nuevo docente", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

# ------------------ USO ------------------
# 👉 Primero agrega docentes:
# agregar_docente("Pia")
# agregar_docente("Eliana")

# 👉 Luego corre el sistema:
# reconocimiento()


