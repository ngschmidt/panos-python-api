#!/usr/bin/python3
# PAN-OS API GlobalProtect Collector
# Nicholas Schmidt
# 31 Jul 2020

# API Processing imports
import requests
import json

# We like JSON, as We'd rather have only one language for data processing. Let's try xmltodict
import xmltodict

# Command line parsing imports
import argparse

# Command line validating imports
from django.core.validators import URLValidator

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
unit_tests = {
    1:  ('GlobalProtect Summary', strata_interface.query_get_globalprotect_summary_v9),
    2:  ('GlobalProtect Summary Detail', strata_interface.query_get_globalprotect_summary_detail_v9)
}
for i in unit_tests:
    res = strata_interface.do_api_get_opcmd_key(unit_tests[i][1])
    print(unit_tests[i][0] + ' Result: ' + str(strata_interface.validate_opcmd_response(res)))
    if(strata_interface.strata_verbosity > 0):
        print(res)