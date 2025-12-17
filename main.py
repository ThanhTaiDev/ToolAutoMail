import smtplib
import time
import random
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    print(f"{Colors.GREEN}  ➤ {label} {Colors.WHITE}(nhap 'END' de ket thuc):{Colors.RESET}")
    lines = []
    while True:
        line = input(f"{Colors.WHITE}    | {Colors.RESET}")
        if line.strip().upper() == 'END':
            break
        lines.append(line)
    return '\n'.join(lines)

def send_email(sender, password, recipients, subject_template, content):
    random_number = random.randint(1000000000000000, 9999999999999999)
    subject = f"{subject_template} #{random_number}"
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()
    
    return subject

def main_menu():
    clear_screen()
    print_banner()
    print_divider()
    
    print_section("Available Options")
    print(f"""
{Colors.RED}  0. ✗ Exit Program{Colors.RESET}
{Colors.GREEN}  1. ➤ Start Send Email{Colors.RESET}
{Colors.CYAN}  2. ◉ Show Current Config{Colors.RESET}
{Colors.YELLOW}  3. ⚙ Quick Send (use saved config){Colors.RESET}
    """)
    print_divider()
    
    return input(f"{Colors.MAGENTA}  Select option: {Colors.RESET}")

def get_config():
    clear_screen()
    print_banner()
    print_divider()
    
    config = {}
    
    print_section("Email Configuration")
    config['sender'] = input_field("Sender Email")
    config['password'] = input_field("App Password")
    
    print_section("Recipients (comma separated)")
    recipients_str = input_field("Recipients")
    config['recipients'] = [r.strip() for r in recipients_str.split(',')]
    
    print_section("Send Settings")
    config['loop_count'] = int(input_field("Loop Count", "10"))
    config['delay_min'] = int(input_field("Delay Min (seconds)", "5"))
    config['delay_max'] = int(input_field("Delay Max (seconds)", "10"))
    
    print_section("Email Content")
    config['subject'] = input_field("Subject Template", "Intellectual Property Appeal Contact Form")
    config['content'] = input_multiline("Email Content")
    
    return config

def run_send(config):
    clear_screen()
    print_banner()
    print_divider()
    print_section("Sending Emails...")
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
                config['content']
            )
            success += 1
            print(f"{Colors.GREEN}  ✓ [{i}/{config['loop_count']}] Sent successfully!{Colors.RESET}")
            print(f"{Colors.WHITE}    Subject: {subject}{Colors.RESET}")
        except Exception as e:
            failed += 1
            print(f"{Colors.RED}  ✗ [{i}/{config['loop_count']}] Failed: {e}{Colors.RESET}")
        
        if i < config['loop_count']:
            delay = random.randint(config['delay_min'], config['delay_max'])
            print(f"{Colors.YELLOW}    Waiting {delay}s...{Colors.RESET}\n")
            time.sleep(delay)
    
    print_divider()
    print(f"\n{Colors.GREEN}  ✓ Complete! Success: {success} | Failed: {failed}{Colors.RESET}")
    input(f"\n{Colors.CYAN}  Press Enter to continue...{Colors.RESET}")

def show_config(config):
    clear_screen()
    print_banner()
    print_divider()
    print_section("Current Configuration")
    
    if not config:
        print(f"{Colors.RED}  No config saved yet!{Colors.RESET}")
    else:
        print(f"{Colors.WHITE}  Sender: {config.get('sender', 'N/A')}{Colors.RESET}")
        print(f"{Colors.WHITE}  Recipients: {', '.join(config.get('recipients', []))}{Colors.RESET}")
        print(f"{Colors.WHITE}  Loop Count: {config.get('loop_count', 'N/A')}{Colors.RESET}")
        print(f"{Colors.WHITE}  Delay: {config.get('delay_min', 'N/A')}s - {config.get('delay_max', 'N/A')}s{Colors.RESET}")
        print(f"{Colors.WHITE}  Subject: {config.get('subject', 'N/A')}{Colors.RESET}")
    
    print_divider()
    input(f"\n{Colors.CYAN}  Press Enter to continue...{Colors.RESET}")

def main():
    config = {}
    
    while True:
        choice = main_menu()
        
        if choice == '0':
            clear_screen()
            print(f"{Colors.CYAN}  Goodbye! 👋{Colors.RESET}\n")
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
                print(f"{Colors.RED}  No config! Please use option 1 first.{Colors.RESET}")
                time.sleep(2)
        else:
            print(f"{Colors.RED}  Invalid option!{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()

