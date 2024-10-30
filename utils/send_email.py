import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo():
    # Configuración del servidor SMTP de Gmail
    smtp_host = "smtp.gmail.com"
    smtp_port = 465
    smtp_user = "dpit.saest.dest@gmail.com"  # Reemplaza con tu email
    smtp_password = "yzjn gphd stcw staq"  # Contraseña de aplicación de Google

    # Información del build de Jenkins
    build_name = os.getenv('JOB_NAME', 'Desconocido')
    build_result = sys.argv[1] if len(sys.argv) > 1 else 'Desconocido'
    build_duration = sys.argv[2] if len(sys.argv) > 2 else 'Desconocido'
    build_number = os.getenv('BUILD_NUMBER', 'Desconocido')
    build_url = os.getenv('BUILD_URL', 'Desconocido')
    allure_report_url = f"{build_url}allure"
    pytest_report_url = f"{build_url}execution/node/3/ws/tests/pytestreport/report.html"
    blue_ocean_url = f"{os.getenv('JENKINS_URL')}blue/organizations/jenkins/{build_name}/detail/{build_name}/{build_number}/pipeline"
 
    # Configuración del mensaje
    destinatarios = ["eric.ruiz@ine.mx", "georgina.cuadriello@ine.mx"]
    subject = f"[DEST][Jenkins] Resultado de ejecución de Pipeline: {build_name} Número: {build_number}"
     
    body = f"""
        <h2 style="color: #2E86C1;">Reporte de Ejecución del Pipeline</h2>
        <p>Estimado equipo:</p>
        <p>El pipeline <strong>{build_name}</strong> ha finalizado. Aquí está el resumen:</p>
        <table style="width: 50%; border: 1px solid #ddd; border-collapse: collapse;">
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">Build Number</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{build_number}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">Estado</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{build_result}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;">Duración</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{build_duration}</td>
            </tr>
        </table>
        <p>Revisa más detalles:</p>
        <a href="{allure_report_url}" style="display: inline-block; padding: 10px 20px; color: #fff; background-color: #5cb85c; text-decoration: none;">Reporte Allure</a>
        <a href="{pytest_report_url}" style="display: inline-block; padding: 10px 20px; color: #fff; background-color: #5cb85c; text-decoration: none;">Reporte Pytest</a><br><br>
        <a href="{blue_ocean_url}" style="display: inline-block; padding: 10px 20px; color: #fff; background-color: #5bc0de; text-decoration: none;">Pipeline Blue Ocean</a>
        <a href="{build_url}" style="display: inline-block; padding: 10px 20px; color: #fff; background-color: #5bc0de; text-decoration: none;">Pipeline Jenkins</a>
        <p>Atentamente.<br>Equipo de DevOps - QA</p>
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
            print(f"Destinatarios: {destinatarios}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Llamada a la función para enviar el correo
if __name__ == "__main__":
    enviar_correo()
