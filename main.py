# -*- coding: utf-8 -*-
import smtplib
import time
import random
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Fix UTF-8 for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Colors
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
 ████████╗ ██████╗  ██████╗ ██╗         ███╗   ███╗ █████╗ ██╗██╗     
 ╚══██╔══╝██╔═══██╗██╔═══██╗██║         ████╗ ████║██╔══██╗██║██║     
    ██║   ██║   ██║██║   ██║██║         ██╔████╔██║███████║██║██║     
    ██║   ██║   ██║██║   ██║██║         ██║╚██╔╝██║██╔══██║██║██║     
    ██║   ╚██████╔╝╚██████╔╝███████╗    ██║ ╚═╝ ██║██║  ██║██║███████╗
    ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
{Colors.RESET}
{Colors.YELLOW}                    Auto Email Sender Tool v1.0.0
{Colors.GREEN}                    Author: ThanhTaiDev
{Colors.BLUE}        Github: https://github.com/ThanhTaiDev/ToolAutoMail
{Colors.RESET}
    """
    print(banner)

def print_divider():
    print(f"{Colors.CYAN}{'═' * 70}{Colors.RESET}")

def print_section(title):
    print(f"\n{Colors.YELLOW}■ {title}{Colors.RESET}")

def input_field(label, default=""):
    if default:
        return input(f"{Colors.GREEN}  ➤ {label} {Colors.WHITE}[{default}]: {Colors.RESET}") or default
    return input(f"{Colors.GREEN}  ➤ {label}: {Colors.RESET}")

def input_multiline(label):
    print(f"{Colors.GREEN}  ➤ {label} {Colors.WHITE}(nhập 'XONG' để kết thúc):{Colors.RESET}")
    lines = []
    while True:
        line = input(f"{Colors.WHITE}    | {Colors.RESET}")
        if line.strip().upper() == 'XONG':
            break
        lines.append(line)
    return '\n'.join(lines)

def send_email(sender, password, recipients, subject_template, content, smtp_server, smtp_port, use_ssl=False):
    random_number = random.randint(1000000000000000, 9999999999999999)
    subject = f"{subject_template} #{random_number}"
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    
    if use_ssl:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    else:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
    
    server.login(sender, password)
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()
    
    return subject

def main_menu():
    clear_screen()
    print_banner()
    print_divider()
    
    print_section("Các Chức Năng")
    print(f"""
{Colors.RED}  0. ✗ Thoát Chương Trình{Colors.RESET}
{Colors.GREEN}  1. ➤ Gửi Email Mới        {Colors.WHITE}(Nhập cấu hình và gửi email){Colors.RESET}
{Colors.CYAN}  2. ◉ Xem Cấu Hình         {Colors.WHITE}(Xem cấu hình đã lưu){Colors.RESET}
{Colors.YELLOW}  3. ⚙ Gửi Nhanh            {Colors.WHITE}(Gửi lại với cấu hình cũ){Colors.RESET}
{Colors.MAGENTA}  4. ✎ Sửa Cấu Hình         {Colors.WHITE}(Sửa một phần cấu hình){Colors.RESET}
    """)
    print_divider()
    
    return input(f"{Colors.MAGENTA}  Chọn chức năng: {Colors.RESET}")

def get_config():
    clear_screen()
    print_banner()
    print_divider()
    
    config = {}
    
    print_section("Cấu Hình SMTP Server")
    print(f"{Colors.WHITE}  Gợi ý: Gmail (smtp.gmail.com:587), Outlook (smtp.office365.com:587){Colors.RESET}")
    print(f"{Colors.WHITE}         Custom domain thường dùng SSL port 465{Colors.RESET}")
    config['smtp_server'] = input_field("SMTP Server", "smtp.gmail.com")
    config['smtp_port'] = int(input_field("SMTP Port", "587"))
    config['use_ssl'] = input_field("Dùng SSL? (y/n)", "n").lower() == 'y'
    
    print_section("Cấu Hình Email Gửi")
    config['sender'] = input_field("Email của bạn")
    config['password'] = input_field("Password/App Password")
    
    print_section("Người Nhận (cách nhau bằng dấu phẩy)")
    recipients_str = input_field("Danh sách email nhận")
    config['recipients'] = [r.strip() for r in recipients_str.split(',')]
    
    print_section("Cài Đặt Gửi")
    config['loop_count'] = int(input_field("Số lần gửi lặp lại", "10"))
    config['delay_min'] = int(input_field("Thời gian chờ tối thiểu (giây)", "5"))
    config['delay_max'] = int(input_field("Thời gian chờ tối đa (giây)", "10"))
    
    print_section("Nội Dung Email")
    config['subject'] = input_field("Tiêu đề email", "Intellectual Property Appeal Contact Form")
    config['content'] = input_multiline("Nội dung email")
    
    return config

def run_send(config):
    clear_screen()
    print_banner()
    print_divider()
    print_section("Đang Gửi Email...")
    print()
    
    success = 0
    failed = 0
    
    for i in range(1, config['loop_count'] + 1):
        try:
            subject = send_email(
                config['sender'],
                config['password'],
                config['recipients'],
                config['subject'],
                config['content'],
                config['smtp_server'],
                config['smtp_port'],
                config.get('use_ssl', False)
            )
            success += 1
            print(f"{Colors.GREEN}  ✓ [{i}/{config['loop_count']}] Gửi thành công!{Colors.RESET}")
            print(f"{Colors.WHITE}    Tiêu đề: {subject}{Colors.RESET}")
        except Exception as e:
            failed += 1
            print(f"{Colors.RED}  ✗ [{i}/{config['loop_count']}] Thất bại: {e}{Colors.RESET}")
        
        if i < config['loop_count']:
            delay = random.randint(config['delay_min'], config['delay_max'])
            print(f"{Colors.YELLOW}    Chờ {delay} giây...{Colors.RESET}\n")
            time.sleep(delay)
    
    print_divider()
    print(f"\n{Colors.GREEN}  ✓ Hoàn thành! Thành công: {success} | Thất bại: {failed}{Colors.RESET}")
    input(f"\n{Colors.CYAN}  Nhấn Enter để tiếp tục...{Colors.RESET}")

def show_config(config):
    clear_screen()
    print_banner()
    print_divider()
    print_section("Cấu Hình Hiện Tại")
    
    if not config:
        print(f"{Colors.RED}  Chưa có cấu hình nào!{Colors.RESET}")
    else:
        print(f"{Colors.WHITE}  SMTP Server: {config.get('smtp_server', 'N/A')}:{config.get('smtp_port', 'N/A')} {'(SSL)' if config.get('use_ssl') else '(TLS)'}{Colors.RESET}")
        print(f"{Colors.WHITE}  Email gửi: {config.get('sender', 'N/A')}{Colors.RESET}")
        print(f"{Colors.WHITE}  Người nhận: {', '.join(config.get('recipients', []))}{Colors.RESET}")
        print(f"{Colors.WHITE}  Số lần gửi: {config.get('loop_count', 'N/A')}{Colors.RESET}")
        print(f"{Colors.WHITE}  Thời gian chờ: {config.get('delay_min', 'N/A')}s - {config.get('delay_max', 'N/A')}s{Colors.RESET}")
        print(f"{Colors.WHITE}  Tiêu đề: {config.get('subject', 'N/A')}{Colors.RESET}")
    
    print_divider()
    input(f"\n{Colors.CYAN}  Nhấn Enter để tiếp tục...{Colors.RESET}")

def edit_config(config):
    clear_screen()
    print_banner()
    print_divider()
    print_section("Sửa Cấu Hình")
    
    if not config:
        print(f"{Colors.RED}  Chưa có cấu hình nào! Vui lòng chọn 1 trước.{Colors.RESET}")
        input(f"\n{Colors.CYAN}  Nhấn Enter để tiếp tục...{Colors.RESET}")
        return config
    
    print(f"""
{Colors.WHITE}  1. Người nhận      : {', '.join(config.get('recipients', []))}{Colors.RESET}
{Colors.WHITE}  2. Số lần gửi      : {config.get('loop_count', 'N/A')}{Colors.RESET}
{Colors.WHITE}  3. Thời gian chờ   : {config.get('delay_min', 'N/A')}s - {config.get('delay_max', 'N/A')}s{Colors.RESET}
{Colors.WHITE}  4. Tiêu đề         : {config.get('subject', 'N/A')}{Colors.RESET}
{Colors.WHITE}  5. Nội dung email{Colors.RESET}
{Colors.RED}  0. Quay lại{Colors.RESET}
    """)
    print_divider()
    
    choice = input(f"{Colors.MAGENTA}  Chọn mục cần sửa: {Colors.RESET}")
    
    if choice == '1':
        print_section("Sửa Người Nhận")
        recipients_str = input_field("Danh sách email nhận (cách nhau bằng dấu phẩy)")
        config['recipients'] = [r.strip() for r in recipients_str.split(',')]
        print(f"{Colors.GREEN}  ✓ Đã cập nhật người nhận!{Colors.RESET}")
    elif choice == '2':
        print_section("Sửa Số Lần Gửi")
        config['loop_count'] = int(input_field("Số lần gửi lặp lại", str(config['loop_count'])))
        print(f"{Colors.GREEN}  ✓ Đã cập nhật số lần gửi!{Colors.RESET}")
    elif choice == '3':
        print_section("Sửa Thời Gian Chờ")
        config['delay_min'] = int(input_field("Thời gian chờ tối thiểu (giây)", str(config['delay_min'])))
        config['delay_max'] = int(input_field("Thời gian chờ tối đa (giây)", str(config['delay_max'])))
        print(f"{Colors.GREEN}  ✓ Đã cập nhật thời gian chờ!{Colors.RESET}")
    elif choice == '4':
        print_section("Sửa Tiêu Đề")
        config['subject'] = input_field("Tiêu đề email", config['subject'])
        print(f"{Colors.GREEN}  ✓ Đã cập nhật tiêu đề!{Colors.RESET}")
    elif choice == '5':
        print_section("Sửa Nội Dung Email")
        config['content'] = input_multiline("Nội dung email mới")
        print(f"{Colors.GREEN}  ✓ Đã cập nhật nội dung!{Colors.RESET}")
    elif choice == '0':
        return config
    else:
        print(f"{Colors.RED}  Lựa chọn không hợp lệ!{Colors.RESET}")
    
    time.sleep(1)
    return config

def main():
    config = {}
    
    while True:
        choice = main_menu()
        
        if choice == '0':
            clear_screen()
            print(f"{Colors.CYAN}  Tạm biệt! 👋{Colors.RESET}\n")
            sys.exit(0)
        elif choice == '1':
            config = get_config()
            run_send(config)
        elif choice == '2':
            show_config(config)
        elif choice == '3':
            if config:
                run_send(config)
            else:
                print(f"{Colors.RED}  Chưa có cấu hình! Vui lòng chọn 1 trước.{Colors.RESET}")
                time.sleep(2)
        elif choice == '4':
            config = edit_config(config)
        else:
            print(f"{Colors.RED}  Lựa chọn không hợp lệ!{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()

