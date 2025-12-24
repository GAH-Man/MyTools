#!/usr/bin/env python3
import subprocess
import time
import sys
from datetime import datetime



# To Run:
# chmod 755 ssl_check.py
# python ssl_check.py (checks every 60 seconds by default)
# Or specify interval:
# python ssl_check.py 30 (checks every 30 seconds)

def check_ssl_certificate(hostname="login.emory.edu", port=443):
    """
    Check SSL certificate information for a given hostname and port.
    """
    cmd = [
        "bash", "-c",
        f"echo | openssl s_client -connect {hostname}:{port} -servername {hostname} 2>/dev/null | "
        f"openssl x509 -noout -subject -issuer -dates -ext subjectAltName"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    hostname = "login.emory.edu"
    port = 443
    interval = 60  # Check every 60 seconds by default


    # Parse command line arguments
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except ValueError:
            print("Usage: python ssl_check.py [interval_seconds]")
            sys.exit(1)

    print(f"Starting SSL certificate monitoring for {hostname}:{port}")
    print(f"Check interval: {interval} seconds")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Checking SSL certificate...")

            result = check_ssl_certificate(hostname, port)
            print(result)
            print("-" * 80)

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nStopping SSL certificate monitoring...")
        sys.exit(0)

if __name__ == "__main__":
    main()
