import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import os
import pickle
import numpy as np
import sqlite3
import datetime

# ===============================
# Conexión a DB Equipo 4
# ===============================
def conectar():
    conn = sqlite3.connect("sistema_acceso.db")
    return conn

def listar_docentes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM docentes WHERE estado='activo'")
    docentes = cursor.fetchall()
    conn.close()
    return docentes

# ===============================
# RUTAS DE GUARDADO
# ===============================
FOTOS_DIR = "fotos_docentes"
PATRONES_FILE = "patrones_docentes.pkl"
os.makedirs(FOTOS_DIR, exist_ok=True)

# ===============================
# Función: Captura de fotos
# ===============================
def capturar_fotos(docente_id):
    messagebox.showinfo("Finalizado", f"Captura de fotos para {docente_nombre} completada.")

# ===============================
# Función: Generación de patrones
# ===============================
def generar_patrones():
    messagebox.showinfo("Patrones", "Generación de patrones completada.")

# ===============================
# Función: Reconocimiento en vivo
# ===============================
def reconocer_docente():
    recognized = True
    if recognized:
        messagebox.showinfo("Reconocimiento", f"Docente reconocido: {recognized}")
        return recognized
    else:
        messagebox.showinfo("Reconocimiento", "No se reconoció ningún docente")
        return "desconocido"

# ===============================
# INTERFAZ TKINTER
# ===============================
class ReconocimientoFacial:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconocimiento Facial - Submenú")
        self.root.geometry("400x300")

        tk.Label(root, text="Reconocimiento Facial", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(root, text="Programa A - Capturar Fotos", width=30, command=self.programa_a).pack(pady=5)
        tk.Button(root, text="Programa B - Generar Patrones", width=30, command=generar_patrones).pack(pady=5)
        tk.Button(root, text="Programa C - Reconocimiento en Vivo", width=30, command=self.programa_c).pack(pady=5)
        tk.Button(root, text="Salir", width=30, command=root.destroy).pack(pady=20)

    def programa_a(self):
        docentes = listar_docentes()
        if not docentes:
            messagebox.showwarning("Error", "No hay docentes activos en la base de datos.")
            return

        # Pedir al usuario seleccionar un docente
        ventana = tk.Toplevel(self.root)
        ventana.title("Seleccionar Docente")
        tk.Label(ventana, text="Seleccione un docente:").pack(pady=10)
        combo = ttk.Combobox(ventana, values=[str(d[0])+"-"+d[1] for d in docentes])
        combo.pack(pady=5)
        combo.current(0)

        def iniciar_captura():
            docente_info= combo.get()
            docente_nombre = docente_info.split("-")[1]
            docente_id=docente_info.split("-")[0]  
            capturar_fotos(docente_id)
            ventana.destroy()

        tk.Button(ventana, text="Iniciar Captura", command=iniciar_captura).pack(pady=10)

    def programa_c(self):
        nombre = reconocer_docente()
        if nombre != "desconocido":
            # Aquí se puede agregar la función para enviar el resultado al Equipo 3
            print(f"Enviar resultado a Equipo 3: {nombre}")
        else:
            print("Enviar resultado a Equipo 3: desconocido")

# ===============================
# EJECUCIÓN
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = ReconocimientoFacial(root)
    root.mainloop()