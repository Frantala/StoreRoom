from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class Pañol:
        db_name = "Proyecto-Escuela.db"

        def __init__(self, ventana_herramienta):
                self.window = ventana_herramienta
                self.window.title("Aplicacion del pañol")
                self.window.geometry("1350x700")
                self.window.resizable(0,0)
                self.window.config(bd=10)


                #### TITULO ####
                titulo = Label(ventana_herramienta, text="REGISTRO DE HERRAMIENTAS", fg="black", font=("helvetica", 17, "bold"), pady=10)
                titulo.pack()


                #### FRAME MARCO ESTUDIANTE####
                marco = LabelFrame(ventana_herramienta, text="Datos del Estudiante", font=("helvetica", 20, "bold"), pady=5)
                marco.config(bd=2)
                marco.pack()

                #### Formulario DATOS####
                lbl_nombre_apellido = Label(marco, text="Alumno", font=("helvetica", 15, "bold"))
                lbl_nombre_apellido.grid(row=1, column=0, sticky="s", pady=5, padx=8)

                self.nombre_apellido = Entry(marco, width=40, border=5, font=("helvetica", 12))
                self.nombre_apellido.grid(row=1, column=1, pady=5, padx=100)
                self.nombre_apellido.focus()

                lbl_profesor = Label(marco, text="Profesor", font=("helvetica", 15, "bold"))
                lbl_profesor.grid(row=2, column=0, sticky="s", pady=5, padx=8)

                self.profesor = Entry(marco, width=40, border=5, font=("helvetica", 12))
                self.profesor.grid(row=2, column=1, pady=5, padx=100)

                lbl_curso = Label(marco, text="Curso", font=("helvetica", 15, "bold"))
                lbl_curso.grid(row=3, column=0, pady=5, padx=8)

                self.curso = Entry(marco, width=40,border=5, font=("helvetica", 12))
                self.curso.grid(row=3, column=1)

                ### MARCO HERRAMIENTAS ###
                marco_herramientas = LabelFrame(ventana_herramienta, text="Herramientas a llevar",font=("helvetica", 20, "bold"),pady=5)
                marco_herramientas.config(bd=2)
                marco_herramientas.pack(pady=20, padx=200)


                lbl_herramientas = Label(marco_herramientas, text="Herramientas", font=("helvetica", 15, "bold"))
                lbl_herramientas.grid(row=1, column=0, pady=5, padx=8)

                self.herramientas = Text(marco_herramientas, width=50, height=10,font=("helvetica", 12), border=5)
                self.herramientas.grid(row=1, column=3, padx=15, pady=10)

                ### FRAME BOTONES ###
                frame_botones = LabelFrame(ventana_herramienta)
                frame_botones.pack()

                ### BOTONES ###
                boton_registrar = Button(frame_botones, text="AGREGAR", height=2, width=15, font=("helvetica", 12), bg="green", fg="white")
                boton_registrar.grid(row=0, column=0)
                boton_editar = Button(frame_botones, text="EDITAR", height=2, width=15, font=("helvetica", 12), bg="gray", fg="white")
                boton_editar.grid(row=0, column=1)
                boton_eliminar = Button(frame_botones, text="ELIMINAR", width=15, height=2, font=("helvetica", 12), bg="red", fg="white")
                boton_eliminar.grid(row=0, column=2)

                ### TABLA ###
                # Crear el widget Treeview
                self.tree = ttk.Treeview(columns=("ALUMNO", "Profesor", "Curso", "Herramientas"), show="headings")

                # Configurar las columnas
                self.tree.column("ALUMNO", width=100)
                self.tree.column("Profesor", width=100)
                self.tree.column("Curso", width=100)
                self.tree.column("Herramientas", width=200)

                # Encabezados de las columnas
                self.tree.heading("ALUMNO", text="ALUMNO")
                self.tree.heading("Profesor", text="PROFESOR")
                self.tree.heading("Curso", text="CURSO")
                self.tree.heading("Herramientas", text="HERRAMIENTAS")

                self.tree.pack(pady=20)                
                
                

app = Tk()

my_app = Pañol(app)
app.mainloop()