import smtplib
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import RECIPIENTS, SENDER_EMAIL, APP_PASSWORD, LOOP_COUNT, DELAY_MIN, DELAY_MAX, EMAIL_CONTENT, EMAIL_SUBJECT

def send_email():
    # Tạo số random 16 chữ số cho tiêu đề
    random_number = random.randint(1000000000000000, 9999999999999999)
    subject = f"{EMAIL_SUBJECT} #{random_number}"
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAILS
    msg['To'] = ", ".join(RECIPIENTS)
    msg['Subject'] = subject
    
    msg.attach(MIMEText(EMAIL_CONTENT, 'plain', 'utf-8'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENTS, msg.as_string())
        server.quit()
        
        print(f"✓ Đã gửi email thành công!")
        print(f"  Tiêu đề: {subject}")
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
