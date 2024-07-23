import sqlite3
import speech_recognition as sr
import subprocess
import threading
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
        alumno.get(),
        profesor.get(),
        curso.get(),
        herramientas.get("1.0", END).strip()
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

# LE AGREGAMOS LA FUNCIONALIDAD DE VOZ A LA APLICACION 
# creamos una funcion para eso
def reconocer_voz():
    reconocedor = sr.Recognizer() #Creamos la clase para reconocer el sonido
    with sr.Microphone() as fuente:
        messagebox.showinfo("Escuchando", "Por favor, hable ahora...")
        reconocedor.adjust_for_ambient_noise(fuente) #ajustamos el sonido para el ambiente 
        audio = reconocedor.listen(fuente) #escuchamso en "vivo" el audio

        try:
            texto = reconocedor.recognize_google(audio, language='es-ES') #llamamos a la API de google Search con el idioma en español
            herramientas.insert(END, texto + '\n') #insertamos el texto escuchado y transcripto a la tabla
        except sr.UnknownValueError:
            messagebox.showerror("Error", "No se pudo entender el audio")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Error al solicitar resultados; {e}")

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

app = Tk()
app.title("StoreRoom")

titulo = Label(app, text="REGISTRO DE HERRAMIENTAS", fg="black", font=("helvetica", 17, "bold"), pady=10)
titulo.pack()

marco = LabelFrame(app, text="Datos del Estudiante", font=("helvetica", 20, "bold"), pady=5)
marco.config(bd=2)
marco.pack()
lbl_alumno = Label(marco, text="Alumno", font=("helvetica", 15, "bold"))
lbl_alumno.grid(row=1, column=0, sticky="s", pady=5, padx=8)
alumno = Entry(marco, width=40, border=5, font=("helvetica", 12))
alumno.grid(row=1, column=1, pady=5, padx=100)
alumno.focus()

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
boton_voz = Button(marco_herramientas, text="Utilizar Voz", font=("helvetica", 12), border=5, bg="gray", fg="white", command=reconocer_voz)
boton_voz.grid(row=2, column=1, padx=15, pady=10)

frame_botones = LabelFrame(app)
frame_botones.pack()

boton_registrar = Button(frame_botones, text="AGREGAR", height=2, width=15, font=("helvetica", 12), bg="green", fg="white", command=agregar)
boton_registrar.grid(row=0, column=0)
boton_editar = Button(frame_botones, text="EDITAR", height=2, width=15, font=("helvetica", 12), bg="gray", fg="white", state=DISABLED)
boton_editar.grid(row=0, column=1)
boton_eliminar = Button(frame_botones, text="ELIMINAR", width=15, height=2, font=("helvetica", 12), bg="red", fg="white", command=eliminar)
boton_eliminar.grid(row=0, column=2)

# Creamos un frame/espacio para filtrar registros es decir buscar por nombre de profesor

frame_filtrar = LabelFrame(app, width=50, height=50)
frame_filtrar.pack(pady=15)

lbl_filtrar = Label(frame_filtrar, text="Buscar Registros", font=("helvetica", 12))
lbl_filtrar.grid(row=0, column=0)
filtrar = Entry(frame_filtrar, width=50, font=("helvetica", 10), borderwidth=5)
filtrar.grid(row=0, column=1, padx=10)
btn_filtrar = Button(frame_filtrar, text="Buscar", font=("helvetica", 12), command=filtrar_registros)
btn_filtrar.grid(row=0, column=2, padx=10)

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