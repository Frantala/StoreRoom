import qrcode
import cv2
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
                "Augereadoras"]

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
