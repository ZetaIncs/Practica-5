# envio_correo.py
import smtplib
from email.message import EmailMessage

def enviar_correo(region):
    mensaje = EmailMessage()
    mensaje["Subject"] = f"Reporte de la región {region}"
    mensaje["From"] = "copilot@reactiva.com"
    mensaje["To"] = "usuario@reactiva.com"
    mensaje.set_content(f"Estimado usuario, \n\nAdjunto encontrará el reporte de la región {region} con el top 5 de costo inversión de las obras de tipo Urbano en estado 1,2,3. \n\nSaludos, \nCopilot")
    with open(f"{region}.xlsx", "rb") as archivo:
        contenido = archivo.read()
        mensaje.add_attachment(contenido, maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=f"{region}.xlsx")
    # Crear una conexión con el servidor de correo usando SMTP
    with smtplib.SMTP("localhost") as servidor:
        servidor.send_message(mensaje)
