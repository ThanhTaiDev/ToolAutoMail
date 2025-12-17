import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import RECIPIENTS, SENDER_EMAIL, APP_PASSWORD, LOOP_COUNT, DELAY_MIN, DELAY_MAX, EMAIL_CONTENT

def send_email():
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = ", ".join(RECIPIENTS)
    msg['Subject'] = ""
    
    msg.attach(MIMEText(EMAIL_CONTENT, 'plain', 'utf-8'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENTS, msg.as_string())
        server.quit()
        
        print(f"✓ Đã gửi email thành công đến {len(RECIPIENTS)} người!")
        for r in RECIPIENTS:
            print(f"  - {r}")
            
    except Exception as e:
        print(f"✗ Lỗi: {e}")

if __name__ == "__main__":
    for i in range(1, LOOP_COUNT + 1):
        print(f"\n===== Lần gửi {i}/{LOOP_COUNT} =====")
        send_email()
        if i < LOOP_COUNT:
            delay = random.randint(DELAY_MIN, DELAY_MAX)
            print(f"Chờ {delay} giây...")
            time.sleep(delay)
    print(f"\n✓ Hoàn thành! Đã gửi {LOOP_COUNT} lần.")
