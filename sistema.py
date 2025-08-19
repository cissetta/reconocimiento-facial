import tkinter as tk
from tkinter import messagebox
import datetime

# ===============================
# Funciones simuladas de cada equipo
# ===============================

# Equipo 1: Control Arduino
def control_arduino():
    # Simulación de recepción de mensaje desde Arduino
    mensaje = "CAPTURA"  
    mostrar_mensaje(f"Arduino envía: {mensaje}")

    if mensaje == "CAPTURAR":
        reconocimiento_facial()  # derivar al equipo 2

# Equipo 2: Reconocimiento Facial
def reconocimiento_facial():
    # Simulación de reconocimiento
    docente_reconocido = True  
    nombre = "Prof. García"

    if docente_reconocido:
        mostrar_mensaje(f"Docente reconocido: {nombre}")
        enviar_a_arduino("OPEN")
        registrar_acceso(nombre, "PERMITIDO")
    else:
        mostrar_mensaje("Acceso denegado: persona desconocida")
        enviar_a_arduino("DENY")
        registrar_acceso("DESCONOCIDO", "DENEGADO")

# Equipo 4: Base de Datos
def registrar_acceso(nombre, estado):
    # Simulación: guardar en BD (aquí solo mostramos en consola)
    hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mostrar_mensaje(f"Registro en BD -> Nombre: {nombre}, Estado: {estado}, Hora: {hora}")

# ===============================
# Funciones de comunicación
# ===============================

def enviar_a_arduino(mensaje):
    mostrar_mensaje(f"Enviado a Arduino: {mensaje}")

def mostrar_mensaje(texto):
    messagebox.showinfo("Sistema Central", texto)
    print(texto)

# ===============================
# Interfaz Tkinter - Menú principal
# ===============================

def main():
    root = tk.Tk()
    root.title("Equipo 3 – Sistema Central en Python")
    root.geometry("400x300")

    tk.Label(root, text="Menú Principal", font=("Arial", 16, "bold")).pack(pady=20)

    btn1 = tk.Button(root, text="1. Control Arduino (Equipo 1)", width=30, command=control_arduino)
    btn1.pack(pady=5)

    btn2 = tk.Button(root, text="2. Reconocimiento Facial (Equipo 2)", width=30, command=reconocimiento_facial)
    btn2.pack(pady=5)

    btn3 = tk.Button(root, text="3. Base de Datos (Equipo 4)", width=30, command=lambda: registrar_acceso("Test", "PERMITIDO"))
    btn3.pack(pady=5)

    btn4 = tk.Button(root, text="4. Salir", width=30, command=root.destroy)
    btn4.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
