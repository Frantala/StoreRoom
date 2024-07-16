import qrcode
import cv2
from pyzbar import pyzbar

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
                "yaqui"]

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


def decode_qr(frame):
    # Detectar códigos QR en la imagen
    qr_codes = pyzbar.decode(frame)
    for qr in qr_codes:
        # Extraer los datos del QR
        qr_data = qr.data.decode("utf-8")
        # Dibujar un rectángulo alrededor del QR
        x, y, w, h = qr.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Mostrar los datos del QR en la imagen
        cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

def main():
    # Capturar video desde la cámara
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Decodificar y mostrar el QR
        frame = decode_qr(frame)
        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()