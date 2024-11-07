import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    print("ajustando el ruido ambiental un momento...")
    r.adjust_for_ambient_noise(source)
    print("escuchando...")
    audio = r.listen(source)
    
    try:
        # Reconocer la voz usando Google Web Speech API
        texto = r.recognize_google(audio, language='es-ES')
        print("Has dicho: " + texto)
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
    except sr.RequestError as e:
        print("Error al solicitar resultados; {0}".format(e))