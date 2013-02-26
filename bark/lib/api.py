"""
Definition of valid respones for the Bark API
"""

json_status_values = frozenset([
    'OK', 
    'UNAUTHORISED',
    'RESOURCE_ERROR',
    'BACKEND_ERROR',
    ])

UNKNOWN_STATUS = 'BACKEND_ERROR'
UNKNOWN_STATUS_ERROR = 'A malformed response was prevented by the server'


def json_response(status, payload={}):
    response = {}
    if status in json_status_values:
        response['status'] = status
        for p in payload:
            response[p] = payload[p]
    else:
        response['status'] = UNKNOWN_STATUS
        response['error_detail'] = UNKNOWN_STATUS_ERROR 
    return response

def json_error(status, error_detail):
    return json_response(status, {'error_detail': error_detail})

def json_ok(payload):
    return json_response('OK', payload)
