#! python
#
# loudark-cmd
# The command line interface to loudark
import argparse
import ipaddress
import logging
import logging.config
from settings import LOGGING
import sys


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('loudark')
logger.info("started...")


# Customer parser to provide different error message - didn't like the default
class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        print(f'\nCommand Error:\n{message}\n')
        self.print_help()
        sys.exit(1)


# ----- Validators -----
# Connection String: Ensuring the content and format of input connection string
# conforms to ip_address:port, e.g. 192.168.1.1:80
def connection_string(string):

    try:
        # Valid input = "ip_address":"port", e.g. 127.0.0.1:8000
        ip, port = string.split(':')
    except ValueError:
        # Exiting if the value is incorrect
        msg = f"Invalid format: {string}\n<ip_addr>:<port>\n192.168.1.2:80"
        raise argparse.ArgumentTypeError(msg)

    try:
        # Checking if the first part of the input is a valid IP address
        ipaddress.ip_address(ip)
    except Exception as e:
        # Exiting if the IP isn't valid
        msg = f'IP address error: {e}'
        raise argparse.ArgumentTypeError(msg)

    if 0 >= int(port) or int(port) > 65535:
        print(f'\nPort provided ({port}) out of range - must be between 0 - '
              '65535\n')
        sys.exit(1)

    return {'ip': ip, 'port': port}


# ----- Argument Parser -----
# Instantiating parser using the custome parser
parser = CustomParser(
    description="A proxy server built with Python 3",
    epilog="Example usage: python loudark.py 192.168.1.100:8000 10.24.35.23:80"
)

# Local arguments
parser.add_argument(
    "local_host:local_port",
    type=connection_string,
    help="Target IP address and port"
)

# Remote arguments
parser.add_argument(
    "remote_host:remote_port",
    type=connection_string,
    help="Destination IP address and port (what target will talk to)"
)

# Print help if there are no args provided
if len(sys.argv) == 1:
    parser.print_help()
    logger.info("No args given")
    sys.exit(1)

# Process the arguments
args = parser.parse_args()

print(f'Local: {args.target}\nRemote: {args.destination}')
