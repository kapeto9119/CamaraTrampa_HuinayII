import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Add body to email

class Envio:
    def __init__(self, filename):
        self.filename = filename

        self.subject = "Email desde python en raspberry"
        self.body = "This is an email with attachment sent from Python"
        self.sender_email = "nicolas.capetillo@smartdots.cl"
        self.receiver_email = "nicolas.capetillo@smartdots.cl"
        self.password = "Mobotix99"
        # password = input("Type your password and press enter:")

        # Create a multipart message and set headers
        self.message = MIMEMultipart()
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email
        self.message["Subject"] = self.subject
        self.message["Bcc"] = self.receiver_email  # Recommended for mass emails
    
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

# envio = Envio("objects_detection_on_202209220959.csv")
# envio.sendByEmail()