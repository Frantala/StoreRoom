from tkinter import *
from tkinter import ttk

# Funciones que necesitas definir, puedes personalizarlas como necesites
def pasar_excel():
    pass

def scan_qr():
    pass

def agregar():
    pass

def eliminar():
    pass

def filtrar_registros():
    pass

def cargar_registro(event):
    pass

def mostrar_registros():
    pass

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

# Tabla de registros
tree = ttk.Treeview(content_frame, columns=("ID", "Alumno", "Profesor", "Curso", "Herramientas"), show="headings", height=20)
tree.heading("ID", text="ID")
tree.heading("Alumno", text="Alumno")
tree.heading("Profesor", text="Profesor")
tree.heading("Curso", text="Curso")
tree.heading("Herramientas", text="Herramientas")
tree.column("ID", width=30)
tree.column("Alumno", width=200)
tree.column("Profesor", width=200)
tree.column("Curso", width=150)
tree.column("Herramientas", width=300)
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

