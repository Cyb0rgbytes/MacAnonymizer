🚀 MacAnonymizer Pro - Advanced MAC Address Manipulation Tool

<p align="center"> <img src="https://img.shields.io/badge/Version-2.0-brightgreen" alt="Version"> <img src="https://img.shields.io/badge/Python-3.7+-blue" alt="Python"> <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License"> <img src="https://img.shields.io/badge/Author-Cyb0rgBytes-purple" alt="Author"> </p><p align="center"> ⚡ <strong>Revolutionizing network discovery with style, speed, and precision!</strong> ⚡ </p>


Professional-grade MAC address manipulation with stunning terminal visuals


✨ Elevate Your Network Security & Privacy

MacAnonymizer Pro transforms the simple concept of MAC address changing into a powerful, feature-rich toolkit with enterprise-grade capabilities. Perfect for penetration testers, network administrators, privacy-conscious users, and cybersecurity enthusiasts.
🆕 What's New in Version 2.0
Feature	v1.0 (Legacy)	v2.0 (Pro)
Platform Support	Linux only	Linux, Windows, macOS
Visual Interface	Basic colors	Rich animations, progress bars, tables
MAC Validation	Regex only	Professional validation with vendor lookup
Network Testing	❌ Not available	✅ Speed test before/after changes
Random Generation	❌ Not available	✅ With vendor-specific OUIs
Rollback System	❌ Not available	✅ One-click restore
Interface Scanning	❌ Not available	✅ Full network interface discovery
📋 Table of Contents

    🌟 Features

    🚀 Quick Start

    📦 Installation

    🎮 Usage Guide

    🔧 Advanced Features

    🎨 Visual Effects

    📁 Project Structure

    🤝 Contributing

    ⚠️ Legal Disclaimer

    📄 License

🌟 Features
🎯 Core Capabilities

    Cross-Platform Support: Works seamlessly on Linux, Windows, and macOS

    Professional MAC Validation: Supports all formats (colon, hyphen, dot, no separator)

    Vendor Database: Auto-detects and displays manufacturer from MAC OUI

    Secure Operations: Proper error handling and permission management

⚡ Performance & Reliability

    Network Testing: Integrated speed test to measure performance impact

    Rollback System: Automatic backup and one-click restoration

    Validation Checks: Pre-flight verification before making changes

    Error Recovery: Graceful handling of failed operations

🎨 Visual Excellence

    Terminal Animations: Matrix, decrypt, rainbow, and glitch effects

    Rich UI Components: Progress bars, tables, panels, and live displays

    Color-Coded Status: Instant visual feedback for all operations

    Interactive Interface: User-friendly command structure with help system

🔒 Advanced Security

    Random MAC Generation: Create untraceable addresses

    Vendor-Specific Random: Generate MACs that match specific manufacturers

    Network Analysis: Comprehensive interface scanning and reporting

    Change Logging: Detailed audit trail of all modifications

🚀 Quick Start
Clone & Run
bash

# Clone the repository
git clone https://github.com/Cyb0rgBytes/MacAnonymizer.git
cd MacAnonymizer

# Install dependencies
pip install -r requirements.txt

# Run with elevated privileges
sudo python3 MacAnonymizerPro.py -l

One-Line Installation
bash

# All-in-one command (Linux/macOS)
git clone https://github.com/Cyb0rgBytes/MacAnonymizer.git && \
cd MacAnonymizer && \
pip install -r requirements.txt && \
sudo python3 MacAnonymizerPro.py --help

📦 Installation
Requirements
txt

Python 3.8 or higher
Administrator/Root privileges
Active network interface

Dependencies

Create a requirements.txt file with:
txt

# requirements.txt
rich>=13.0.0
terminaltexteffects>=1.0.0
speedtest-cli>=2.1.3
netifaces>=0.11.0
colorama>=0.4.6
argparse>=1.4.0

Install all dependencies:
bash

pip install -r requirements.txt

Platform-Specific Notes
Platform	Command	Notes
Linux	sudo python3 MacAnonymizerPro.py	Uses ip command (modern)
Windows	Run as Administrator	Uses PowerShell commands
macOS	sudo python3 MacAnonymizerPro.py	Uses ifconfig
🎮 Usage Guide
Basic Commands
bash

# List all network interfaces
sudo python3 MacAnonymizerPro.py -l

# Change to specific MAC address
sudo python3 MacAnonymizerPro.py -i eth0 -m 00:11:22:33:44:55

# Generate and set random MAC
sudo python3 MacAnonymizerPro.py -i eth0 -r

# Restore original MAC address
sudo python3 MacAnonymizerPro.py -i eth0 --restore

Advanced Operations
bash

# Random MAC with specific vendor (Microsoft example)
sudo python3 MacAnonymizerPro.py -i eth0 -r --vendor 00:50:C2

# Test network speed before and after change
sudo python3 MacAnonymizerPro.py -i wlan0 -r --test

# Change MAC with different format output
sudo python3 MacAnonymizerPro.py -i eth0 -m 001122334455 --format hyphen

# Verbose output for debugging
sudo python3 MacAnonymizerPro.py -i eth0 -m 00:11:22:33:44:55 -v

Command Reference
Option	Short	Description	Example
--interface	-i	Network interface name	-i eth0
--mac	-m	Specific MAC address	-m 00:11:22:33:44:55
--random	-r	Generate random MAC	-r
--vendor		Vendor OUI for random MAC	--vendor 00:50:C2
--list	-l	List all interfaces	-l
--test		Run speed test	--test
--restore		Restore original MAC	--restore
--format		MAC format (colon/hyphen/dot/none)	--format hyphen
--verbose	-v	Detailed output	-v
🔧 Advanced Features
1. Vendor OUI Database

The tool includes a comprehensive vendor database:
python

VENDOR_OUI = {
    "00:50:C2": "Microsoft",
    "00:0C:29": "VMware",
    "00:1A:11": "Google",
    "00:1B:63": "Apple",
    "00:1E:65": "Cisco",
    "00:24:E8": "Dell",
    "3C:06:30": "Intel",
    "08:00:27": "VirtualBox",
    "52:54:00": "QEMU",
    "B8:27:EB": "Raspberry Pi"
}

2. Network Performance Testing

Compare network speed before and after MAC changes:
bash

# Results appear in a beautiful comparison table
┌─────────────────────────────────────────┐
│   Network Performance Comparison        │
├─────────────────────────────────────────┤
│ Metric     Before     After    Difference│
│ Download   95.2 Mbps  96.1 Mbps  +0.9 Mbps│
│ Upload     42.5 Mbps  43.2 Mbps  +0.7 Mbps│
│ Ping       24 ms      23 ms      -1 ms    │
└─────────────────────────────────────────┘

3. Random MAC Generation Algorithms

    Completely Random: Generates truly anonymous MAC addresses

    Vendor-Specific: Maintains vendor OUI for compatibility

    Avoids Special Addresses: Skips multicast/broadcast ranges

    Format Consistency: Outputs in user-selected format

4. Cross-Platform Command Mapping
python

# Linux
commands = [
    ['sudo', 'ip', 'link', 'set', interface, 'down'],
    ['sudo', 'ip', 'link', 'set', interface, 'address', normalized_mac],
    ['sudo', 'ip', 'link', 'set', interface, 'up']
]

# Windows (PowerShell)
ps_commands = """
$adapter = Get-NetAdapter -Name "{interface}"
Disable-NetAdapter -Name "{interface}" -Confirm:$false
Set-NetAdapter -Name "{interface}" -MacAddress "{mac}"
Enable-NetAdapter -Name "{interface}" -Confirm:$false
"""

# macOS
commands = [
    ['sudo', 'ifconfig', interface, 'down'],
    ['sudo', 'ifconfig', interface, 'ether', normalized_mac],
    ['sudo', 'ifconfig', interface, 'up']
]

🎨 Visual Effects Gallery
Startup Animation
text

╔══════════════════════════════════════════════════════════╗
║                   MacAnonymizer Pro v2.0                 ║
║         Advanced MAC Address Manipulation Tool           ║
╚══════════════════════════════════════════════════════════╝

Decrypt effect with sequential character reveal
Interface Discovery Table
text

┌─────────────────────────────────────────────────────────────────┐
│                     Network Interfaces                          │
├─────────────┬───────────────────┬──────────────┬──────┬────────┤
│ Interface   │ MAC Address       │ Vendor       │ IP   │ Status │
├─────────────┼───────────────────┼──────────────┼──────┼────────┤
│ eth0        │ 00:11:22:33:44:55 │ Intel        │ ...  │ UP     │
│ wlan0       │ AA:BB:CC:DD:EE:FF │ Apple        │ ...  │ UP     │
│ veth1       │ 08:00:27:XX:XX:XX │ VirtualBox   │ N/A  │ DOWN   │
└─────────────┴───────────────────┴──────────────┴──────┴────────┘

Progress Indicators
text

[████████████████████░░░░░░░░] 75% Changing MAC address...

Success/Failure Animations
text

✅ SUCCESS!                  ❌ FAILURE!
MAC changed successfully!   Operation failed!

📁 Project Structure
text

MacAnonymizer/
├── MacAnonymizerPro.py     # Main application
├── requirements.txt        # Dependencies
├── README.md              # This documentation
├── mac_backup.json        # Auto-generated backup file
├── examples/              # Usage examples
│   ├── basic_usage.sh
│   ├── advanced_operations.sh
│   └── automation_script.py
└── docs/                  # Additional documentation
    ├── platform_specific.md
    ├── troubleshooting.md
    └── api_reference.md

Key Components

    Animator Class - Handles all visual effects and animations

    MacAddress Class - Validation, formatting, and vendor lookup

    NetworkInterface Class - Cross-platform interface management

    NetworkTester Class - Speed testing and performance comparison

    MacAnonymizerPro Class - Main application controller

🤝 Contributing

We welcome contributions! Here's how you can help:
Development Setup
bash

# 1. Fork the repository
# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/MacAnonymizer.git

# 3. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# 4. Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# 5. Create a feature branch
git checkout -b feature/amazing-feature

Contribution Areas

    Add New Vendor OUIs: Expand the vendor database

    Platform Extensions: Improve Windows/macOS support

    Animation Effects: Create new terminal animations

    Testing: Write unit tests for components

    Documentation: Improve guides and examples

Pull Request Process

    Update documentation reflecting changes

    Add tests for new functionality

    Ensure all tests pass

    Submit PR with detailed description

⚠️ Legal Disclaimer

IMPORTANT: Use this tool responsibly and only on networks you own or have explicit permission to test.
Legal Considerations

    MAC address spoofing may violate terms of service

    Some networks track MAC addresses for security

    Corporate networks may have policies against MAC changing

    Always obtain proper authorization before testing

Ethical Use Cases

    Privacy protection on public Wi-Fi

    Network testing in lab environments

    Security research with permission

    Educational purposes in controlled settings

Limitations

    Some network cards don't support MAC changing

    Virtual machines may have restrictions

    Enterprise networks may detect and block spoofed MACs

    Not all OS/driver combinations are supported

📄 License
text

MIT License

Copyright (c) 2024 Cyb0rgBytes

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

🌟 Acknowledgments

Created by: Cyb0rgBytes

Special Thanks To:

    The open-source community for amazing Python libraries

    Network security researchers for inspiration

    Beta testers who helped refine the tool

Related Projects:

    macchanger - Original inspiration

    SpoofMAC - Alternative implementation

<div align="center">
🌟 Star This Repository if You Find It Useful!

https://img.shields.io/github/stars/Cyb0rgBytes/MacAnonymizer?style=for-the-badge
https://img.shields.io/github/forks/Cyb0rgBytes/MacAnonymizer?style=for-the-badge
https://img.shields.io/github/issues/Cyb0rgBytes/MacAnonymizer?style=for-the-badge

📧 Contact: Open an Issue | 🐦 Twitter: @Cyb0rgBytes
</div>
