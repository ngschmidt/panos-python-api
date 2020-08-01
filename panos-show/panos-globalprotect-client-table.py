#!/usr/bin/python3
# PAN-OS API GlobalProtect Collector
# Nicholas Schmidt
# 31 Jul 2020

# API Processing imports
import requests
import json

# XML has vulnerabilities, use DefusedXML libraries instead to offload security mitigations to the project
# https://pypi.org/project/defusedxml/#defusedxml
from defusedxml import ElementTree
# We like JSON, as We'd rather have only one language for data processing. Let's try xmltodict
import xmltodict

# Command line parsing imports
import argparse

# Command line validating imports
from django.core.validators import URLValidator

# Object Definitions

# Functions

# Do API GET
def do_api_get_unpw(do_api_unpw_user, do_api_unpw_password, do_api_unpw_url, do_api_certvalidation):
    # Perform API Processing - conditional basic authentication
    try:
        do_api_unpw_headers = {'content-type': 'application/xml'}
        do_api_unpw_r = requests.get(do_api_unpw_url, headers=do_api_unpw_headers, verify=do_api_certvalidation)
        # We'll be discarding the actual `Response` object after this, but we do want to get HTTP status for erro handling
        response_code = do_api_unpw_r.status_code
        do_api_unpw_r.raise_for_status()  # trigger an exception before trying to convert or read data. This should allow us to get good error info
        return do_api_unpw_r.text  # if HTTP status is good, i.e. a 100/200 status code, we're going to convert the response into a json dict
    except requests.Timeout:
        print('API Connection timeout!')
    except requests.ConnectionError as connection_error:
        print(connection_error)
    except requests.HTTPError:
        if httperrors.get(response_code):
            print('HTTP Status Error ' + str(response_code) + ' ' + httperrors.get(response_code)[max(min(args.verbosity, 1), 0)])
            exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
        else:
            print('Unhandled HTTP Error ' + str(response_code) + '!')
            exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
    except requests.RequestException as requests_exception:
        print(requests_exception)
    except:
        print('Unhandled Requests exception!')
        exit()


# Do API GET with Auth Key
# Send a xml payload via the requests API
def do_api_get_key(do_api_post_auth_key, do_api_post_url, do_api_post_payload, do_api_certvalidation):
    # Perform API Processing - conditional basic authentication
    try:
        do_api_post_headers = {'content-type': 'application/xml'}
        print(do_api_post_url + do_api_post_payload + '&key=' + do_api_post_auth_key)
        do_api_post_r = requests.get(do_api_post_url + do_api_post_payload + '&key=' + do_api_post_auth_key, headers=do_api_post_headers, verify=do_api_certvalidation)
        # We'll be discarding the actual `Response` object after this, but we do want to get HTTP status for erro handling
        response_code = do_api_post_r.status_code
        do_api_post_r.raise_for_status()  # trigger an exception before trying to convert or read data. This should allow us to get good error info
        return do_api_post_r.text  # if HTTP status is good, i.e. a 100/200 status code, we're going to convert the response into a json dict
    except requests.Timeout:
        print('API Connection timeout!')
    except requests.ConnectionError as connection_error:
        print(connection_error)
    except requests.HTTPError:
        if httperrors.get(response_code):
            print('HTTP Status Error ' + str(response_code) + ' ' + httperrors.get(response_code)[max(min(args.verbosity, 1), 0)])
            exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
        else:
            print('Unhandled HTTP Error ' + str(response_code) + '!')
            exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
    except requests.RequestException as requests_exception:
        print(requests_exception)
    except:
        print('Unhandled Requests exception!')
        exit()


# Do API POST with Auth Key
# Send a xml payload via the requests API
def do_api_post_key(do_api_post_auth_key, do_api_post_url, do_api_post_payload, do_api_certvalidation):
    # Perform API Processing - conditional basic authentication
    try:
        do_api_post_headers = {'content-type': 'application/xml'}
        do_api_post_r = requests.post(do_api_post_url + do_api_post_payload + '&key=' + do_api_post_auth_key, headers=do_api_post_headers, verify=do_api_certvalidation)
        # We'll be discarding the actual `Response` object after this, but we do want to get HTTP status for erro handling
        response_code = do_api_post_r.status_code
        do_api_post_r.raise_for_status()  # trigger an exception before trying to convert or read data. This should allow us to get good error info
        return do_api_post_r.text  # if HTTP status is good, i.e. a 100/200 status code, we're going to convert the response into a json dict
    except requests.Timeout:
        print('API Connection timeout!')
    except requests.ConnectionError as connection_error:
        print(connection_error)
    except requests.HTTPError:
        if httperrors.get(response_code):
            print('HTTP Status Error ' + str(response_code) + ' ' + httperrors.get(response_code)[max(min(args.verbosity, 1), 0)])
            exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
        else:
            print('Unhandled HTTP Error ' + str(response_code) + '!')
            exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
    except requests.RequestException as requests_exception:
        print(requests_exception)
    except:
        print('Unhandled Requests exception!')
        exit()


# DO API GET for API Key
def do_api_get_auth_key(do_api_get_auth_key_user, do_api_get_auth_key_password, do_api_get_auth_key_url, do_api_get_auth_key_certvalidation):
    try:
        api_response = xmltodict.parse(do_api_get_unpw(do_api_get_auth_key_user, do_api_get_auth_key_password, 
                                        do_api_get_auth_key_url + '/?type=keygen&user=' + do_api_get_auth_key_user + '&password=' + do_api_get_auth_key_password,
                                        do_api_get_auth_key_certvalidation), encoding='utf-8')
    except:
        print('An error was encountered while parsing XML API Response!')
        exit()
    return api_response['response']['result']['key']


# Do an API Op Command
def do_api_get_opcmd_key(do_api_opcmd_auth_key, do_api_opcmd_url, do_api_opcmd_payload, do_api_certvalidation):
    return do_api_get_key(do_api_opcmd_auth_key, do_api_opcmd_url, '/?type=op&cmd=' + do_api_opcmd_payload, do_api_certvalidation)


# Open an xml payload file
def get_xml_from_file(get_xml_from_file_name):
    # Attempt to load a json file, and lint it
    try:
        with open(get_xml_from_file_name) as file_contents_string:
            return file_contents_string.read()
    except ValueError as err:
        print('Python thinks you have a xml formatting issue. Please run your payload input through a xml linter.')
        print(err)
        exit()
    except IOError as err:
        print('A File I/O error has occurred. Please check your file path!')
        print(err)
        exit()
    except:
        print('An unexpected error has occurred!')
        exit()


# Validate XML from string
def validate_xml_from_string(validate_xml_from_string_string):
    # Test an import into dict
    try:
        return_dict_from_xml = xmltodict.parse(validate_xml_from_string_string, encoding='utf-8')
    except:
        print('Invalid XML found! Exiting...')
        exit()
    return return_dict_from_xml


# References

# Set HTTP Error + Verbosity table. Due to the use of max(min()), verbosity count becomes a numerical range that caps off and prevents array issues
# Credit where due - https://gist.github.com/bl4de/3086cf26081110383631 by bl4de
# 1-99 Errors are PAN-OS specific.
# More here: https://docs.paloaltonetworks.com/pan-os/9-0/pan-os-panorama-api/get-started-with-the-pan-os-xml-api/pan-os-xml-api-error-codes.html
httperrors = {
    1:   ('Unknown Command', 'The specific config or operational command is not recognized.'),
    2:   ('Internal Error', 'Check with technical support when seeing these errors.'),
    3:   ('Internal Error', 'Check with technical support when seeing these errors.'),
    4:   ('Internal Error', 'Check with technical support when seeing these errors.'),
    5:   ('Internal Error', 'Check with technical support when seeing these errors.'),
    6:   ('Bad Xpath', 'The xpath specified in one or more attributes of the command is invalid. Check the API browser for proper xpath values.'),
    7:   ('Object Not Present', 'Object specified by the xpath is not present. For example, entry[@name="value"] where no object with name "value" is present.'),
    8:   ('Object Not Unique', 'For commands that operate on a single object, the specified object is not unique.'),
    10:  ('Reference count not zero', 'Object cannot be deleted as there are other objects that refer to it. For example, address object still in use in policy.'),
    11:  ('Internal Error', 'Check with technical support when seeing these errors.'),
    12:  ('Invalid Object', 'Xpath or element values provided are not complete.'),
    14:  ('Operation Not Possible', 'Operation is allowed but not possible in this case. For example, moving a rule up one position when it is already at the top.'),
    15:  ('Operation Denied', 'Operation is allowed. For example, Admin not allowed to delete own account, Running a command that is not allowed on a passive device.'),
    16:  ('Unauthorized', 'The API role does not have access rights to run this query.'),
    17:  ('Invalid Command', 'Invalid command or parameters.'),
    18:  ('Malformed command', 'The XML is malformed'),
    19:  ('Success', 'Command Completed Successfully'),
    20:  ('Success', 'Command Completed Successfully'),
    21:  ('Internal Error', 'Check with technical support when seeing these errors.'),
    22:  ('Session timed out', 'The session for this query timed out'),

    100: ('Continue', 'Request received, please continue'),
    101: ('Switching Protocols',
          'Switching to new protocol; obey Upgrade header'),

    200: ('OK', 'Request fulfilled, document follows'),
    201: ('Created', 'Document created, URL follows'),
    202: ('Accepted',
          'Request accepted, processing continues off-line'),
    203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
    204: ('No Content', 'Request fulfilled, nothing follows'),
    205: ('Reset Content', 'Clear input form for further input.'),
    206: ('Partial Content', 'Partial content follows.'),

    300: ('Multiple Choices',
          'Object has several resources -- see URI list'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    302: ('Found', 'Object moved temporarily -- see URI list'),
    303: ('See Other', 'Object moved -- see Method and URL list'),
    304: ('Not Modified',
          'Document has not changed since given time'),
    305: ('Use Proxy',
          'You must use proxy specified in Location to access this '
          'resource.'),
    307: ('Temporary Redirect',
          'Object moved temporarily -- see URI list'),

    400: ('Bad Request',
          'Bad request syntax or unsupported method'),
    401: ('Unauthorized',
          'No permission -- see authorization schemes'),
    402: ('Payment Required',
          'No payment -- see charging schemes'),
    403: ('Forbidden',
          'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
          'Specified method is invalid for this server.'),
    406: ('Not Acceptable', 'URI not available in preferred format.'),
    407: ('Proxy Authentication Required', 'You must authenticate with '
          'this proxy before proceeding.'),
    408: ('Request Timeout', 'Request timed out; try again later.'),
    409: ('Conflict', 'Request conflict.'),
    410: ('Gone',
          'URI no longer exists and has been permanently removed.'),
    411: ('Length Required', 'Client must specify Content-Length.'),
    412: ('Precondition Failed', 'Precondition in headers is false.'),
    413: ('Request Entity Too Large', 'Entity is too large.'),
    414: ('Request-URI Too Long', 'URI is too long.'),
    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
    416: ('Requested Range Not Satisfiable',
          'Cannot satisfy request range.'),
    417: ('Expectation Failed',
          'Expect condition could not be satisfied.'),

    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented',
          'Server does not support this operation'),
    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
    503: ('Service Unavailable',
          'The server cannot process the request due to a high load'),
    504: ('Gateway Timeout',
          'The gateway server did not receive a timely response'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
}

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

# Ensure that API Endpoint is a valid one
validate = URLValidator()
try:
    validate(args.api_endpoint)
except:
    print('Invalid URL. Please try a valid URL. Example: "https://10.0.0.0/api"')
    exit()

# Let's try getting an API key first
try:
    session_auth_key = do_api_get_auth_key(args.u, args.p, args.api_endpoint, args.k)
except:
    print('Encountered an unhandled issue getting authorization key!')
    exit()
print('Generated PAN-OS API Key!')

# Let's try parsing a payload
xml_payload_globalprotect_summary = get_xml_from_file('globalprotect_summary.xml')
print(validate_xml_from_string(xml_payload_globalprotect_summary) + 'Read from file!')
xml_payload_globalprotect_summary_detail = get_xml_from_file('globalprotect_summary_detail.xml')
print(validate_xml_from_string(xml_payload_globalprotect_summary) + ' Read from file!') 
# Let's try deploying the payload!
globalprotect_summary = validate_xml_from_string(do_api_get_opcmd_key(session_auth_key, args.api_endpoint, xml_payload_globalprotect_summary, args.k))
#globalprotect_summary_detail = validate_xml_from_string(do_api_get_opcmd_key(session_auth_key, args.api_endpoint, xml_payload_globalprotect_summary_detail, args.k))

# Begin Processing API Data - Parsing Route Tables
# Debugging shouldn't require code changes, let's use our verbosity switches
print(globalprotect_summary)
#print(globalprotect_summary_detail)