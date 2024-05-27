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
    # Crear o conectar a una base de datos
    conn = sqlite3.connect('Proyecto-Escuela')
    # Crear un cursor
    c = conn.cursor()
    # Insertar en una tabla
    c.execute("INSERT INTO Registros VALUES (:nombre_apellido, :profesor, :curso, :herramientas)", {
        'nombre_apellido': nombre_apellido.get(),
        'profesor': profesor.get(),
        'curso': curso.get(),
        'herramientas': herramientas.get("1.0", END).strip()
    })
    # Guardar los cambios
    conn.commit()
    # Cerrar la conexión
    conn.close()
    # Limpiar los campos después de agregar
    nombre_apellido.delete(0, END)
    profesor.delete(0, END)
    curso.delete(0, END)
    herramientas.delete("1.0", END)
    messagebox.showinfo("Registro exitoso", "Datos guardados correctamente")
    # Actualizar la vista de los registros 
    mostrar_registros()

def mostrar_registros():
    #Limpiar la tabla
    for row in tree.get_children():
        tree.delete(row)
    # Crear o conectar a una base de datos
    conn = sqlite3.connect('Proyecto-Escuela')
    # Crear un cursor
    c = conn.cursor()
    # Seleccionar todos los registros
    c.execute("SELECT * FROM Registros")
    registros = c.fetchall()
    # Añadir registros a la tabla
    for registro in registros:
        tree.insert("", END, values=registro)
    # Cerrar la conexión
    conn.close()

def eliminar():
    # Obtener el registro seleccionado
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar")
        return
    # Confirmar eliminación
    respuesta = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar este registro?")
    if respuesta:
        # Obtener el ID del registro seleccionado
        item = tree.item(seleccionado)
        registro_id = item['values'][0]
        # Crear o conectar a una base de datos
        conn = sqlite3.connect('Proyecto-Escuela')
        # Crear un cursor
        c = conn.cursor()
        # Eliminar el registro de la base de datos
        c.execute("DELETE FROM Registros WHERE rowid = ?", (registro_id,))
        # Guardar los cambios
        conn.commit()
        # Cerrar la conexión
        conn.close()
        # Eliminar el registro del Treeview
        tree.delete(seleccionado)
        messagebox.showinfo("Eliminación exitosa", "Registro eliminado correctamente")



# Configuración de la ventana principal
app = Tk()
app.title("Registro de Herramientas")

# Título
titulo = Label(app, text="REGISTRO DE HERRAMIENTAS", fg="black", font=("helvetica", 17, "bold"), pady=10)
titulo.pack()

# Frame de datos del estudiante
marco = LabelFrame(app, text="Datos del Estudiante", font=("helvetica", 20, "bold"), pady=5)
marco.config(bd=2)
marco.pack()

# Formulario de datos
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

# Frame de herramientas
marco_herramientas = LabelFrame(app, text="Herramientas a llevar", font=("helvetica", 20, "bold"), pady=5)
marco_herramientas.config(bd=2)
marco_herramientas.pack(pady=20, padx=200)

lbl_herramientas = Label(marco_herramientas, text="Herramientas", font=("helvetica", 15, "bold"))
lbl_herramientas.grid(row=1, column=0, pady=5, padx=8)
herramientas = Text(marco_herramientas, width=50, height=10, font=("helvetica", 12), border=5)
herramientas.grid(row=1, column=1, padx=15, pady=10)

# Frame de botones
frame_botones = LabelFrame(app)
frame_botones.pack()

# Botones
boton_registrar = Button(frame_botones, text="AGREGAR", height=2, width=15, font=("helvetica", 12), bg="green", fg="white", command=agregar)
boton_registrar.grid(row=0, column=0)
boton_editar = Button(frame_botones, text="EDITAR", height=2, width=15, font=("helvetica", 12), bg="gray", fg="white")
boton_editar.grid(row=0, column=1)
boton_eliminar = Button(frame_botones, text="ELIMINAR", width=15, height=2, font=("helvetica", 12), bg="red", fg="white", command=eliminar)
boton_eliminar.grid(row=0, column=2)

# Tabla para mostrar los registros
tree = ttk.Treeview(app, columns=("Alumno", "Profesor", "Curso", "Herramientas"), show="headings")
tree.heading("Alumno", text="Alumno")
tree.heading("Profesor", text="Profesor")
tree.heading("Curso", text="Curso")
tree.heading("Herramientas", text="Herramientas")
tree.pack(pady=20)

# Cargar los registros al iniciar la aplicación
mostrar_registros()

# Ejecutar la aplicación
app.mainloop()