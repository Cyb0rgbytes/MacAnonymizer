#!/usr/bin/env python3
"""
Title: MacAnonymizer Pro
Description: Advanced cross-platform MAC address manipulation tool with visual effects
Author: Cyb0rgBytes
Version: 2.0
Python: 3.8+
Features: Cross-platform (Linux/Windows/macOS), animations, random MAC generation, vendor lookup, speed testing, rollback system
"""
import os
import sys
import re
import time
import random
import platform
import subprocess
import argparse
import json
from datetime import datetime
from typing import Optional, Tuple, Dict, List
from enum import Enum

# Third-party imports (install via: pip install -r requirements.txt)
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich import box
    import netifaces
    import speedtest
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    
    # Try to import terminaltexteffects, but it's optional
    try:
        from terminaltexteffects.effects import Decrypt
        TERMINALTEXTEFFECTS_AVAILABLE = True
    except ImportError:
        TERMINALTEXTEFFECTS_AVAILABLE = False
        print("[Warning] terminaltexteffects not installed. Animations will be limited.")
        print("Install with: pip install terminaltexteffects")
        
except ImportError as e:
    print(f"Missing dependencies. Install with: pip install -r requirements.txt")
    print(f"Error details: {e}")
    sys.exit(1)

# ============================================================================
# ENUMS AND CONSTANTS
# ============================================================================

class Platform(Enum):
    """Supported operating systems"""
    LINUX = "linux"
    WINDOWS = "windows"
    MACOS = "darwin"
    UNKNOWN = "unknown"

class MacFormat(Enum):
    """MAC address formats"""
    COLON = ":"      # 00:11:22:33:44:55
    HYPHEN = "-"     # 00-11-22-33-44-55
    DOT = "."        # 0011.2233.4455
    NONE = ""        # 001122334455

class AnimationType(Enum):
    """Available animation effects"""
    MATRIX = "matrix"
    DECRYPT = "decrypt"
    RAINBOW = "rainbow"
    GLITCH = "glitch"
    SCAN = "scan"

# Vendor OUI database (simplified - would be larger in production)
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

# ============================================================================
# ANIMATION ENGINE
# ============================================================================

class Animator:
    """Handles terminal animations and visual effects"""
    
    def __init__(self, console: Console):
        self.console = console
        self.animation_speed = 0.03
        self.use_advanced_animations = TERMINALTEXTEFFECTS_AVAILABLE
    
    def show_startup_animation(self):
        """Display startup animation sequence"""
        title = """
╔══════════════════════════════════════════════════════════╗
║                   MacAnonymizer Pro v2.0                 ║
║         Advanced MAC Address Manipulation Tool           ║
╚══════════════════════════════════════════════════════════╝
        """
        
        # Use terminaltexteffects if available
        if self.use_advanced_animations:
            try:
                # Create a decrypt effect instance
                effect = Decrypt(title)
                
                # Play the animation
                with effect.terminal_output() as terminal:
                    for frame in effect:
                        terminal.print(frame)
                self.console.print()
                return
            except Exception as e:
                self.console.print(f"[yellow]Advanced animation failed, using fallback: {e}[/yellow]")
        
        # Fallback animation using rich
        self.console.print("\n" * 2)
        for i, char in enumerate(title):
            if i % 3 == 0:
                self.console.print(char, end="", style="bold green")
            elif i % 3 == 1:
                self.console.print(char, end="", style="bold cyan")
            else:
                self.console.print(char, end="", style="bold blue")
            time.sleep(0.001)
        self.console.print("\n" * 2)
    
    def progress_spinner(self, message: str, duration: float = 1.5):
        """Show a spinner with progress"""
        with self.console.status(f"[bold yellow]{message}") as status:
            time.sleep(duration)
    
    def typewriter_effect(self, text: str, style: str = "bold white"):
        """Typewriter effect for text output"""
        for char in text:
            self.console.print(char, end="", style=style)
            time.sleep(0.02)
        self.console.print()
    
    def success_animation(self, message: str):
        """Display success animation"""
        success_art = """
        ╔══════════════════════════════╗
        ║        ✅ SUCCESS!           ║
        ╚══════════════════════════════╝
        """
        self.console.print(Panel.fit(
            f"[bold green]{success_art}\n[bold cyan]{message}[/bold cyan]",
            border_style="green",
            box=box.DOUBLE
        ))
    
    def failure_animation(self, message: str):
        """Display failure animation"""
        failure_art = """
        ╔══════════════════════════════╗
        ║        ❌ FAILURE!           ║
        ╚══════════════════════════════╝
        """
        self.console.print(Panel.fit(
            f"[bold red]{failure_art}\n[bold yellow]{message}[/bold yellow]",
            border_style="red",
            box=box.DOUBLE
        ))
    
    def network_scan_animation(self):
        """Network scanning animation"""
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        for _ in range(20):
            for frame in frames:
                self.console.print(f"\r[bold blue]Scanning network interfaces {frame}", end="")
                time.sleep(0.1)
        self.console.print()

# ============================================================================
# MAC ADDRESS VALIDATOR & FORMATTER
# ============================================================================

class MacAddress:
    """MAC address validation and formatting"""
    
    @staticmethod
    def is_valid(mac: str) -> bool:
        """Validate MAC address format"""
        patterns = [
            r'^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$',  # Colon
            r'^([0-9A-Fa-f]{2}[-]){5}([0-9A-Fa-f]{2})$',  # Hyphen
            r'^([0-9A-Fa-f]{4}[.]){2}([0-9A-Fa-f]{4})$',  # Dot
            r'^[0-9A-Fa-f]{12}$'                          # No separator
        ]
        
        for pattern in patterns:
            if re.match(pattern, mac):
                return True
        return False
    
    @staticmethod
    def normalize(mac: str, format: MacFormat = MacFormat.COLON) -> str:
        """Normalize MAC address to specified format"""
        # Remove all separators
        clean_mac = re.sub(r'[:\-\.]', '', mac).upper()
        
        if len(clean_mac) != 12:
            raise ValueError(f"Invalid MAC address length: {clean_mac}")
        
        if format == MacFormat.NONE:
            return clean_mac
        elif format == MacFormat.DOT:
            return f"{clean_mac[:4]}.{clean_mac[4:8]}.{clean_mac[8:]}"
        elif format == MacFormat.HYPHEN:
            return '-'.join([clean_mac[i:i+2] for i in range(0, 12, 2)])
        else:  # COLON (default)
            return ':'.join([clean_mac[i:i+2] for i in range(0, 12, 2)])
    
    @staticmethod
    def get_vendor(mac: str) -> str:
        """Get vendor from MAC OUI"""
        try:
            normalized = MacAddress.normalize(mac, MacFormat.COLON)
            oui = normalized[:8]  # First 3 bytes
            
            # Try exact match
            vendor = VENDOR_OUI.get(oui)
            if vendor:
                return vendor
            
            # Try partial match (first 2 bytes)
            oui_prefix = normalized[:5]
            for key, value in VENDOR_OUI.items():
                if key.startswith(oui_prefix):
                    return value
            
            return "Unknown Vendor"
        except:
            return "Unknown Vendor"
    
    @staticmethod
    def generate_random(vendor_oui: Optional[str] = None) -> str:
        """Generate random MAC address"""
        if vendor_oui:
            # Validate OUI format
            if not re.match(r'^[0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}$', vendor_oui):
                raise ValueError("Invalid OUI format. Use format like 00:11:22")
            
            # Clean OUI
            oui = re.sub(r'[:\-]', '', vendor_oui).upper()
            random_part = ''.join(f"{random.randint(0, 255):02X}" for _ in range(3))
            return MacAddress.normalize(oui + random_part)
        else:
            # Generate completely random (ensure not multicast, not broadcast)
            first_byte = random.randint(0x00, 0xFD)  # Avoid FE and FF
            if first_byte & 0x01:  # If multicast bit is set
                first_byte &= 0xFE  # Clear multicast bit
            
            mac_bytes = [first_byte] + [random.randint(0x00, 0xFF) for _ in range(5)]
            return ':'.join(f"{b:02X}" for b in mac_bytes)

# ============================================================================
# NETWORK INTERFACE MANAGER
# ============================================================================

class NetworkInterface:
    """Network interface operations"""
    
    def __init__(self, console: Console):
        self.console = console
        self.system = self._detect_platform()
        self.original_mac = None
        self.current_mac = None
        
    def _detect_platform(self) -> Platform:
        """Detect operating system"""
        system = platform.system().lower()
        if system == "linux":
            return Platform.LINUX
        elif system == "windows":
            return Platform.WINDOWS
        elif system == "darwin":
            return Platform.MACOS
        else:
            return Platform.UNKNOWN
    
    def get_interfaces(self) -> List[Dict[str, str]]:
        """Get list of network interfaces"""
        interfaces = []
        
        try:
            iface_list = netifaces.interfaces()
            
            for iface in iface_list:
                # Skip loopback and virtual interfaces
                if iface.startswith(('lo', 'virbr', 'docker', 'veth')):
                    continue
                
                try:
                    addrs = netifaces.ifaddresses(iface)
                    if netifaces.AF_LINK in addrs:
                        mac = addrs[netifaces.AF_LINK][0]['addr']
                        vendor = MacAddress.get_vendor(mac)
                        
                        # Get IP address if available
                        ip = "N/A"
                        if netifaces.AF_INET in addrs:
                            ip = addrs[netifaces.AF_INET][0]['addr']
                        
                        interfaces.append({
                            'name': iface,
                            'mac': mac,
                            'vendor': vendor,
                            'ip': ip,
                            'status': 'UP' if mac != '00:00:00:00:00:00' else 'DOWN'
                        })
                except:
                    continue
                    
        except Exception as e:
            self.console.print(f"[bold red]Error scanning interfaces: {e}[/bold red]")
        
        return interfaces
    
    def get_current_mac(self, interface: str) -> Optional[str]:
        """Get current MAC address of interface"""
        try:
            if self.system == Platform.LINUX:
                # Linux: use ip command
                result = subprocess.run(
                    ['ip', 'link', 'show', interface],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    match = re.search(r'link/ether\s+([0-9a-f:]{17})', result.stdout)
                    if match:
                        return match.group(1)
            
            elif self.system == Platform.WINDOWS:
                # Windows: use getmac command
                result = subprocess.run(
                    ['getmac', '/v', '/fo', 'csv'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    encoding='utf-8'
                )
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if interface in line:
                            match = re.search(r'([0-9A-F-]{17})', line)
                            if match:
                                return match.group(1).replace('-', ':')
            
            elif self.system == Platform.MACOS:
                # macOS: use ifconfig
                result = subprocess.run(
                    ['ifconfig', interface],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    match = re.search(r'ether\s+([0-9a-f:]{17})', result.stdout)
                    if match:
                        return match.group(1)
        
        except Exception as e:
            self.console.print(f"[bold red]Error getting MAC: {e}[/bold red]")
        
        return None
    
    def change_mac(self, interface: str, new_mac: str, backup: bool = True) -> bool:
        """Change MAC address of interface"""
        try:
            # Backup original MAC
            if backup:
                self.original_mac = self.get_current_mac(interface)
            
            normalized_mac = MacAddress.normalize(new_mac)
            
            self.console.print(f"[bold cyan]Changing MAC on {interface} to {normalized_mac}...[/bold cyan]")
            
            if self.system == Platform.LINUX:
                # Linux using ip command (modern)
                commands = [
                    ['sudo', 'ip', 'link', 'set', interface, 'down'],
                    ['sudo', 'ip', 'link', 'set', interface, 'address', normalized_mac],
                    ['sudo', 'ip', 'link', 'set', interface, 'up'],
                    ['sudo', 'ip', 'link', 'show', interface]
                ]
            
            elif self.system == Platform.WINDOWS:
                # Windows using PowerShell (run as admin)
                ps_commands = f"""
                $adapter = Get-NetAdapter -Name "{interface}"
                Disable-NetAdapter -Name "{interface}" -Confirm:$false
                Set-NetAdapter -Name "{interface}" -MacAddress "{normalized_mac}"
                Enable-NetAdapter -Name "{interface}" -Confirm:$false
                """
                
                commands = [
                    ['powershell', '-Command', ps_commands]
                ]
            
            elif self.system == Platform.MACOS:
                # macOS
                commands = [
                    ['sudo', 'ifconfig', interface, 'down'],
                    ['sudo', 'ifconfig', interface, 'ether', normalized_mac],
                    ['sudo', 'ifconfig', interface, 'up'],
                    ['ifconfig', interface]
                ]
            
            else:
                raise NotImplementedError(f"Platform {self.system} not supported")
            
            # Execute commands
            for cmd in commands:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode != 0:
                    self.console.print(f"[bold red]Command failed: {' '.join(cmd)}[/bold red]")
                    self.console.print(f"[yellow]Error: {result.stderr}[/yellow]")
                    return False
            
            # Verify change
            time.sleep(2)  # Allow interface to settle
            self.current_mac = self.get_current_mac(interface)
            
            if self.current_mac and MacAddress.normalize(self.current_mac) == normalized_mac:
                return True
            else:
                return False
                
        except Exception as e:
            self.console.print(f"[bold red]Error changing MAC: {e}[/bold red]")
            return False
    
    def restore_mac(self, interface: str) -> bool:
        """Restore original MAC address"""
        if not self.original_mac:
            self.console.print("[bold yellow]No original MAC address stored[/bold yellow]")
            return False
        
        self.console.print(f"[bold cyan]Restoring original MAC: {self.original_mac}[/bold cyan]")
        return self.change_mac(interface, self.original_mac, backup=False)

# ============================================================================
# NETWORK PERFORMANCE TESTER
# ============================================================================

class NetworkTester:
    """Network performance testing"""
    
    def __init__(self, console: Console):
        self.console = console
        self.results = {}
    
    def run_test(self, test_type: str = "quick") -> Dict:
        """Run network speed test"""
        self.console.print("[bold cyan]Running network performance test...[/bold cyan]")
        
        try:
            import speedtest
            st = speedtest.Speedtest()
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=self.console,
                transient=True
            ) as progress:
                
                # Get best server
                task1 = progress.add_task("[yellow]Finding optimal server...", total=100)
                st.get_best_server()
                progress.update(task1, completed=100)
                
                if test_type == "full":
                    # Download test
                    task2 = progress.add_task("[green]Testing download speed...", total=100)
                    download_speed = st.download() / 1_000_000  # Convert to Mbps
                    progress.update(task2, completed=100)
                    
                    # Upload test
                    task3 = progress.add_task("[blue]Testing upload speed...", total=100)
                    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
                    progress.update(task3, completed=100)
                else:
                    # Quick test (download only)
                    task2 = progress.add_task("[green]Testing download speed...", total=100)
                    download_speed = st.download() / 1_000_000
                    progress.update(task2, completed=100)
                    upload_speed = 0
                
                # Ping
                ping = st.results.ping
                
                self.results = {
                    'download': f"{download_speed:.2f} Mbps",
                    'upload': f"{upload_speed:.2f} Mbps" if upload_speed else "Not tested",
                    'ping': f"{ping:.2f} ms",
                    'server': st.results.server['name'],
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                return self.results
                
        except ImportError:
            self.console.print("[bold yellow]speedtest-cli not installed. Install with: pip install speedtest-cli[/bold yellow]")
            return {}
        except Exception as e:
            self.console.print(f"[bold red]Speed test failed: {e}[/bold red]")
            return {}

    def display_results(self, before_results: Dict, after_results: Dict):
        """Compare and display test results"""
        if not before_results or not after_results:
            return
        
        table = Table(title="Network Performance Comparison", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Before Change", style="green")
        table.add_column("After Change", style="yellow")
        table.add_column("Difference", style="magenta")
        
        for key in ['download', 'upload', 'ping']:
            if key in before_results and key in after_results:
                # Extract numeric values
                before_val = float(before_results[key].split()[0])
                after_val = float(after_results[key].split()[0])
                
                # Calculate difference
                if key == 'ping':  # Lower is better
                    diff = before_val - after_val
                    diff_str = f"{diff:+.2f} ms"
                    diff_style = "green" if diff > 0 else "red"
                else:  # Higher is better (download/upload)
                    diff = after_val - before_val
                    diff_str = f"{diff:+.2f} Mbps"
                    diff_style = "green" if diff > 0 else "red"
                
                table.add_row(
                    key.title(),
                    before_results[key],
                    after_results[key],
                    Text(diff_str, style=diff_style)
                )
        
        self.console.print(table)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

class MacAnonymizerPro:
    """Main application class"""
    
    def __init__(self):
        self.console = Console()
        self.animator = Animator(self.console)
        self.interface_mgr = NetworkInterface(self.console)
        self.network_tester = NetworkTester(self.console)
        self.backup_file = "mac_backup.json"
        
        # Show startup animation
        self.animator.show_startup_animation()
    
    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description="Advanced MAC Address Manipulation Tool",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s -i eth0 -m 00:11:22:33:44:55    # Set specific MAC
  %(prog)s -i eth0 -r                       # Set random MAC
  %(prog)s -i eth0 -r --vendor 00:50:C2    # Random MAC with vendor OUI
  %(prog)s -l                               # List interfaces
  %(prog)s -i eth0 --test                   # Test network before/after
  %(prog)s -i eth0 --restore                # Restore original MAC
            """
        )
        
        parser.add_argument("-i", "--interface", help="Network interface name")
        parser.add_argument("-m", "--mac", help="New MAC address")
        parser.add_argument("-r", "--random", action="store_true", help="Generate random MAC")
        parser.add_argument("--vendor", help="Vendor OUI for random MAC (e.g., 00:50:C2)")
        parser.add_argument("-l", "--list", action="store_true", help="List all interfaces")
        parser.add_argument("--test", action="store_true", help="Run speed test before/after")
        parser.add_argument("--restore", action="store_true", help="Restore original MAC")
        parser.add_argument("--format", choices=["colon", "hyphen", "dot", "none"], 
                          default="colon", help="MAC address format")
        parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
        
        return parser.parse_args()
    
    def display_interface_table(self, interfaces: List[Dict[str, str]]):
        """Display interfaces in a formatted table"""
        table = Table(title="Network Interfaces", box=box.ROUNDED)
        
        table.add_column("Interface", style="cyan", no_wrap=True)
        table.add_column("MAC Address", style="green")
        table.add_column("Vendor", style="yellow")
        table.add_column("IP Address", style="blue")
        table.add_column("Status", justify="right")
        
        for iface in interfaces:
            status_color = "green" if iface['status'] == 'UP' else "red"
            table.add_row(
                iface['name'],
                iface['mac'],
                iface['vendor'],
                iface['ip'],
                Text(iface['status'], style=status_color)
            )
        
        self.console.print(table)
    
    def run(self):
        """Main application loop"""
        args = self.parse_arguments()
        
        # List interfaces if requested
        if args.list:
            self.animator.network_scan_animation()
            interfaces = self.interface_mgr.get_interfaces()
            if interfaces:
                self.display_interface_table(interfaces)
            else:
                self.console.print("[bold red]No interfaces found[/bold red]")
            return
        
        # Validate interface
        if not args.interface:
            self.console.print("[bold red]Error: Interface not specified. Use -i or --interface[/bold red]")
            self.console.print("[yellow]Available interfaces:[/yellow]")
            interfaces = self.interface_mgr.get_interfaces()
            self.display_interface_table(interfaces)
            return
        
        # Check if interface exists
        interfaces = self.interface_mgr.get_interfaces()
        interface_names = [iface['name'] for iface in interfaces]
        if args.interface not in interface_names:
            self.console.print(f"[bold red]Error: Interface '{args.interface}' not found[/bold red]")
            self.console.print("[yellow]Available interfaces:[/yellow]")
            self.display_interface_table(interfaces)
            return
        
        # Restore mode
        if args.restore:
            self.animator.progress_spinner("Restoring original MAC address...")
            if self.interface_mgr.restore_mac(args.interface):
                self.animator.success_animation("MAC address restored successfully!")
            else:
                self.animator.failure_animation("Failed to restore MAC address")
            return
        
        # Determine target MAC
        if args.random:
            # Generate random MAC
            try:
                target_mac = MacAddress.generate_random(args.vendor)
                vendor = MacAddress.get_vendor(target_mac)
                self.console.print(f"[bold cyan]Generated random MAC: {target_mac}[/bold cyan]")
                self.console.print(f"[bold yellow]Vendor: {vendor}[/bold yellow]")
            except Exception as e:
                self.console.print(f"[bold red]Error generating random MAC: {e}[/bold red]")
                return
        elif args.mac:
            # Validate provided MAC
            if not MacAddress.is_valid(args.mac):
                self.console.print(f"[bold red]Error: Invalid MAC address format: {args.mac}[/bold red]")
                self.console.print("[yellow]Valid formats: 00:11:22:33:44:55, 00-11-22-33-44-55, 001122334455[/yellow]")
                return
            target_mac = MacAddress.normalize(args.mac, MacFormat(args.format))
            vendor = MacAddress.get_vendor(target_mac)
            self.console.print(f"[bold cyan]Target MAC: {target_mac}[/bold cyan]")
            self.console.print(f"[bold yellow]Vendor: {vendor}[/bold yellow]")
        else:
            self.console.print("[bold red]Error: No MAC address specified. Use -m or --random[/bold red]")
            return
        
        # Get current MAC for comparison
        current_mac = self.interface_mgr.get_current_mac(args.interface)
        if current_mac:
            current_vendor = MacAddress.get_vendor(current_mac)
            self.console.print(f"[bold green]Current MAC: {current_mac}[/bold green]")
            self.console.print(f"[bold yellow]Current Vendor: {current_vendor}[/bold yellow]")
        
        # Run speed test before change if requested
        before_test = None
        if args.test:
            self.console.print("[bold cyan]Running pre-change network test...[/bold cyan]")
            before_test = self.network_tester.run_test()
        
        # Change MAC address
        self.animator.progress_spinner("Changing MAC address...", duration=2)
        
        if self.interface_mgr.change_mac(args.interface, target_mac):
            self.animator.success_animation(f"MAC address changed successfully!\nNew: {target_mac}")
            
            # Run speed test after change if requested
            if args.test:
                self.console.print("[bold cyan]Running post-change network test...[/bold cyan]")
                after_test = self.network_tester.run_test()
                
                # Display comparison
                if before_test and after_test:
                    self.network_tester.display_results(before_test, after_test)
            
            # Display summary
            summary = f"""
┌─────────────────────────────────────────┐
│          [bold cyan]Change Summary[/bold cyan]          │
├─────────────────────────────────────────┤
│ [bold]Interface:[/bold]    {args.interface:<20} │
│ [bold]Original MAC:[/bold] {current_mac or 'Unknown':<20} │
│ [bold]New MAC:[/bold]      {target_mac:<20} │
│ [bold]Vendor:[/bold]       {vendor:<20} │
│ [bold]Time:[/bold]         {datetime.now().strftime('%H:%M:%S'):<20} │
└─────────────────────────────────────────┘
            """
            self.console.print(Panel.fit(summary, border_style="cyan", box=box.ROUNDED))
            
            # Save backup information
            self._save_backup(args.interface, current_mac, target_mac)
            
        else:
            self.animator.failure_animation("Failed to change MAC address")
    
    def _save_backup(self, interface: str, original_mac: str, new_mac: str):
        """Save backup information to file"""
        try:
            backup_data = {
                'interface': interface,
                'original_mac': original_mac,
                'new_mac': new_mac,
                'timestamp': datetime.now().isoformat(),
                'platform': platform.system()
            }
            
            with open(self.backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            self.console.print(f"[bold green]Backup saved to: {self.backup_file}[/bold green]")
            
        except Exception as e:
            self.console.print(f"[yellow]Warning: Could not save backup: {e}[/yellow]")

# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Application entry point"""
    # Check for root/admin privileges
    if os.name != 'nt' and os.geteuid() != 0:
        print("This script requires root privileges. Please run with sudo.")
        sys.exit(1)
    
    # Run application
    app = MacAnonymizerPro()
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\n[bold yellow]Operation cancelled by user[/bold yellow]")
        sys.exit(0)
    except Exception as e:
        print(f"\n[bold red]Unexpected error: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
