# coding: utf-8
import SocketServer
from mimetools import Message
from StringIO import StringIO

# Copyright 2015 Morgan Patzelt
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


class MyWebServer(SocketServer.StreamRequestHandler):
    
    # parses the request from the client
    # returns 1 if successful, else 0
    # if 0, an error message is sent
    # if 1, a response occurs
    def parse_request():
        # get request line
        raw_requestline = self.raw_requestline
    
        # splits the raw requstline into the request line and headers
        requestline, headers_alone = request_text.split('\r\n', 1)
        # adds the headerts to a dictionary 'headers' using Message from mimetools (See Import)
        headers = Message(StringIO(headers_alone))
        
        # splits the words of the requestline
        words = requestline.split()        
        
        # Get the command
        command = words[0]
        
        # Check the version
        if words[2][:5] != 'HTTP/':
            send_error(400, "Bad Request - Version (%s)" % version)
            return 0
        else: 
            # Success
            version = words[2]
            if version == 'HTTP/1.1':
                # Test to see if request contains Host: header
                # Only needed in HTTP 1.1
                if 'Host' not in headers:
                    send_error(400, "Bad Request - No Host: header specified")
        
        # Specify path or absolute URL
        if words[1][1] == 'http://':
            # absolute path
            path = words[1][7:]
            url, path = path.split('/', 1)
            path = "/" + path
        else:
            # path
            path = words[1]
            

        # set variables
        self.path = path
        self.command = command
        self.request_version = version
        self.headers = headers
        
        #return 1 if was a sucesss, else 0
        return 1    
    
    # Handles a single HTTP request 
    def handle(self):
        # gets the request line, sets it to raw_requestline
        self.raw_requestline = self.rfile.readline()
        
        # If an error occurs during parsing
        # An error code has been sent, just exit
        if not self.parse_request(): 
            return
        
        # concatanate 'do_' with the command type to get method name (i.e. do_GET)
        mname = 'do_' + self.command
        
        # if this method has not been implemented, send 5XX error
        if not hasattr(self, mname):
            self.send_error(501, "Unsupported method (%s)" % self.command)
            return
        
        # if the method exists, call method
        method = getattr(self, mname)
        method()
        
        
    # called when an error occurs
    # matches the error code with a message
    # if a message was provided, that message is used instead
    def send_response(self, code, message=None):
        # list of responses used in this code
        responses = {
            200: ('OK', 'Request fulfilled, document follows'),
            400: ('Bad request', 'Bad request syntax or unsupported method'),
            500: ('Internal error', 'Server got itself in trouble'),
            501: ('Not implemented', 'Server does not support this operation')
            }

        shortmsg, longmsg = responses[code]
        # if a message is provided, use that instead
        if not message:
            message = shortmsg
        
        #call print_error_msg to print output for client
        print_msg(code, message, longmsg)
    
    # prints the error message if an error message is sent
    # called by send error
    def print_msg(self, code, message, longmsg):
        # creates the html output to tell the client the error
        htmlres = "<html><body>\r\n<h2>" + message + "</h2>\r\n" + longmsg + "</body></html>"
        # counts the length of the html output
        length = len(htmlres)
        
        # writes the message that goes above the html output
        self.wfile.write(self.version + " " + code + " " + message)
        self.wfile.write("Content-Type: text/html")
        self.wfile.write("Content-Length: " + length)
        self.wfile.write("\r\n")
        self.wfile.write(htmlres)
    
    # returns the date in the proper format for GMT
    def get_date():
        currTime = time.time()
        year, mm, dd, h, m, s, wday, yday, isdst = time.gmtime(currTime)
        
        # converts the month from number format to 3-letter abbreviation
        month = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        # converts the weekday from number format to 3-letter abbreviation
        day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        mm = month[mm]
        wday = day[wday]
        
        # creates the string with the date in the correct format
        date = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (wday, dd, mm, year, h, m, s)
        
        # string
        return date
    
    # sends a MIME header
    def send_header(self, header, value):
        # no headers in HTTP/0.9
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("%s: %s\r\n" % (header, value))
    
    # sends the blank line that indicates no more MIME headers
    def end_headers(self):
        # no headers in HTTP/0.9
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("\r\n")
                
        
        
        
        
    
            
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


protocol_version = "HTTP/1.1" # MIGHT HAVE TO CHANGE THIS




        