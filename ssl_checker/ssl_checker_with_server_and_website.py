#!/usr/bin/env python3
import subprocess
import time
import sys
import os
import argparse
from datetime import datetime

######################################################
#New CLI Arguments:

#-s, --server: Web server hostname (with optional :port)
#-w, --website: Website name for identification and logging
#-i, --interval: Check interval in seconds (optional, default 60)

# python ssl_checker_with_server_and_website.py -s intidpappprd101.cc.emory.edu -w login.emory.edu -i 5
# python ssl_checker_with_server_and_website.py -s intidpappprd102.cc.emory.edu -w login.emory.edu -i 5

#Usage Examples:
# Basic usage
    #python ssl_checker_with_server_and_website.py -s login.emory.edu -w emory.edu

# With custom interval
    #python ssl_checker_with_server_and_website.py -s github.com -w github.com -i 30

# With custom port
    #python ssl_checker_with_server_and_website.py -s example.com:8443 -w example.com -i 120

# Long form arguments
    #python ssl_checker_with_server_and_website.py --server login.emory.edu --website emory.edu --interval 60

# Help
    #python ssl_checker_with_server_and_website.py -h
#######################################################

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

def parse_hostname_port(hostname_arg):
    """
    Parse hostname:port format, default port to 443 if not specified.
    """
    if ':' in hostname_arg:
        hostname, port_str = hostname_arg.rsplit(':', 1)
        try:
            port = int(port_str)
            return hostname, port
        except ValueError:
            print(f"Error: Invalid port number '{port_str}'")
            sys.exit(1)
    else:
        return hostname_arg, 443

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Monitor SSL certificates for web servers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s -s login.emory.edu -w emory.edu
  %(prog)s -s github.com -w github.com -i 30
  %(prog)s -s example.com:8443 -w example.com -i 120
  %(prog)s --server login.emory.edu --website emory.edu --interval 60
        '''
    )

    parser.add_argument('-s', '--server',
                       required=True,
                       help='Web server hostname (with optional :port, default port 443)')

    parser.add_argument('-w', '--website',
                       required=True,
                       help='Website name/domain for identification and logging')

    parser.add_argument('-i', '--interval',
                       type=int,
                       default=60,
                       help='Check interval in seconds (default: 60)')

    # Parse arguments
    args = parser.parse_args()

    # Validate interval
    if args.interval <= 0:
        print("Error: Interval must be a positive number")
        sys.exit(1)

    # Parse hostname and port
    hostname, port = parse_hostname_port(args.server)
    website = args.website
    interval = args.interval

    # Generate log filename with timestamp
    start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Clean website name for filename (replace special chars)
    clean_website = website.replace(':', '_').replace('/', '_').replace('.', '_')
    log_filename = f"ssl_check_{clean_website}_{start_time}.log"

    # Create header message
    header = f"SSL Certificate Monitoring Started"
    header_details = f"Server: {hostname}:{port}\nWebsite: {website}\nInterval: {interval} seconds\nLog file: {log_filename}\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
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
            check_header = f"[Check #{check_count}] [{timestamp}] Checking SSL certificate for {website} ({hostname}:{port})..."
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
        final_msg = f"\n[{end_time}] SSL certificate monitoring for {website} stopped after {check_count} checks."
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
