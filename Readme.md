# WiFi Cracker Tool

## Overview

WiFi Cracker Tool is a powerful tool for scanning and analyzing nearby WiFi networks. It is intended for educational and ethical purposes only. Unauthorized use of this tool to access WiFi networks without permission may violate applicable laws.

## Features

- Scans for available WiFi networks
- Displays detailed information about detected networks, including BSSID, channel, encryption, power, ESSID, WPS status, manufacturer, and number of users
- Supports enabling monitor mode on wireless interfaces
- Automatically installs necessary dependencies

## Requirements

- Python 3.x
- Root privileges
- Supported on Linux (Debian-based distributions recommended)

## Tools Used

- `airmon-ng`
- `airodump-ng`
- `aireplay-ng`
- `aircrack-ng`
- `hashcat`
- `crunch`
- `cap2hccapx.bin`
- `reaver`
- `bettercap`
- `bully`

## Installation

1. Clone this repository:

    git clone https://github.com/eude313/Wifi-cracker.git
    cd CRACKER
    

2. Ensure Python dependencies are installed. The script will automatically install missing packages.

## Usage

1. **Run the script as root:**

    sudo python3 wifi.py
    

2. **Read and agree to the license:**

    - The script will display the MIT License and ask for confirmation. You must agree to the license to use the tool.

3. **Enable Monitor Mode:**

    - The script will enable monitor mode on your wireless interface (e.g., `wlan0`).

4. **Scan for Networks:**

    - The script will scan for nearby WiFi networks. Press `Ctrl+C` to stop the scan and proceed to network selection.

5. **Display Network Information:**

    - The script will display detailed information about detected networks.

## Example Output

    | Number |      BSSID        | Channel | Encryption | Power |   ESSID      | WPS | Manufacturer | Users |
    |--------|-------------------|---------|------------|-------|--------------|-----|--------------|-------|
    |   1    | 00:14:22:01:23:45 |    6    |    WPA2    |  -45  | MyNetwork    |  No |    Apple     |   3   |
    |   2    | 00:14:22:01:23:46 |    11   |    WEP     |  -50  | GuestNetwork | Yes |   Cisco      |   1   |


## Important Notes

- **Legal Disclaimer:** This tool is intended for educational and ethical purposes only. Unauthorized use of this tool to access WiFi networks without permission is illegal and punishable by law. The author is not responsible for any misuse of this tool.

- **Dependencies:** The script checks for necessary tools and installs them if missing. Ensure you have a stable internet connection for this process.

## License

This project is licensed under the MIT License - see the [MIT ](LICENSE) file for details.

## Author

- Eude313



Enjoy responsibly and respect privacy!
