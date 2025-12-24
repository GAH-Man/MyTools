#!/usr/bin/env python3
import subprocess
import time
import sys
import os
from datetime import datetime


# To Run:
# chmod 755 ssl_checkV2.py
# python ssl_checkV2.py (checks every 60 seconds by default)
# Or specify interval:
# python ssl_checkV2.py 30 (checks every 30 seconds)

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

def write_to_file(filename, content):
    """
    Write content to file with error handling.
    """
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(content + '\n')
    except Exception as e:
        print(f"Error writing to file: {e}")

def main():
    hostname = "login.emory.edu"
    port = 443
    interval = 60  # Check every 60 seconds by default

    # Generate log filename with timestamp
    start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"script_output/ssl_check_{hostname}_{start_time}.log"

    # Parse command line arguments
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except ValueError:
            print("Usage: python ssl_check.py [interval_seconds]")
            sys.exit(1)

    # Create header message
    header = f"SSL Certificate Monitoring Started"
    header_details = f"Target: {hostname}:{port}\nInterval: {interval} seconds\nLog file: {log_filename}\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    separator = "=" * 80

    # Display and log startup info
    startup_msg = f"{separator}\n{header}\n{separator}\n{header_details}\n{separator}"
    print(startup_msg)
    write_to_file(log_filename, startup_msg)

    print("Press Ctrl+C to stop\n")

    try:
        check_count = 0
        while True:
            check_count += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Create check header
            check_header = f"[Check #{check_count}] [{timestamp}] Checking SSL certificate..."
            print(check_header)
            write_to_file(log_filename, check_header)

            # Run SSL check
            result = check_ssl_certificate(hostname, port)

            # Display and log results
            print(result)
            write_to_file(log_filename, result)

            # Add separator
            separator_line = "-" * 80
            print(separator_line)
            write_to_file(log_filename, separator_line)

            time.sleep(interval)

    except KeyboardInterrupt:
        # Final message
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        final_msg = f"\n[{end_time}] SSL certificate monitoring stopped after {check_count} checks."
        final_separator = "=" * 80

        print(final_msg)
        print(f"Results saved to: {log_filename}")
        print(final_separator)

        write_to_file(log_filename, final_msg)
        write_to_file(log_filename, f"Results saved to: {log_filename}")
        write_to_file(log_filename, final_separator)

        sys.exit(0)

if __name__ == "__main__":
    main()
