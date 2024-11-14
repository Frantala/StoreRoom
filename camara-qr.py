import qrcode
import cv2
from pyzbar import pyzbar
from pyzbar.pyzbar import decode
import numpy as np

# Lista de herramientas
herramientas = ["Martillo", 
                "Destornillador", 
                "Llave inglesa", 
                "Alicates", 
                "Sierra", 
                "Mechas", 
                "Gafas", 
                "Guantes", 
                "Amoladora", 
                "Augereadoras",
                "Guardapolvo",
                "Mascara facial",
                "Regla",
                "Punta de Trazar"
                ]

# Generar códigos QR para cada herramienta
for herramienta in herramientas:
    # Crear un objeto de código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Agregar el nombre de la herramienta como datos del código QR
    qr.add_data(herramienta)
    qr.make(fit=True)

    # Crear una imagen del código QR
    img = qr.make_image(fill='black', back_color='white')

    # Guardar la imagen
    img.save(f"{herramienta}.png")

print("Códigos QR generados y guardados.")

def decode_qr(frame, last_qr_data):
    # Detectar códigos QR en la imagen
    qr_codes = pyzbar.decode(frame)
    for qr in qr_codes:
        # Extraer los datos del QR
        qr_data = qr.data.decode("utf-8")
        if qr_data != last_qr_data:  # Solo mostrar si el QR es diferente al último leído
            print(qr_data)
            last_qr_data = qr_data
        # Dibujar un rectángulo alrededor del QR
        x, y, w, h = qr.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Mostrar los datos del QR en la imagen
        cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame, last_qr_data

def scan_qr():
    def decode_qr(frame):
        qr_codes = decode(frame)
        for qr in qr_codes:
            qr_data = qr.data.decode("utf-8")
            x, y, w, h = qr.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            return qr_data
        return None

    cap = cv2.VideoCapture(0)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        mask_inv = cv2.bitwise_not(mask)
        blurred = cv2.GaussianBlur(frame, (21, 21), 0)
        hands = cv2.bitwise_and(frame, frame, mask=mask)
        background = cv2.bitwise_and(blurred, blurred, mask=mask_inv)
        combined = cv2.add(hands, background)

        qr_data = decode_qr(combined)
        if qr_data:
            print(f"QR Code Data: {qr_data}")

        cv2.imshow("Escanear QR", combined)
        if cv2.waitKey(1) & 0xFF == ord('t'):
            break

    cap.release()
    cv2.destroyAllWindows()

print(scan_qr())