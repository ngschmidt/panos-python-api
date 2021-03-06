#!/usr/bin/python3
# PAN-OS API GlobalProtect Collector
# Nicholas Schmidt
# 31 Jul 2020

# API Processing imports
import requests

# Let's try xmltodict
import xmltodict

# Command line validating imports
from django.core.validators import URLValidator

# Object Definitions

# Class Definitions
# They're not here to stay, just passing through
class IronStrataReliquary:

    # Initial Variable Settings
    #
    strata_verbosity = 0
    strata_certvalidation = True
    strata_username = ''
    strata_password = ''
    strata_authkey = ''
    strata_endpoint = ''

    # And construct with specific endpoint
    def __init__(self, input_verbosity, input_certvalidation, input_username, input_password, input_endpoint):
        # Set variables from constructor
        self.strata_verbosity = input_verbosity
        self.strata_certvalidation = input_certvalidation
        self.strata_username = input_username
        self.strata_password = input_password
        self.strata_endpoint = input_endpoint

        # Once variables are set, develop a relationship with said endpoint
        # Ensure that API Endpoint is a valid one
        validate = URLValidator()
        try:
            validate(self.strata_endpoint)
        except:
            print('E0001: Invalid URL. Please try a valid URL. Example: "https://10.0.0.0/api"')
            exit()

        # If URL is valid, try to establish session key
        try:
            api_response = xmltodict.parse(self.do_api_get(self.strata_endpoint + '/?type=keygen&user=' +
                                           self.strata_username + '&password=' + self.strata_password), encoding='utf-8')
        except:
            print('E1001: An error was encountered while parsing XML API Response!')
            exit()
        self.strata_authkey = api_response['response']['result']['key']

    # Variable Declarations
    #
    # XML Queries
    #
    # List of all saved queries.
    #
    # Naming Convention: <module>_<name>_<first tested version>
    strata_bibliotheca = {
        'globalprotect_summary_v9':         ('<show><global-protect-gateway><summary><all/></summary></global-protect-gateway></show>',
                                             '<response status=\"success\"><result>'),
        'globalprotect_summary_detail_v9':  ('<show><global-protect-gateway><summary><detail/></summary></global-protect-gateway></show>',
                                             '<response status=\"success\"><result>'),
        'routing_route_v9':                  ('<show><routing><route/></routing></show>',
                                              '<response status=\"success\"><result>'),
        'routing_summary_v9':                ('<show><routing><summary/></routing></show>',
                                              '<response status=\"success\"><result>'),
        'routing_capacity_v9':               ('<show><routing><resource/></routing></show>',
                                              '<response status=\"success\"><result>'),
        'bgp_summary_v9':                    ('<show><routing><protocol><bgp><summary/></bgp></protocol></routing></show>',
                                              '<response status=\"success\"><result>')
    }
    #
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
        7:   ('Object Not Present',
              'Object specified by the xpath is not present. For example, entry[@name="value"] where no object with name "value" is present.'),
        8:   ('Object Not Unique', 'For commands that operate on a single object, the specified object is not unique.'),
        10:  ('Reference count not zero',
              'Object cannot be deleted as there are other objects that refer to it. For example, address object still in use in policy.'),
        11:  ('Internal Error', 'Check with technical support when seeing these errors.'),
        12:  ('Invalid Object', 'Xpath or element values provided are not complete.'),
        14:  ('Operation Not Possible',
              'Operation is allowed but not possible in this case. For example, moving a rule up one position when it is already at the top.'),
        15:  ('Operation Denied',
              'Operation is allowed. For example, Admin not allowed to delete own account, Running a command that is not allowed on a passive device.'),
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
    # Functions

    # Do API GET, using basic credentials
    def do_api_get(self, do_api_unpw_url):
        # Perform API Processing - conditional basic authentication
        try:
            do_api_get_headers = {'content-type': 'application/xml'}
            do_api_get_r = requests.get(do_api_unpw_url, headers=do_api_get_headers, verify=self.strata_certvalidation)
            # We'll be discarding the actual `Response` object after this, but we do want to get HTTP status for erro handling
            response_code = do_api_get_r.status_code
            do_api_get_r.raise_for_status()  # trigger an exception before trying to convert or read data. This should allow us to get good error info
            return do_api_get_r.text  # if HTTP status is good, i.e. a 100/200 status code, we're going to convert the response into a json dict
        except requests.Timeout:
            print('E1000: API Connection timeout!')
        except requests.ConnectionError as connection_error:
            print(connection_error)
        except requests.HTTPError:
            if self.get_http_error_code(response_code):
                print('EA' + str(response_code) + ': HTTP Status Error ' + str(response_code) + ' ' + self.get_http_error_code(response_code))
                exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
            else:
                print('EA999: Unhandled HTTP Error ' + str(response_code) + '!')
                exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
        except requests.RequestException as requests_exception:
            print(requests_exception)
        except:
            print('E1002: Unhandled Requests exception!')
            exit()

    # Do API GET with Auth Key
    # Send a xml payload via the requests API
    def do_api_get_key(self, do_api_post_url, do_api_post_payload):
        # Perform API Processing - conditional basic authentication
        try:
            do_api_post_headers = {'content-type': 'application/xml'}
            if(self.strata_verbosity > 0):
                print(do_api_post_url + do_api_post_payload + '&key=' + self.strata_authkey)
            do_api_post_r = requests.get(do_api_post_url + do_api_post_payload + '&key=' + self.strata_authkey,
                                         headers=do_api_post_headers, verify=self.strata_certvalidation)
            # We'll be discarding the actual `Response` object after this, but we do want to get HTTP status for erro handling
            response_code = do_api_post_r.status_code
            do_api_post_r.raise_for_status()  # trigger an exception before trying to convert or read data. This should allow us to get good error info
            return do_api_post_r.text  # if HTTP status is good, i.e. a 100/200 status code, we're going to convert the response into a json dict
        except requests.Timeout:
            print('E1000: API Connection timeout!')
        except requests.ConnectionError as connection_error:
            print(connection_error)
        except requests.HTTPError:
            if self.get_http_error_code(response_code):
                print('EA' + str(response_code) + ': HTTP Status Error ' + str(response_code) + ' ' + self.get_http_error_code(response_code))
                exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
            else:
                print('EA999: Unhandled HTTP Error ' + str(response_code) + '!')
                exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
        except requests.RequestException as requests_exception:
            print(requests_exception)
        except:
            print('E1002: Unhandled Requests exception!')
            exit()

    # Do API POST with Auth Key
    # Send a xml payload via the requests API
    def do_api_post_key(self, do_api_post_url, do_api_post_payload):
        # Perform API Processing - conditional basic authentication
        try:
            do_api_post_headers = {'content-type': 'application/xml'}
            do_api_post_r = requests.post(do_api_post_url + do_api_post_payload + '&key=' + self.strata_authkey,
                                          headers=do_api_post_headers, verify=self.strata_certvalidation)
            # We'll be discarding the actual `Response` object after this, but we do want to get HTTP status for erro handling
            response_code = do_api_post_r.status_code
            do_api_post_r.raise_for_status()  # trigger an exception before trying to convert or read data. This should allow us to get good error info
            return do_api_post_r.text  # if HTTP status is good, i.e. a 100/200 status code, we're going to convert the response into a json dict
        except requests.Timeout:
            print('E1000: API Connection timeout!')
        except requests.ConnectionError as connection_error:
            print(connection_error)
        except requests.HTTPError:
            if self.get_http_error_code(response_code):
                print('EA' + str(response_code) + ': HTTP Status Error ' + str(response_code) + ' ' + self.get_http_error_code(response_code))
                exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
            else:
                print('EA999: Unhandled HTTP Error ' + str(response_code) + '!')
                exit()  # interpet the error, then close out so we don't have to put all the rest of our code in an except statement
        except requests.RequestException as requests_exception:
            print(requests_exception)
        except:
            print('E1002: Unhandled Requests exception!')
            exit()

    # DO API GET for API Key
    def do_api_get_auth_key(self):
        try:
            api_response = xmltodict.parse(self.do_api_get(self.strata_endpoint + '/?type=keygen&user=' +
                                           self.strata_username + '&password=' + self.strata_password), encoding='utf-8')
        except:
            print('E2001: An error was encountered while parsing XML API Response!')
            exit()
        self.strata_authkey = api_response['response']['result']['key']
        return api_response['response']['result']['key']

    # Do an API Op Command
    def do_api_get_opcmd_key(self, do_api_opcmd_payload):
        return self.do_api_get_key(self.strata_endpoint, '/?type=op&cmd=' + do_api_opcmd_payload)

    # Get HTTP Error Code
    def get_http_error_code(self, get_http_error_code_code):
        return self.httperrors.get(get_http_error_code_code)[max(min(self.strata_verbosity, 1), 0)]

    # Validate XML from string
    def validate_xml_from_string(self, validate_xml_from_string_string):
        # Test an import into dict
        try:
            return_dict_from_xml = xmltodict.parse(validate_xml_from_string_string, encoding='utf-8')
        except:
            print('E2001: Invalid XML found! Exiting...')
            exit()
        return return_dict_from_xml

    # Validate API responses
    def validate_opcmd_response(self, validate_opcmd_response_name, validate_opcmd_response_response):
        return self.strata_bibliotheca[validate_opcmd_response_name][1] in validate_opcmd_response_response
