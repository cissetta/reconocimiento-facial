import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import datetime

# ===============================
# Conexión y creación de tablas
# ===============================
def conectar():
    conn = sqlite3.connect("sistema_acceso.db")
    return conn

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS docentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        foto TEXT,
        estado TEXT CHECK(estado IN ('activo', 'inactivo')) DEFAULT 'activo'
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accesos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        docente_id INTEGER,
        fecha TEXT,
        autorizado TEXT CHECK(autorizado IN ('SI', 'NO')),
        FOREIGN KEY(docente_id) REFERENCES docentes(id)
    )
    """)

    conn.commit()
    conn.close()

crear_tablas()

# ===============================
# FUNCIONES DOCENTES
# ===============================
def agregar_docente(nombre, foto, estado="activo"):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO docentes (nombre, foto, estado) VALUES (?, ?, ?)",
                   (nombre, foto, estado))
    conn.commit()
    conn.close()

def listar_docentes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM docentes")
    docentes = cursor.fetchall()
    conn.close()
    return docentes

def modificar_docente(id_docente, nombre=None, foto=None, estado=None):
    conn = conectar()
    cursor = conn.cursor()
    if nombre:
        cursor.execute("UPDATE docentes SET nombre=? WHERE id=?", (nombre, id_docente))
    if foto:
        cursor.execute("UPDATE docentes SET foto=? WHERE id=?", (foto, id_docente))
    if estado:
        cursor.execute("UPDATE docentes SET estado=? WHERE id=?", (estado, id_docente))
    conn.commit()
    conn.close()

def eliminar_docente(id_docente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM docentes WHERE id=?", (id_docente,))
    conn.commit()
    conn.close()

# ===============================
# FUNCIONES ACCESOS
# ===============================
def registrar_acceso(docente_id, autorizado):
    conn = conectar()
    cursor = conn.cursor()
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO accesos (docente_id, fecha, autorizado) VALUES (?, ?, ?)",
                   (docente_id, fecha, autorizado))
    conn.commit()
    conn.close()

def listar_accesos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT a.id, d.nombre, a.fecha, a.autorizado
    FROM accesos a
    JOIN docentes d ON a.docente_id = d.id
    ORDER BY a.fecha DESC
    """)
    accesos = cursor.fetchall()
    conn.close()
    return accesos


# ===============================
# INTERFAZ TKINTER
# ===============================
class SistemaDB:
    def __init__(self, root):
        self.root = root
        self.root.title("Equipo 4 – Base de Datos")
        self.root.geometry("600x400")

        tk.Label(root, text="Gestión de Docentes y Accesos", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(root, text="CRUD Docentes", width=25, command=self.ventana_docentes).pack(pady=5)
        tk.Button(root, text="Registrar/Listar Accesos", width=25, command=self.ventana_accesos).pack(pady=5)

    # ---------------------------
    # Ventana CRUD Docentes
    # ---------------------------
    def ventana_docentes(self):
        win = tk.Toplevel(self.root)
        win.title("CRUD Docentes")
        win.geometry("700x400")

        # Lista
        self.tree_docentes = ttk.Treeview(win, columns=("ID","Nombre","Foto","Estado"), show="headings")
        self.tree_docentes.column("ID",  width=20)
        self.tree_docentes.column("Estado",  width=20)
        self.tree_docentes.heading("ID", text="ID")
        self.tree_docentes.heading("Nombre", text="Nombre")
        self.tree_docentes.heading("Foto", text="Foto")
        self.tree_docentes.heading("Estado", text="Estado")
        self.tree_docentes.pack(fill="both", expand=True)

        # Formulario
        frm = tk.Frame(win)
        frm.pack(pady=10)

        tk.Label(frm, text="Nombre:").grid(row=0, column=0)
        self.entry_nombre = tk.Entry(frm)
        self.entry_nombre.grid(row=0, column=1)

        tk.Label(frm, text="Foto:").grid(row=1, column=0)
        self.entry_foto = tk.Entry(frm)
        self.entry_foto.grid(row=1, column=1)
        tk.Button(frm, text="Examinar", command=self.seleccionar_foto).grid(row=1, column=2)

        tk.Label(frm, text="Estado:").grid(row=2, column=0)
        self.combo_estado = ttk.Combobox(frm, values=["activo","inactivo"])
        self.combo_estado.grid(row=2, column=1)
        self.combo_estado.current(0)

        tk.Button(frm, text="Agregar", command=self.agregar_docente_gui).grid(row=3, column=0, pady=5)
        tk.Button(frm, text="Modificar", command=self.modificar_docente_gui).grid(row=3, column=1)
        tk.Button(frm, text="Eliminar", command=self.eliminar_docente_gui).grid(row=3, column=2)
        tk.Button(frm, text="Actualizar Lista", command=self.cargar_docentes).grid(row=3, column=3)

        self.cargar_docentes()

    def seleccionar_foto(self):
        archivo = filedialog.askopenfilename(filetypes=[("Imagen", "*.jpg *.png")])
        if archivo:
            self.entry_foto.delete(0, tk.END)
            self.entry_foto.insert(0, archivo)

    def cargar_docentes(self):
        for i in self.tree_docentes.get_children():
            self.tree_docentes.delete(i)
        for d in listar_docentes():
            self.tree_docentes.insert("", tk.END, values=d)

    def agregar_docente_gui(self):
        nombre = self.entry_nombre.get()
        foto = self.entry_foto.get()
        estado = self.combo_estado.get()
        if nombre:
            agregar_docente(nombre, foto, estado)
            self.cargar_docentes()
        else:
            messagebox.showwarning("Error", "Ingrese un nombre")

    def modificar_docente_gui(self):
        selected = self.tree_docentes.selection()
        if selected:
            item = self.tree_docentes.item(selected)
            id_docente = item["values"][0]
            nombre = self.entry_nombre.get()
            foto = self.entry_foto.get()
            estado = self.combo_estado.get()
            modificar_docente(id_docente, nombre, foto, estado)
            self.cargar_docentes()
        else:
            messagebox.showwarning("Error", "Seleccione un docente")

    def eliminar_docente_gui(self):
        selected = self.tree_docentes.selection()
        if selected:
            item = self.tree_docentes.item(selected)
            id_docente = item["values"][0]
            eliminar_docente(id_docente)
            self.cargar_docentes()
        else:
            messagebox.showwarning("Error", "Seleccione un docente")

    # ---------------------------
    # Ventana CRUD Accesos
    # ---------------------------
    def ventana_accesos(self):
        win = tk.Toplevel(self.root)
        win.title("Accesos")
        win.geometry("700x400")

        # Lista
        self.tree_accesos = ttk.Treeview(win, columns=("ID","Docente","Fecha","Autorizado"), show="headings")
        self.tree_accesos.heading("ID", text="ID")
        self.tree_accesos.heading("Docente", text="Docente")
        self.tree_accesos.heading("Fecha", text="Fecha")
        self.tree_accesos.heading("Autorizado", text="Autorizado")

        self.tree_accesos.pack(fill="both", expand=True)

                # Formulario
        frm = tk.Frame(win)
        frm.pack(pady=10)

        tk.Label(frm, text="Docente ID:").grid(row=0, column=0)
        self.entry_docente_id = tk.Entry(frm)
        self.entry_docente_id.grid(row=0, column=1)

        tk.Label(frm, text="Autorizado:").grid(row=1, column=0)
        self.combo_autorizado = ttk.Combobox(frm, values=["SI","NO"])
        self.combo_autorizado.grid(row=1, column=1)
        self.combo_autorizado.current(0)

        tk.Button(frm, text="Registrar Acceso", command=self.registrar_acceso_gui).grid(row=2, column=0, pady=5)
        tk.Button(frm, text="Actualizar Lista", command=self.cargar_accesos).grid(row=2, column=1)

        self.tree_accesos.bind("<Double-1>", self.on_double_click)

        self.cargar_accesos()

    def on_double_click(self):
        selected = self.tree_docentes.selection()
        print("pass")
        if selected:
            print("pass")
            

    def registrar_acceso_gui(self):
        docente_id = self.entry_docente_id.get()
        autorizado = self.combo_autorizado.get()
        if docente_id.isdigit():
            registrar_acceso(int(docente_id), autorizado)
            self.cargar_accesos()
        else:
            messagebox.showwarning("Error", "Ingrese un ID válido")

    def cargar_accesos(self):
        for i in self.tree_accesos.get_children():
            self.tree_accesos.delete(i)
        for a in listar_accesos():
            self.tree_accesos.insert("", tk.END, values=a)

# ===============================
# EJECUCIÓN
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaDB(root)
    root.mainloop()
