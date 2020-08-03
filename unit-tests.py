#!/usr/bin/python3
# PAN-OS API GlobalProtect Collector
# Nicholas Schmidt
# 31 Jul 2020

# Command line parsing imports
import argparse

# Import IronStrataReliquary
from IronStrataReliquary import IronStrataReliquary

# Arguments Parsing
parser = argparse.ArgumentParser(description='Fetch via API')
parser.add_argument('-v', '--verbosity', action='count', default=0, help='Output Verbosity')
parser.add_argument('-k', action='store_false', default=True, help='Ignore Certificate Errors')
subparsers = parser.add_subparsers(help='Use Basic or Key Authentication')
unpw = subparsers.add_parser('basic', help='Use Basic Authentication')
unpw.add_argument('-u', help='Username')
unpw.add_argument('-p', help='Password')
cert = subparsers.add_parser('key', help='Use Key Authentication')
cert.add_argument('--auth_key', help='Authentication Key')
parser.add_argument('api_endpoint', help='The API Endpoint to target with this API call. PAN-OS XML API is at https://<ip>/api')
args = parser.parse_args()

strata_interface = IronStrataReliquary(args.verbosity, args.k, args.u, args.p, args.api_endpoint)

# Let's try deploying the payload!
for i in strata_interface.strata_bibliotheca:
    res = strata_interface.do_api_get_opcmd_key(strata_interface.strata_bibliotheca[i][0])
    print(str(i) + ' Result: ' + str(strata_interface.validate_opcmd_response(i, res)))
    if(strata_interface.strata_verbosity > 0):
        print(res)
