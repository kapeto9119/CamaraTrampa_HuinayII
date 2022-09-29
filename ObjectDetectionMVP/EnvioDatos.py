import email, smtplib, ssl, request

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Add body to email

class Envio:
    def __init__(self, filename, json):
        self.filename = filename
        self.jsonOriginal = json

        self.subject = "Resultados analisis de imágenes Camara Trampa - Huinay II"
        self.body = "Archivo adjunto"
        self.sender_email = "compras@smartdots.cl"
        self.receiver_email = "nicolas.capetillo@smartdots.cl"
        self.bcc = "carlos@smartdots.cl"
        self.password = "Proyectoap1"
        # password = input("Type your password and press enter:")

        # Create a multipart message and set headers
        self.message = MIMEMultipart()
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email
        self.message["Subject"] = self.subject
        self.message["Bcc"] = self.bcc  # Recommended for mass emails
    
    def sendByEmail(self):
        (self.message).attach(MIMEText(self.body, "plain"))

        # filename = self.filename  # In same directory as script

        # Open PDF file in binary mode
        with open(self.filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {self.filename}",
        )

        # Add attachment to message and convert message to string
        (self.message).attach(part)
        text = (self.message).as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("mail.smartdots.cl", 465, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, text)

    def sendByHTTP(self):
        r = requests.post('http://lwan.smartdots.cl:1880/camaras/payload', json=jsonOriginal)
        print(f"Status Code: {r.status_code}, Response: {r.json()}")