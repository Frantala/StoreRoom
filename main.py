import sqlite3
import cv2
from pyzbar.pyzbar import decode
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import ttk as ttk_widgets
import pandas as pd
import openpyxl
import datetime
from tkinter import filedialog
from datetime import datetime


# Crear o conectar a una base de datos
conn = sqlite3.connect('Proyecto-Escuela')
# Crear un cursor
c = conn.cursor()
# Crear tabla para la base de datos (si no existe)
c.execute("""CREATE TABLE IF NOT EXISTS Registros (
    Alumno text,
    Profesor text,
    Curso text,
    Herramientas text,
    Fecha text
)""")

# Añadir la columna timestamp si no existe
try:
    c.execute("ALTER TABLE Registros ADD COLUMN timestamp TEXT")
    conn.commit()
except sqlite3.OperationalError:
    # La columna ya existe
    pass
# Guardar los cambios y cerrar la conexión inicial
conn.commit()
conn.close()

def agregar():
    conn = sqlite3.connect('Proyecto-Escuela')
    c = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO Registros (Alumno, Profesor, Curso, Herramientas) VALUES (?, ?, ?, ?, ?)", (
        alumno.get(),
        profesor.get(),
        curso.get(),
        herramientas.get("1.0", END).strip(),
        fecha_actual
    ))
    conn.commit()
    conn.close()
    alumno.delete(0, END)
    profesor.delete(0, END)
    curso.delete(0, END)
    herramientas.delete("1.0", END)
    messagebox.showinfo("Registro exitoso", "Datos guardados correctamente")
    mostrar_registros()

def mostrar_registros():
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect('Proyecto-Escuela')
    c = conn.cursor()
    c.execute("SELECT rowid, Alumno, Profesor, Curso, Herramientas, Fecha FROM Registros")
    registros = c.fetchall()
    for registro in registros:
        tree.insert("", END, values=registro)
    conn.close()

def eliminar():
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar")
        return
    respuesta = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar este registro?")
    if respuesta:
        item = tree.item(seleccionado)
        registro_id = item['values'][0]
        conn = sqlite3.connect('Proyecto-Escuela')
        c = conn.cursor()
        c.execute("DELETE FROM Registros WHERE rowid = ?", (registro_id,))
        conn.commit()
        conn.close()
        tree.delete(seleccionado)
        messagebox.showinfo("Eliminación exitosa", "Registro eliminado correctamente")
        mostrar_registros()

def cargar_registro(event):
    seleccionado = tree.selection()
    if seleccionado:
        item = tree.item(seleccionado)
        registro_id = item['values'][0]
        alumno.delete(0, END)
        alumno.insert(END, item['values'][1])
        profesor.delete(0, END)
        profesor.insert(END, item['values'][2])
        curso.delete(0, END)
        curso.insert(END, item['values'][3])
        herramientas.delete("1.0", END)
        herramientas.insert(END, item['values'][4])
        boton_editar.config(state=NORMAL)
        boton_editar.config(command=lambda: editar_registro(registro_id))

def editar_registro(registro_id):
    conn = sqlite3.connect('Proyecto-Escuela')
    c = conn.cursor()
    c.execute("UPDATE Registros SET Alumno = ?, Profesor = ?, Curso = ?, Herramientas = ? WHERE rowid = ?", (
        alumno.get(),
        profesor.get(),
        curso.get(),
        herramientas.get("1.0", END).strip(),
        registro_id
    ))
    conn.commit()
    conn.close()
    alumno.delete(0, END)
    profesor.delete(0, END)
    curso.delete(0, END)
    herramientas.delete("1.0", END)
    messagebox.showinfo("Actualización exitosa", "Datos actualizados correctamente")
    mostrar_registros()
    boton_editar.config(state=DISABLED)

# LE AGREGAMOS LA FUNCIONALIDAD DE DETECTAR QRs A LA APLICACION 
# creamos una funcion para eso
def scan_qr():
    def decode_qr(frame):
        qr_codes = decode(frame)
        for qr in qr_codes:
            qr_data = qr.data.decode("utf-8")
            x, y, w, h = qr.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            return qr_data
        return None

    cap = cv2.VideoCapture(0) 
    herramientas_qr = []
    while True: # Creamos un bucle que mientras este sea igual a True va a leer los frames de la camara
        ret, frame = cap.read()
        if not ret:
            break

        herramienta = decode_qr(frame)
        if herramienta and herramienta not in herramientas_qr:
            herramientas_qr.append(herramienta)
            herramientas.insert(END, herramienta)

        cv2.imshow("Escanear QR", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): #Esto le da la orden de como sacar la camara
            break

    cap.release()
    cv2.destroyAllWindows()

# Funcion para filtrar los registros en la tabla
def filtrar_registros():
    filtro = filtrar.get().strip() #los obtenemos y lo ordenamos 
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect('Proyecto-Escuela')
    c = conn.cursor()
    c.execute("SELECT rowid, Alumno, Profesor, Curso, Herramientas FROM Registros WHERE Alumno LIKE ? OR Profesor LIKE ? OR Curso LIKE ? OR Herramientas LIKE ?", ('%' + filtro + '%', '%' + filtro + '%', '%' + filtro + '%', '%' + filtro + '%'))
    registros = c.fetchall()
    for registro in registros:
        tree.insert("", END, values=registro)
    conn.close()


# Funcion para pasar todos los datos guardados en la treeview a un excel 
def pasar_excel():
    # Obtener los datos de la Treeview
    registros = []
    for row_id in tree.get_children():
        row = tree.item(row_id)['values']
        registros.append(row)
    
    # Verificar si hay datos en la Treeview
    if not registros:
        messagebox.showwarning("Sin Datos", "No hay datos para exportar.")
        return
    
    # Convertir los datos en un DataFrame de pandas
    df = pd.DataFrame(registros, columns=["ID", "Alumno", "Profesor", "Curso", "Herramientas", "Fecha"])
    
    # Abrir un diálogo para guardar el archivo
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    
    if file_path:
        # Guardar el DataFrame como un archivo Excel
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Exportación Exitosa", f"Los datos han sido exportados a {file_path}")

    # Creamos funcion para eliminar todo del registro de una sola vez
def eliminar_todo():
        elimnar = tree.delete()
        respuesta = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar todos los registros?")
        if respuesta:
            conn = sqlite3.connect('Proyecto-Escuela')
            c = conn.cursor()
            c.execute("DELETE  FROM Registros")
            conn.commit()
            conn.close()
            tree.delete(*tree.get_children())
            conn.close()


# Crear la ventana principal
app = Tk()
app.title("StoreRoom")
app.geometry("1200x800")  # Resolución inicial más amplia para centrar mejor el contenido

# Crear un contenedor para el canvas y el scrollbar
main_frame = Frame(app)
main_frame.pack(fill=BOTH, expand=1)

# Crear un canvas
canvas = Canvas(main_frame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Crear un scrollbar y asociarlo con el canvas
scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)

# Crear un frame dentro del canvas para contener todos los widgets
content_frame = Frame(canvas)

# Crear una ventana en el canvas para contener el content_frame
canvas.create_window((0, 0), window=content_frame, anchor="n", width=canvas.winfo_width())  # Centramos usando "n"

# Actualizar el área de scroll según el contenido
content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Ajustar el canvas al tamaño del content_frame
canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas.create_window((canvas.winfo_width()/2, 0), window=content_frame, anchor="n"), width=canvas.winfo_width()))

# Contenido de la app
titulo = Label(content_frame, text="REGISTRO DE HERRAMIENTAS", fg="black", font=("helvetica", 20, "bold"), pady=10)
titulo.grid(row=0, column=0, columnspan=3, pady=10)

# Marco de datos del estudiante
marco = LabelFrame(content_frame, text="Datos del Estudiante", font=("helvetica", 20, "bold"), pady=5)
marco.config(bd=2)
marco.grid(row=1, column=0, pady=10, padx=20, sticky="n")

# Campos dentro del marco de datos del estudiante
lbl_alumno = Label(marco, text="Alumno", font=("helvetica", 15, "bold"))
lbl_alumno.grid(row=1, column=0, sticky="w", pady=5, padx=8)
alumno = Entry(marco, width=40, border=5, font=("helvetica", 12))
alumno.grid(row=1, column=1, pady=5, padx=10)
alumno.focus()

lbl_profesor = Label(marco, text="Profesor", font=("helvetica", 15, "bold"))
lbl_profesor.grid(row=2, column=0, sticky="w", pady=5, padx=8)
profesor = Entry(marco, width=40, border=5, font=("helvetica", 12))
profesor.grid(row=2, column=1, pady=5, padx=10)

lbl_curso = Label(marco, text="Curso", font=("helvetica", 15, "bold"))
lbl_curso.grid(row=3, column=0, sticky="w", pady=5, padx=8)
curso = Entry(marco, width=40, border=5, font=("helvetica", 12))
curso.grid(row=3, column=1, pady=5, padx=10)

# Botón para guardar en Excel
btn_excel = Button(content_frame, text="Guardar como Excel", height=2, width=18, font=("helvetica", 15), bg="green", fg="white", command=pasar_excel)
btn_excel.grid(column=0, row=1, sticky="e", padx=50, pady=10)

# Marco de herramientas a llevar
marco_herramientas = LabelFrame(content_frame, text="Herramientas a llevar", font=("helvetica", 20, "bold"), pady=5)
marco_herramientas.config(bd=2)
marco_herramientas.grid(row=3, column=0, pady=20, padx=20, sticky="n")

lbl_herramientas = Label(marco_herramientas, text="Herramientas", font=("helvetica", 15, "bold"))
lbl_herramientas.grid(row=1, column=0, pady=5, padx=8)
herramientas = Text(marco_herramientas, width=30, height=10, font=("helvetica", 12), border=5)
herramientas.grid(row=1, column=1, padx=15, pady=10)
boton_qr = Button(marco_herramientas, text="Escanear QR", font=("helvetica", 12), border=5, bg="gray", fg="white", command=scan_qr)
boton_qr.grid(row=2, column=1, padx=15, pady=10)

# Frame de botones
frame_botones = LabelFrame(content_frame)
frame_botones.grid(row=4, column=0, pady=10, sticky="n")

boton_registrar = Button(frame_botones, text="AGREGAR", height=2, width=15, font=("helvetica", 12), bg="green", fg="white", command=agregar)
boton_registrar.grid(row=0, column=0)
boton_editar = Button(frame_botones, text="EDITAR", height=2, width=15, font=("helvetica", 12), bg="gray", fg="white", state=DISABLED)
boton_editar.grid(row=0, column=1)
boton_eliminar = Button(frame_botones, text="ELIMINAR", width=15, height=2, font=("helvetica", 12), bg="red", fg="white", command=eliminar)
boton_eliminar.grid(row=0, column=2)

# Frame para filtrar registros
frame_filtrar = LabelFrame(content_frame, width=50, height=50)
frame_filtrar.grid(row=5, column=0, pady=15, sticky="n")

lbl_filtrar = Label(frame_filtrar, text="Buscar Registros", font=("helvetica", 12))
lbl_filtrar.grid(row=0, column=0)
filtrar = Entry(frame_filtrar, width=50, font=("helvetica", 10), borderwidth=5)
filtrar.grid(row=0, column=1, padx=10)
btn_filtrar = Button(frame_filtrar, text="Buscar", font=("helvetica", 12), command=filtrar_registros)
btn_filtrar.grid(row=0, column=2, padx=10)

# dentro de este frame de filtrar ponemos un boton al lado para eliminar todo los registros de una sola vez
btn_eliminar_todo = Button(frame_filtrar, text="Eliminar Todo", font=("helvetica", 12), bg="blue", fg="white", command=eliminar_todo)
btn_eliminar_todo.grid(row=0, column=4, padx=5) # aca le damos un padding en x para que tenga mas esapacio 

# Tabla de registros
tree = ttk.Treeview(content_frame, columns=("ID", "Alumno", "Profesor", "Curso", "Herramientas"), show="headings", height=20)
tree.heading("ID", text="ID")
tree.heading("Alumno", text="Alumno")
tree.heading("Profesor", text="Profesor")
tree.heading("Curso", text="Curso")
tree.heading("Herramientas", text="Herramientas")
tree.heading("Fecha", text="Fecha")
tree.column("ID", width=30)
tree.column("Alumno", width=200)
tree.column("Profesor", width=200)
tree.column("Curso", width=150)
tree.column("Herramientas", width=300)
tree.column("Fecha", width=200)
tree.grid(row=6, column=0, pady=20, sticky="n")

tree.bind("<Double-1>", cargar_registro)

# Llamar a la función que muestra los registros en la tabla
mostrar_registros()

# Hacer que el frame principal se ajuste al tamaño de la ventana
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

content_frame.grid_rowconfigure(0, weight=1)
content_frame.grid_columnconfigure(0, weight=1)

app.mainloop()