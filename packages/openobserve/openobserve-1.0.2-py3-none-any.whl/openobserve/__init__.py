import json
import os
from typing import Any
import threading

import requests
from jsonex import JsonEx
from requests.auth import HTTPBasicAuth

import openobserve.generate

username = ''
password = ''
host = 'http://127.0.0.1:5080'
stream_global = 'default'
organization_global = 'default'
ssl_verify = False
timeout = 3
additional_info = False
enable_threading = True
logs_dir = os.path.join(os.path.expanduser('~'), '.openobserve', 'logs')

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

def _send_request(data, url):
    try:
        response = requests.post(
            url=url,
            data=JsonEx.dump([data]),
            auth=HTTPBasicAuth(username, password),
            verify=ssl_verify,
            timeout=timeout
        )

        response_data = json.loads(response.content)

        if response_data['status'][0]['failed'] > 0:
            print("Failed to send data:", str(response.content))
            return False

        return response
    except Exception as e:
        print("Error during sending data:", str(e))
        return False


def send(
        job: Any = '',
        level: str = 'INFO',
        _stream: str = None,
        _organization: str = None,
        _return_data: bool = False,
        **kwargs
) -> Any:
    global host, username, password, stream_global, organization_global, ssl_verify, timeout, additional_info, enable_threading

    _stream = _stream if _stream is not None else stream_global
    _organization = _organization if _organization is not None else organization_global
    url = host + '/api/' + _organization + '/' + _stream + '/_json'
    debug = {} if additional_info is False else openobserve.generate.debug_data()

    data = {
        **{
            'job': job,
            'level': level
        },
        **debug,
        **kwargs
    }

    if _return_data:
        return data

    if enable_threading:
        thread = threading.Thread(target=_send_request, args=(data, url))
        thread.start()
        return thread
    else:
        return _send_request(data, url)
