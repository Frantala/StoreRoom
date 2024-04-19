import tkinter as ttk
from tkinter import *

ventana = ttk.Tk()
ventana.title("Pañol Herramientas")
ventana.geometry("500x500")

lbl_herramientas = ttk.Label(ventana, text="Hola", font=("helvetica", 15))
lbl_herramientas.pack()


ventana.mainloop()