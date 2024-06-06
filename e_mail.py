import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def mail(receiver_email, content,sender_email = "wewe231223@tukorea.ac.kr", sender_pw = "hdfcgtcbanjsvcme"):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "부동산 매물 즐겨찾기 알림"
    msg.attach(MIMEText(content, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_pw)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()