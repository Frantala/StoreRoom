import sounddevice as sd
import numpy as np
import whisper
import queue
import threading

# Cargar el modelo Whisper
model = whisper.load_model("tiny")

# Configuración de la grabación de audio
samplerate = 16000  # 16 kHz
blocksize = 1600  # Aproximadamente 0.1 segundos de audio
channels = 1

# Cola para manejar los datos de audio
audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    """Función de callback que coloca los datos de audio en la cola"""
    if status:
        print(status)
    audio_queue.put(indata.copy())

def process_audio():
    """Procesa los datos de audio en la cola y obtiene la transcripción"""
    while True:
        audio_data = audio_queue.get()
        audio_data = audio_data.flatten().astype(np.float32) / 32768.0
        result = model.transcribe(audio_data, fp16=False)
        print(f'Transcripción: {result["text"]}')

# Abrir un stream de audio
stream = sd.InputStream(samplerate=samplerate, blocksize=blocksize, channels=channels, callback=audio_callback)

print("Grabando... Presiona Ctrl+C para detener.")
try:
    # Iniciar un hilo para procesar el audio
    threading.Thread(target=process_audio, daemon=True).start()
    with stream:
        while True:
            sd.sleep(1000)  # Duerme por 1 segundo y luego continúa
except KeyboardInterrupt:
    print("Finalizando grabación.")
finally:
    stream.close()

