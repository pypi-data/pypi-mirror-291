import sys
import traceback
import json
import io

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from flask import Flask

from werkzeug.wrappers.request import Request


def make_environ(event):
    environ = {}
    # print('event', event)
    # key might be there but set to None
    headers = event.get('headers', {}) or {}
    for hdr_name, hdr_value in headers.items():
        hdr_name = hdr_name.replace('-', '_').upper()
        if hdr_name in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
            environ[hdr_name] = hdr_value
            continue

        http_hdr_name = 'HTTP_{}'.format(hdr_name)
        environ[http_hdr_name] = hdr_value

    qs = event['queryStringParameters']

    environ['REQUEST_METHOD'] = event['httpMethod']

    environ['PATH_INFO'] = event['path']

    environ['QUERY_STRING'] = urlencode(qs) if qs else ''
    environ['REMOTE_ADDR'] = event['requestContext']['identity']['sourceIp']
    environ['HOST'] = '{}:{}'.format(
        environ.get('HTTP_HOST', ''),
        environ.get('HTTP_X_FORWARDED_PORT', ''),
    )
    environ['SCRIPT_NAME'] = ''
    environ['SERVER_NAME'] = 'SERVER_NAME'

    try:
        environ['SERVER_PORT'] = environ['HTTP_X_FORWARDED_PORT']
    except:
        environ['SERVER_PORT'] = '80'

    environ['SERVER_PROTOCOL'] = 'HTTP/1.1'

    environ['CONTENT_LENGTH'] = str(
        len(event['body']) if event['body'] else ''
    )

    try:
        environ['wsgi.url_scheme'] = environ['HTTP_X_FORWARDED_PROTO']
    except:
        environ['wsgi.url_scheme'] = 'https'

    environ['wsgi.input'] = io.BytesIO((event['body'] or '').encode())
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.multithread'] = False
    environ['wsgi.run_once'] = True
    environ['wsgi.multiprocess'] = False
    environ['AWS_STAGE_NAME'] = event['requestContext']['stage']
    environ['apiId'] = event['requestContext']['apiId']

    Request(environ)

    return environ


class LambdaResponse(object):

    def __init__(self):
        self.status = None
        self.response_headers = None

    def start_response(self, status, response_headers, exc_info=None):
        self.status = int(status[:3])
        self.response_headers = dict(response_headers)


class FlaskLambda(Flask):

    def __call__(self, event, context):
        try:
            if 'httpMethod' not in event:
                # print('call as flask app')
                # In this "context" `event` is `environ` and
                # `context` is `start_response`, meaning the request didn't
                # occur via API Gateway and Lambda
                return super(FlaskLambda, self).__call__(event, context)

            # print('call as aws lambda')
            response = LambdaResponse()

            body = next(self.wsgi_app(
                make_environ(event),
                response.start_response
            ))

            return {
                'statusCode': response.status,
                'headers': response.response_headers,
                'body': body.decode('utf-8')
            }

        except Exception as e:
            # print('unexpected error', e)
            trace = traceback.format_exc()
            trace = trace.replace('\"', "'").split("\n")
            return {
                'statusCode': 500,
                'headers': {},
                'body': json.dumps(trace)
            }
