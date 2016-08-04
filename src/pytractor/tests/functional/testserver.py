# Copyright 2014 Konrad Podloucky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This is the web server that serves the angular app that we use for testing.
It is started by setup_package() in __init__.py
"""

import logging
import os
import signal
import http.server
import socketserver
import time
import multiprocessing

PORT = 8000

logger = logging.getLogger(__name__)


class TestServerHandler(http.server.SimpleHTTPRequestHandler):
    """
    The handler for the web server. It has the same functionality as the
    server for protractor's test app.
    """
    def send_text_response(self, text):
        self.send_response(200)
        self.send_header("Content-type", 'text/plain')
        self.send_header("Content-Length", len(text))
        self.end_headers()
        self.wfile.write(text.encode('utf-8'))

    def do_GET(self):
        if self.path == '/fastcall':
            self.send_text_response('done')
        elif self.path == '/slowcall':
            time.sleep(5)
            self.send_text_response('finally done')
        elif self.path == '/fastTemplateUrl':
            self.send_text_response('fast template contents')
        elif self.path == '/slowTemplateUrl':
            time.sleep(5)
            self.send_text_response('slow template contents')
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, msg_format, *args):
        """Use python logging to avoid lots of output during testing."""
        logger.info("TESTSERVER: %s - - [%s] %s\n" %
                    (self.client_address[0],
                     self.log_date_time_string(),
                     msg_format % args))


class SimpleWebServerProcess(object):
    """
    A simple webserver for serving pages for testing.
    """
    HOST = 'localhost'
    PORT = 9999
    APP_DIR = 'testapp'
    _process = None

    def run(self):
        if not self._process:
            self._process = multiprocessing.Process(target=self.start_server);
            self._process.start()
        time.sleep(1)

    def start_server(self):
        module_path = __file__
        server_path = os.path.join(os.path.dirname(module_path), self.APP_DIR)
        logger.debug('Starting webserver for path {} on'
                     ' port {}'.format(server_path, self.PORT))
        os.chdir(server_path)
        handler = TestServerHandler
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer((self.HOST, self.PORT), handler)
        httpd.serve_forever()

    def stop(self):
        if self._process:
            self._process.terminate()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # start blocking server, do not fork into the background
    process = SimpleWebServerProcess()
    process.start_server()
