import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


app = Tk()

# Crear funcion agregar a la base de datos
def agregar():
    # Crear o conectar a una base de datos
    conn = sqlite3.connect('Proyecto-Escuela')
    # Crear un cursor
    c = conn.cursor()
    # Insertar en una tabla
    c.execute("INSERT INTO Registros VALUES(:nombre_apellido,:profesor,:curso,:herramientas)",
              {
                  'nombre_apellido':nombre_apellido.get(),
                  'profesor':profesor.get(),
                  'curso': curso.get(),
                  'herramientas': herramientas.get("1.0")
              })
    #Guardar los cambios
    conn.commit()
    #Cerrar la conexion
    conn.close()
#### TITULO ####
titulo = Label(text="REGISTRO DE HERRAMIENTAS", fg="black", font=("helvetica", 17, "bold"), pady=10)
titulo.pack()


        #### FRAME MARCO ESTUDIANTE####
marco = LabelFrame(app,text="Datos del Estudiante", font=("helvetica", 20, "bold"), pady=5)
marco.config(bd=2)
marco.pack()

#### Formulario DATOS####
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

curso = Entry(marco, width=40,border=5, font=("helvetica", 12))
curso.grid(row=3, column=1)

### MARCO HERRAMIENTAS ###
marco_herramientas = LabelFrame(text="Herramientas a llevar",font=("helvetica", 20, "bold"),pady=5)
marco_herramientas.config(bd=2)
marco_herramientas.pack(pady=20, padx=200)


lbl_herramientas = Label(marco_herramientas, text="Herramientas", font=("helvetica", 15, "bold"))
lbl_herramientas.grid(row=1, column=0, pady=5, padx=8)

herramientas = Text(marco_herramientas, width=50, height=10,font=("helvetica", 12), border=5)
herramientas.grid(row=1, column=3, padx=15, pady=10)

### FRAME BOTONES ###
frame_botones = LabelFrame(app)
frame_botones.pack()

### BOTONES ###
boton_registrar = Button(frame_botones, text="AGREGAR", height=2, width=15, font=("helvetica", 12), bg="green", fg="white", command=agregar)
boton_registrar.grid(row=0, column=0)
boton_editar = Button(frame_botones, text="EDITAR", height=2, width=15, font=("helvetica", 12), bg="gray", fg="white")
boton_editar.grid(row=0, column=1)
boton_eliminar = Button(frame_botones, text="ELIMINAR", width=15, height=2, font=("helvetica", 12), bg="red", fg="white")
boton_eliminar.grid(row=0, column=2)

### TABLA ###
# Crear el widget Treeview
                
        
app.mainloop()