import speech_recognition as sr
import subprocess
import pyautogui 

reccognizer = sr.Recognizer()
proceso = None
saludo = """
Agragando alumno...
"""

def ejecutar_comando(comando):
    global proceso
    if "abrir archivo" in comando:
        proceso = subprocess.Popen(["notepad.exe"])
    elif "saludar" in comando:
        pyautogui.write(saludo)
    elif "cerrar archivo" in comando:
        proceso.terminate()

def escuchar_comandos():
    with sr.Microphone() as source:
        print("en que te puedo ayudar...")
        reccognizer.adjust_for_ambient_noise(source)
        audio = reccognizer.listen(source)
    try:
        comando = reccognizer.recognize_google(audio, language="es-ES")
        print(f"comando reconocido: {comando}")
        ejecutar_comando(comando)
    except sr.UnknownValueError:
        print("no se pudo reconocer el audio")
    except sr.RequestError as e:
        print(f"error al realizar la solicitud {e}")

while True:
    escuchar_comandos()
