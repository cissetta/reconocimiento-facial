import tkinter as tk
from tkinter import messagebox
import datetime
import serial
from crud_docentes import SistemaDB


class SistemaCentral:
    def __init__(self, root):
        self.root = root
        self.root.title("Equipo 3 – Sistema Central en Python")

        # Dimensiones de la ventana
        ancho_ventana = 400
        alto_ventana = 300
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Interfaz gráfica
        self._crear_interfaz()

    # ===============================
    # Métodos de interfaz
    # ===============================
    def _crear_interfaz(self):
        tk.Label(self.root, text="Menú Principal", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self.root, text="1. Control Arduino (Equipo 1)", width=30,
                  command=self.control_arduino).pack(pady=5)

        tk.Button(self.root, text="2. Reconocimiento Facial (Equipo 2)", width=30,
                  command=self.reconocimiento_facial).pack(pady=5)

        tk.Button(self.root, text="3. Base de Datos (Equipo 4)", width=30,
                  command=self.registrar_docentes).pack(pady=5)

        tk.Button(self.root, text="4. Salir", width=30,
                  command=self.root.destroy).pack(pady=20)

    # ===============================
    # Métodos simulados de cada equipo
    # ===============================
    def control_arduino(self):
        mensaje = "CAPTURA"  # Simulación
        self.mostrar_mensaje(f"Arduino envía: {mensaje}")
        arduino = serial.Serial('COM3', 9600) 
        print("⏳ Esperando botón (Arduino enviará señal)...")
        while True:
            if arduino.in_waiting > 0:
                dato = arduino.readline().decode().strip()
                if dato == "CAPTURAR":  # Arduino envía esto cuando se aprieta el botón
                    print("📸 Capturando imagen...")
                    autorizado = False

                    if not autorizado:
                        print("❌ Acceso denegado")
                        registrar_acceso(None, "DESCONOCIDO", 0)
                        arduino.write(b"DENY\n")
        if mensaje == "CAPTURA":
            self.reconocimiento_facial()

    def reconocimiento_facial(self):
        docente_reconocido = True
        nombre = "Prof. García"

        if docente_reconocido:
            self.mostrar_mensaje(f"Docente reconocido: {nombre}")
            self.enviar_a_arduino("OPEN")
            self.registrar_acceso(nombre, "PERMITIDO")
        else:
            self.mostrar_mensaje("Acceso denegado: persona desconocida")
            self.enviar_a_arduino("DENY")
            self.registrar_acceso("DESCONOCIDO", "DENEGADO")

    def registrar_docentes(self):
        root1 = tk.Toplevel(self.root)  # 🔑 Usamos Toplevel en lugar de Tk()
        app = SistemaDB(root1)

    # ===============================
    # Comunicación
    # ===============================
    def enviar_a_arduino(self, mensaje):
        self.mostrar_mensaje(f"Enviado a Arduino: {mensaje}")

    def mostrar_mensaje(self, texto):
        messagebox.showinfo("Sistema Central", texto)

    # ===============================
    # Registro de accesos
    # ===============================
    def registrar_acceso(self, nombre, estado):
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{fecha_hora}] {nombre} - {estado}")


# ===============================
# Programa principal
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaCentral(root)
    root.mainloop()