#  coding: utf-8
import SocketServer

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

WHITE_LIST= ["html", "css"]

class MyWebServer(SocketServer.BaseRequestHandler):
    def get_resp(self, req):
        # response headers (taken 2016/01/07)
        # see http://blog.scphillips.com/posts/2012/12/a-simple-python-webserver/
        resp_ok = "HTTP/1.1 200 OK\nContent-Type: text/{}\n\n"
        resp_err = "HTTP/1.1 404 Not Found\r\n"

        # get file request from string
        print req + "\n"
        result = req.split(" ")[1]

        # handle '/' request
        if result[-1] == "/":
            result += "index.html"

        # if file is servable, return the content with the headers
        if result.split(".")[-1] in WHITE_LIST:
            try:
                return resp_ok.format(result.split(".")[-1]) + open("www"+result).read()
            except:
                return resp_err
        else:
            return resp_err

    def handle(self):
        self.req = self.request.recv(1024).strip()
        self.resp = self.get_resp(self.req)
        self.request.sendall(self.resp)
        self.request.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    # for example headers
