#!/usr/bin/env python3
import subprocess
import time
import sys
import os
import argparse
from datetime import datetime


############################################################################
############################################################################
#CLI Arguments:
# -w, --website: Website hostname (required)
# -p, --port: Port number (optional, default: 443)
# -i, --interval: Check interval in seconds (optional, default: 60)

# Basic usage (uses default port 443 and interval 60)
    #python ssl_checkV3.py -w login.emory.edu
# Custom interval, default port 443
    # python ssl_checkV3.py -w github.com -i 30
# Custom port, default interval 60
    # python ssl_checkV3.py -w example.com -p 8443
# All custom values
    # python ssl_checkV3.py -w google.com -p 443 -i 120
# Long form arguments
    # python ssl_checkV3.py --website login.emory.edu --port 443 --interval 60
# Help
    # python ssl_checkV3.py -h
############################################################################
############################################################################



def check_ssl_certificate(hostname, port=443):
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
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Monitor SSL certificates for websites',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s -w login.emory.edu
  %(prog)s -w github.com -i 30
  %(prog)s -w example.com -p 8443
  %(prog)s --website login.emory.edu --port 443 --interval 60
  %(prog)s -w google.com -p 443 -i 120
        '''
    )

    parser.add_argument('-w', '--website',
                       required=True,
                       help='Website hostname/domain name')

    parser.add_argument('-p', '--port',
                       type=int,
                       default=443,
                       help='Port number (default: 443)')

    parser.add_argument('-i', '--interval',
                       type=int,
                       default=60,
                       help='Check interval in seconds (default: 60)')

    # Parse arguments
    args = parser.parse_args()

    # Validate arguments
    if args.interval <= 0:
        print("Error: Interval must be a positive number")
        sys.exit(1)

    if args.port <= 0 or args.port > 65535:
        print("Error: Port must be between 1 and 65535")
        sys.exit(1)

    website = args.website
    port = args.port
    interval = args.interval

    # Generate log filename with timestamp
    start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Clean website name for filename (replace special chars)
    clean_website = website.replace(':', '_').replace('/', '_').replace('.', '_')
    log_filename = f"ssl_check_{clean_website}_{port}_{start_time}.log"

    # Create header message
    header = f"SSL Certificate Monitoring Started"
    header_details = f"Website: {website}\nPort: {port}\nInterval: {interval} seconds\nLog file: {log_filename}\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
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
            check_header = f"[Check #{check_count}] [{timestamp}] Checking SSL certificate for {website}:{port}..."
            print(check_header)
            write_to_file(log_filename, check_header)

            # Run SSL check
            result = check_ssl_certificate(website, port)

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
        final_msg = f"\n[{end_time}] SSL certificate monitoring for {website}:{port} stopped after {check_count} checks."
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
