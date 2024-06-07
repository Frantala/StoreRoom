import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Crear o conectar a una base de datos
conn = sqlite3.connect('Proyecto-Escuela')
# Crear un cursor
c = conn.cursor()
# Crear tabla para la base de datos (si no existe)
c.execute("""CREATE TABLE IF NOT EXISTS Registros (
    Alumno text,
    Profesor text,
    Curso text,
    Herramientas text
)""")
# Guardar los cambios y cerrar la conexión inicial
conn.commit()
conn.close()

def agregar():
    conn = sqlite3.connect('Proyecto-Escuela')
    c = conn.cursor()
    c.execute("INSERT INTO Registros (Alumno, Profesor, Curso, Herramientas) VALUES (?, ?, ?, ?)", (
        nombre_apellido.get(),
        profesor.get(),
        curso.get(),
        herramientas.get("1.0", END).strip()
    ))
    conn.commit()
    conn.close()
    nombre_apellido.delete(0, END)
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
    c.execute("SELECT rowid, Alumno, Profesor, Curso, Herramientas FROM Registros")
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
        nombre_apellido.delete(0, END)
        nombre_apellido.insert(END, item['values'][1])
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
        nombre_apellido.get(),
        profesor.get(),
        curso.get(),
        herramientas.get("1.0", END).strip(),
        registro_id
    ))
    conn.commit()
    conn.close()
    nombre_apellido.delete(0, END)
    profesor.delete(0, END)
    curso.delete(0, END)
    herramientas.delete("1.0", END)
    messagebox.showinfo("Actualización exitosa", "Datos actualizados correctamente")
    mostrar_registros()
    boton_editar.config(state=DISABLED)


app = Tk()
app.title("Registro de Herramientas")

titulo = Label(app, text="REGISTRO DE HERRAMIENTAS", fg="black", font=("helvetica", 17, "bold"), pady=10)
titulo.pack()

marco = LabelFrame(app, text="Datos del Estudiante", font=("helvetica", 20, "bold"), pady=5)
marco.config(bd=2)
marco.pack()

lbl_nombre_apellido = Label(marco, text="Alumno", font=("helvetica", 15, "bold"))
lbl_nombre_apellido.grid(row=1, column=0, sticky="s", pady=5, padx=8)
nombre_apellido = Entry(marco, width=40, border=5, font=("helvetica", 12))
nombre_apellido.grid(row=1, column=1, pady=5, padx=100)
nombre_apellido.focus()

lbl_profesor = Label(marco, text="Profesor", font=("helvetica", 15, "bold"))
lbl_profesor.grid(row=2, column=0, sticky="s", pady=5, padx=8)
profesor = Entry(marco, width=40, border=5, font=("helvetica", 12))
profesor.grid(row=2, column=1, pady=5, padx=100)

lbl_curso = Label(marco, text="Curso", font=("helvetica", 15, "bold"))
lbl_curso.grid(row=3, column=0, pady=5, padx=8)
curso = Entry(marco, width=40, border=5, font=("helvetica", 12))
curso.grid(row=3, column=1)

marco_herramientas = LabelFrame(app, text="Herramientas a llevar", font=("helvetica", 20, "bold"), pady=5)
marco_herramientas.config(bd=2)
marco_herramientas.pack(pady=20, padx=200)

lbl_herramientas = Label(marco_herramientas, text="Herramientas", font=("helvetica", 15, "bold"))
lbl_herramientas.grid(row=1, column=0, pady=5, padx=8)
herramientas = Text(marco_herramientas, width=30, height=10, font=("helvetica", 12), border=5)
herramientas.grid(row=1, column=1, padx=15, pady=10)

frame_botones = LabelFrame(app)
frame_botones.pack()

boton_registrar = Button(frame_botones, text="AGREGAR", height=2, width=15, font=("helvetica", 12), bg="green", fg="white", command=agregar)
boton_registrar.grid(row=0, column=0)
boton_editar = Button(frame_botones, text="EDITAR", height=2, width=15, font=("helvetica", 12), bg="gray", fg="white", state=DISABLED)
boton_editar.grid(row=0, column=1)
boton_eliminar = Button(frame_botones, text="ELIMINAR", width=15, height=2, font=("helvetica", 12), bg="red", fg="white", command=eliminar)
boton_eliminar.grid(row=0, column=2)

tree = ttk.Treeview(app, columns=("ID", "Alumno", "Profesor", "Curso", "Herramientas"), show="headings", height=20)
tree.heading("ID", text="ID")
tree.heading("Alumno", text="Alumno")
tree.heading("Profesor", text="Profesor")
tree.heading("Curso", text="Curso")
tree.heading("Herramientas", text="Herramientas")
tree.column("ID", width=2)
tree.column("Alumno", width=200)
tree.column("Profesor", width=200)
tree.column("Curso", width=150)
tree.column("Herramientas", width=300)
tree.pack(pady=20)

tree.bind("<Double-1>", cargar_registro)

# Crear Scrollbar vertical
scrollbar = ttk.Scrollbar(app)
tree.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)

# Empaquetamos la barra vertical y lo colocamos en el lugar correcot
tree.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

mostrar_registros()
app.mainloop()
