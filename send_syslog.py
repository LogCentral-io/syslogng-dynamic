#!/usr/bin/env python3
import socket
import sys
import time
import random
import ipaddress
from datetime import datetime

WORDS = [
    "error", "login", "logout", "packet", "firewall", "accepted",
    "denied", "restart", "systemd", "network", "warning", "info",
    "update", "reboot", "session", "kernel", "database", "timeout"
]

def get_address_family(host):
    """
    Determine the address family (IPv4 or IPv6) for a given host.
    Returns socket.AF_INET for IPv4 or socket.AF_INET6 for IPv6.
    """
    try:
        # First, try to parse as an IP address
        ip = ipaddress.ip_address(host)
        if isinstance(ip, ipaddress.IPv4Address):
            return socket.AF_INET
        elif isinstance(ip, ipaddress.IPv6Address):
            return socket.AF_INET6
    except ValueError:
        # Not a valid IP address, try to resolve hostname
        try:
            # Use getaddrinfo to resolve hostname and determine address family
            addrinfo = socket.getaddrinfo(host, None, socket.AF_UNSPEC, socket.SOCK_DGRAM)
            if addrinfo:
                return addrinfo[0][0]  # Return the address family of first result
        except socket.gaierror:
            pass
    
    # Default to IPv4 if unable to determine
    return socket.AF_INET

def random_message(length=6):
    """Generate a random message with a few random words."""
    return " ".join(random.choices(WORDS, k=length))

def send_syslog(host, port, message, facility=16, severity=6):
    """
    Send a syslog message via UDP (supports both IPv4 and IPv6)
    facility: 16 = local0, severity: 6 = info
    Priority = facility * 8 + severity
    """
    priority = facility * 8 + severity
    timestamp = datetime.now().strftime('%b %d %H:%M:%S')
    hostname = socket.gethostname()
    
    # Format: <priority>timestamp hostname tag: message
    syslog_msg = f"<{priority}>{timestamp} {hostname} testapp: {message}"
    
    # Determine address family (IPv4 or IPv6)
    addr_family = get_address_family(host)
    
    sock = socket.socket(addr_family, socket.SOCK_DGRAM)
    try:
        sock.sendto(syslog_msg.encode('utf-8'), (host, port))
        family_name = "IPv6" if addr_family == socket.AF_INET6 else "IPv4"
        print(f"Sent to {host}:{port} ({family_name}): {syslog_msg}")
    except Exception as e:
        print(f"Error sending to {host}:{port}: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 send_syslog.py <host> <port>")
        print("  host: IPv4 address, IPv6 address, or hostname")
        print("  port: UDP port number")
        print("Examples:")
        print("  python3 send_syslog.py 192.168.1.100 514")
        print("  python3 send_syslog.py ::1 514")
        print("  python3 send_syslog.py 2001:db8::1 514")
        print("  python3 send_syslog.py localhost 514")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])

    try:
        while True:
            message = random_message()
            send_syslog(host, port, message)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nStopped by user.")