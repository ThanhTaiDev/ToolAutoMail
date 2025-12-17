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

# Lưu trữ tối đa 5 cấu hình
MAX_CONFIGS = 5
saved_configs = []

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
{Colors.YELLOW}                    Auto Email Sender Tool v1.1.0
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

def get_smtp_type(smtp_server):
    """Trả về loại SMTP dựa trên server"""
    if 'gmail' in smtp_server.lower():
        return 'Gmail'
    elif 'office365' in smtp_server.lower() or 'outlook' in smtp_server.lower():
        return 'Outlook'
    elif 'yahoo' in smtp_server.lower():
        return 'Yahoo'
    else:
        return 'Custom'

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

def display_config_list(title="Danh Sách Cấu Hình"):
    """Hiển thị danh sách cấu hình đã lưu"""
    print_section(f"{title} ({len(saved_configs)}/{MAX_CONFIGS})")
    
    if not saved_configs:
        print(f"{Colors.RED}  Chưa có cấu hình nào được lưu!{Colors.RESET}")
        return False
    
    for i, cfg in enumerate(saved_configs, 1):
        smtp_type = get_smtp_type(cfg.get('smtp_server', ''))
        sender = cfg.get('sender', 'N/A')
        loop_count = cfg.get('loop_count', 0)
        print(f"{Colors.WHITE}  {i}. [{smtp_type}] {sender} ({loop_count} lần gửi){Colors.RESET}")
    
    return True

def select_config(title="Chọn Cấu Hình"):
    """Cho phép người dùng chọn một cấu hình từ danh sách"""
    clear_screen()
    print_banner()
    print_divider()
    
    if not display_config_list(title):
        input(f"\n{Colors.CYAN}  Nhấn Enter để tiếp tục...{Colors.RESET}")
        return None
    
    print(f"{Colors.RED}  0. Quay lại{Colors.RESET}")
    print_divider()
    
    choice = input(f"{Colors.MAGENTA}  Chọn số (1-{len(saved_configs)}): {Colors.RESET}")
    
    try:
        idx = int(choice)
        if idx == 0:
            return None
        if 1 <= idx <= len(saved_configs):
            return idx - 1  # Trả về index
    except ValueError:
        pass
    
    print(f"{Colors.RED}  Lựa chọn không hợp lệ!{Colors.RESET}")
    time.sleep(1)
    return None

def save_config(config):
    """Lưu cấu hình vào danh sách"""
    global saved_configs
    
    if len(saved_configs) >= MAX_CONFIGS:
        print(f"{Colors.YELLOW}  ⚠ Đã đạt tối đa {MAX_CONFIGS} cấu hình!{Colors.RESET}")
        print(f"{Colors.WHITE}  Chọn cấu hình cần thay thế:{Colors.RESET}")
        display_config_list("Cấu Hình Hiện Có")
        
        choice = input(f"{Colors.MAGENTA}  Thay thế số (1-{MAX_CONFIGS}) hoặc 0 để hủy: {Colors.RESET}")
        try:
            idx = int(choice)
            if idx == 0:
                return False
            if 1 <= idx <= MAX_CONFIGS:
                saved_configs[idx - 1] = config.copy()
                print(f"{Colors.GREEN}  ✓ Đã thay thế cấu hình {idx}!{Colors.RESET}")
                return True
        except ValueError:
            pass
        print(f"{Colors.RED}  Lựa chọn không hợp lệ!{Colors.RESET}")
        return False
    else:
        saved_configs.append(config.copy())
        print(f"{Colors.GREEN}  ✓ Đã lưu cấu hình ({len(saved_configs)}/{MAX_CONFIGS})!{Colors.RESET}")
        return True

def main_menu():
    clear_screen()
    print_banner()
    print_divider()
    
    print_section("Các Chức Năng")
    print(f"""
{Colors.RED}  0. ✗ Thoát Chương Trình{Colors.RESET}
{Colors.GREEN}  1. ➤ Gửi Email Mới        {Colors.WHITE}(Nhập cấu hình và gửi email){Colors.RESET}
{Colors.CYAN}  2. ◉ Xem Cấu Hình         {Colors.WHITE}(Xem {len(saved_configs)}/{MAX_CONFIGS} cấu hình đã lưu){Colors.RESET}
{Colors.YELLOW}  3. ⚙ Gửi Nhanh            {Colors.WHITE}(Chọn cấu hình đã lưu để gửi){Colors.RESET}
{Colors.MAGENTA}  4. ✎ Sửa Cấu Hình         {Colors.WHITE}(Sửa một cấu hình đã lưu){Colors.RESET}
{Colors.RED}  5. ✗ Xóa Cấu Hình         {Colors.WHITE}(Xóa một cấu hình đã lưu){Colors.RESET}
    """)
    print_divider()
    
    return input(f"{Colors.MAGENTA}  Chọn chức năng: {Colors.RESET}")

def get_config():
    clear_screen()
    print_banner()
    print_divider()
    
    config = {}
    
    print_section("Cấu Hình SMTP Server")
    print(f"{Colors.WHITE}  ┌─────────────────────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.WHITE}  │ Email            │ SMTP Server            │ Port │ SSL │{Colors.RESET}")
    print(f"{Colors.WHITE}  ├─────────────────────────────────────────────────────────┤{Colors.RESET}")
    print(f"{Colors.WHITE}  │ Gmail            │ smtp.gmail.com         │ 587  │  n  │{Colors.RESET}")
    print(f"{Colors.WHITE}  │ Outlook/Hotmail  │ smtp.office365.com     │ 587  │  n  │{Colors.RESET}")
    print(f"{Colors.WHITE}  │ Yahoo            │ smtp.mail.yahoo.com    │ 587  │  n  │{Colors.RESET}")
    print(f"{Colors.WHITE}  │ Custom (SSL)     │ mail.yourdomain.com    │ 465  │  y  │{Colors.RESET}")
    print(f"{Colors.WHITE}  └─────────────────────────────────────────────────────────┘{Colors.RESET}")
    print(f"{Colors.YELLOW}  💡 Port 587 → SSL: n | Port 465 → SSL: y{Colors.RESET}")
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
    print(f"{Colors.WHITE}  Từ: {config.get('sender', 'N/A')}{Colors.RESET}")
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

def show_config_detail(config):
    """Hiển thị chi tiết một cấu hình"""
    print(f"{Colors.WHITE}  SMTP Server: {config.get('smtp_server', 'N/A')}:{config.get('smtp_port', 'N/A')} {'(SSL)' if config.get('use_ssl') else '(TLS)'}{Colors.RESET}")
    print(f"{Colors.WHITE}  Email gửi: {config.get('sender', 'N/A')}{Colors.RESET}")
    print(f"{Colors.WHITE}  Người nhận: {', '.join(config.get('recipients', []))}{Colors.RESET}")
    print(f"{Colors.WHITE}  Số lần gửi: {config.get('loop_count', 'N/A')}{Colors.RESET}")
    print(f"{Colors.WHITE}  Thời gian chờ: {config.get('delay_min', 'N/A')}s - {config.get('delay_max', 'N/A')}s{Colors.RESET}")
    print(f"{Colors.WHITE}  Tiêu đề: {config.get('subject', 'N/A')}{Colors.RESET}")

def show_configs():
    """Xem danh sách cấu hình đã lưu"""
    clear_screen()
    print_banner()
    print_divider()
    
    if not display_config_list("Danh Sách Cấu Hình Đã Lưu"):
        input(f"\n{Colors.CYAN}  Nhấn Enter để tiếp tục...{Colors.RESET}")
        return
    
    print(f"{Colors.RED}  0. Quay lại{Colors.RESET}")
    print_divider()
    
    choice = input(f"{Colors.MAGENTA}  Xem chi tiết cấu hình số (1-{len(saved_configs)}) hoặc 0 để quay lại: {Colors.RESET}")
    
    try:
        idx = int(choice)
        if idx == 0:
            return
        if 1 <= idx <= len(saved_configs):
            clear_screen()
            print_banner()
            print_divider()
            print_section(f"Chi Tiết Cấu Hình {idx}")
            show_config_detail(saved_configs[idx - 1])
            print_divider()
            input(f"\n{Colors.CYAN}  Nhấn Enter để tiếp tục...{Colors.RESET}")
            return
    except ValueError:
        pass
    
    print(f"{Colors.RED}  Lựa chọn không hợp lệ!{Colors.RESET}")
    time.sleep(1)

def quick_send():
    """Gửi nhanh với cấu hình đã lưu"""
    idx = select_config("Chọn Cấu Hình Để Gửi")
    if idx is not None:
        run_send(saved_configs[idx])

def edit_config():
    """Sửa một cấu hình đã lưu"""
    idx = select_config("Chọn Cấu Hình Để Sửa")
    if idx is None:
        return
    
    config = saved_configs[idx]
    
    clear_screen()
    print_banner()
    print_divider()
    print_section(f"Sửa Cấu Hình {idx + 1}: {config.get('sender', 'N/A')}")
    
    print(f"""
{Colors.WHITE}  1. SMTP Server    : {config.get('smtp_server', 'N/A')}:{config.get('smtp_port', 'N/A')}{Colors.RESET}
{Colors.WHITE}  2. Email gửi      : {config.get('sender', 'N/A')}{Colors.RESET}
{Colors.WHITE}  3. Password       : ********{Colors.RESET}
{Colors.WHITE}  4. Người nhận     : {', '.join(config.get('recipients', []))}{Colors.RESET}
{Colors.WHITE}  5. Số lần gửi     : {config.get('loop_count', 'N/A')}{Colors.RESET}
{Colors.WHITE}  6. Thời gian chờ  : {config.get('delay_min', 'N/A')}s - {config.get('delay_max', 'N/A')}s{Colors.RESET}
{Colors.WHITE}  7. Tiêu đề        : {config.get('subject', 'N/A')}{Colors.RESET}
{Colors.WHITE}  8. Nội dung email{Colors.RESET}
{Colors.RED}  0. Quay lại{Colors.RESET}
    """)
    print_divider()
    
    choice = input(f"{Colors.MAGENTA}  Chọn mục cần sửa: {Colors.RESET}")
    
    if choice == '1':
        print_section("Sửa SMTP Server")
        config['smtp_server'] = input_field("SMTP Server", config['smtp_server'])
        config['smtp_port'] = int(input_field("SMTP Port", str(config['smtp_port'])))
        config['use_ssl'] = input_field("Dùng SSL? (y/n)", "y" if config.get('use_ssl') else "n").lower() == 'y'
        print(f"{Colors.GREEN}  ✓ Đã cập nhật SMTP Server!{Colors.RESET}")
    elif choice == '2':
        print_section("Sửa Email Gửi")
        config['sender'] = input_field("Email của bạn", config['sender'])
        print(f"{Colors.GREEN}  ✓ Đã cập nhật email gửi!{Colors.RESET}")
    elif choice == '3':
        print_section("Sửa Password")
        config['password'] = input_field("Password/App Password")
        print(f"{Colors.GREEN}  ✓ Đã cập nhật password!{Colors.RESET}")
    elif choice == '4':
        print_section("Sửa Người Nhận")
        recipients_str = input_field("Danh sách email nhận (cách nhau bằng dấu phẩy)")
        config['recipients'] = [r.strip() for r in recipients_str.split(',')]
        print(f"{Colors.GREEN}  ✓ Đã cập nhật người nhận!{Colors.RESET}")
    elif choice == '5':
        print_section("Sửa Số Lần Gửi")
        config['loop_count'] = int(input_field("Số lần gửi lặp lại", str(config['loop_count'])))
        print(f"{Colors.GREEN}  ✓ Đã cập nhật số lần gửi!{Colors.RESET}")
    elif choice == '6':
        print_section("Sửa Thời Gian Chờ")
        config['delay_min'] = int(input_field("Thời gian chờ tối thiểu (giây)", str(config['delay_min'])))
        config['delay_max'] = int(input_field("Thời gian chờ tối đa (giây)", str(config['delay_max'])))
        print(f"{Colors.GREEN}  ✓ Đã cập nhật thời gian chờ!{Colors.RESET}")
    elif choice == '7':
        print_section("Sửa Tiêu Đề")
        config['subject'] = input_field("Tiêu đề email", config['subject'])
        print(f"{Colors.GREEN}  ✓ Đã cập nhật tiêu đề!{Colors.RESET}")
    elif choice == '8':
        print_section("Sửa Nội Dung Email")
        config['content'] = input_multiline("Nội dung email mới")
        print(f"{Colors.GREEN}  ✓ Đã cập nhật nội dung!{Colors.RESET}")
    elif choice == '0':
        return
    else:
        print(f"{Colors.RED}  Lựa chọn không hợp lệ!{Colors.RESET}")
    
    time.sleep(1)

def delete_config():
    """Xóa một cấu hình đã lưu"""
    global saved_configs
    
    idx = select_config("Chọn Cấu Hình Để Xóa")
    if idx is None:
        return
    
    config = saved_configs[idx]
    confirm = input(f"{Colors.RED}  Xác nhận xóa cấu hình '{config.get('sender', 'N/A')}'? (y/n): {Colors.RESET}")
    
    if confirm.lower() == 'y':
        saved_configs.pop(idx)
        print(f"{Colors.GREEN}  ✓ Đã xóa cấu hình!{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}  Đã hủy xóa.{Colors.RESET}")
    
    time.sleep(1)

def main():
    while True:
        choice = main_menu()
        
        if choice == '0':
            clear_screen()
            print(f"{Colors.CYAN}  Tạm biệt! 👋{Colors.RESET}\n")
            sys.exit(0)
        elif choice == '1':
            config = get_config()
            run_send(config)
            # Hỏi có muốn lưu cấu hình không
            save_choice = input(f"{Colors.MAGENTA}  Lưu cấu hình này? (y/n): {Colors.RESET}")
            if save_choice.lower() == 'y':
                save_config(config)
            time.sleep(1)
        elif choice == '2':
            show_configs()
        elif choice == '3':
            if saved_configs:
                quick_send()
            else:
                print(f"{Colors.RED}  Chưa có cấu hình nào! Vui lòng chọn 1 để tạo mới.{Colors.RESET}")
                time.sleep(2)
        elif choice == '4':
            if saved_configs:
                edit_config()
            else:
                print(f"{Colors.RED}  Chưa có cấu hình nào! Vui lòng chọn 1 để tạo mới.{Colors.RESET}")
                time.sleep(2)
        elif choice == '5':
            if saved_configs:
                delete_config()
            else:
                print(f"{Colors.RED}  Chưa có cấu hình nào để xóa!{Colors.RESET}")
                time.sleep(2)
        else:
            print(f"{Colors.RED}  Lựa chọn không hợp lệ!{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
