#!/usr/bin/env python3
import socket
import sys
import time
import random
from datetime import datetime

WORDS = [
    "error", "login", "logout", "packet", "firewall", "accepted",
    "denied", "restart", "systemd", "network", "warning", "info",
    "update", "reboot", "session", "kernel", "database", "timeout"
]

def random_message(length=6):
    """Generate a random message with a few random words."""
    return " ".join(random.choices(WORDS, k=length))

def send_syslog(host, port, message, facility=16, severity=6):
    """
    Send a syslog message via UDP
    facility: 16 = local0, severity: 6 = info
    Priority = facility * 8 + severity
    """
    priority = facility * 8 + severity
    timestamp = datetime.now().strftime('%b %d %H:%M:%S')
    hostname = socket.gethostname()
    
    # Format: <priority>timestamp hostname tag: message
    syslog_msg = f"<{priority}>{timestamp} {hostname} testapp: {message}"
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(syslog_msg.encode('utf-8'), (host, port))
        print(f"Sent to {host}:{port}: {syslog_msg}")
    except Exception as e:
        print(f"Error sending to {host}:{port}: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 send_syslog.py <host> <port>")
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