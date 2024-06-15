import qrcode
import cv2
# Lista de herramientas
herramientas = ["Martillo", "Destornillador", "Llave inglesa", "Alicates", "Sierra", "Mechas", "Gafas"]

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


# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Cargar el detector de QR Code
detector = cv2.QRCodeDetector()

while True:
    # Leer frames de la cámara
    _, frame = cap.read()

    # Detectar y decodificar el QR Code
    data, bbox, _ = detector.detectAndDecode(frame)

    # Si hay un QR Code en la imagen, mostrar su contenido
    if bbox is not None and data:
        print("Datos del QR Code:", data)
        # Mostrar el frame con un rectángulo alrededor del QR Code
        n_lines = len(bbox)
        for i in range(n_lines):
            point1 = tuple(bbox[i][0])
            point2 = tuple(bbox[(i+1) % n_lines][0])
            cv2.line(frame, point1, point2, color=(255, 0, 0), thickness=2)

    # Mostrar la imagen en una ventana
    cv2.imshow("Frame", frame)

    # Salir con 'ESC'
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()