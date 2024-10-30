import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo():
    # Configuración del servidor SMTP de Gmail
    smtp_host = "smtp.gmail.com"
    smtp_port = 465
    smtp_user = "dpit.saest.dest@gmail.com"  # Reemplaza con tu email
    smtp_password = "yzjn gphd stcw staq"  # Contraseña de aplicación de Google

    # Configuración del mensaje
    destinatarios = ["eric.ruiz@ine.mx", "kaderodi@gmail.com"]
    subject = f"Resultado de ejecución de Pipeline: {os.getenv('JOB_NAME', 'Desconocido')} Número:{os.getenv('BUILD_NUMBER', 'Desconocido')}"
    
    # Cuerpo del mensaje en HTML
    allure_report_url = f"{os.getenv('BUILD_URL')}allure"
    pytest_report_url = f"{os.getenv('BUILD_URL')}execution/node/3/ws/tests/pytestreport/report.html"
    blue_ocean_url = f"{os.getenv('JENKINS_URL')}blue/organizations/jenkins/{os.getenv('JOB_NAME')}/detail/{os.getenv('JOB_NAME')}/{os.getenv('BUILD_ID')}/pipeline"
    
    body = f"""
    <p>El pipeline ha finalizado con el estado: {os.getenv('BUILD_RESULT', 'Desconocido')}</p>
    <p>Duración pipeline: {os.getenv('BUILD_DURATION')}</p>
    <p>Revisa los detalles en Jenkins: <a href="{os.getenv('BUILD_URL')}">{os.getenv('BUILD_URL')}</a></p>
    <p>Revisa los detalles en Open Blue Ocean: <a href="{blue_ocean_url}">{blue_ocean_url}</a></p>
    <p>Reporte Allure: <a href="{allure_report_url}">{allure_report_url}</a></p>
    <p>Reporte Pytest: <a href="{pytest_report_url}">{pytest_report_url}</a></p>
    """

    # Crear el mensaje MIME
    mensaje = MIMEMultipart()
    mensaje['From'] = smtp_user
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = subject
    mensaje.attach(MIMEText(body, 'html'))

    # Conectar al servidor y enviar el correo
    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, destinatarios, mensaje.as_string())
            print("Correo enviado con éxito")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Llamada a la función para enviar el correo
if __name__ == "__main__":
    enviar_correo()
