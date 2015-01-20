# coding: utf-8
import SocketServer
import sys
import time
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
    
    __version__ = 1.0
    
    # parses the request from the client
    # returns 1 if successful, else 0
    # if 0, an error message is sent
    # if 1, a response occurs
    def parse_request(self):
        # get request line
        raw_requestline = self.data
    
        # splits the raw requstline into the request line and headers
        requestline, headers_alone = raw_requestline.split('\r\n', 1)
        # adds the headerts to a dictionary 'headers' using Message from mimetools (See Import)
        headers = Message(StringIO(headers_alone))
        
        # splits the words of the requestline
        words = requestline.split()        
        
        # Get the command
        command = words[0]
        
        # Check the version
        version = words[2]
        self.version = version
        if words[2][:5] != 'HTTP/':
            self.send_error(400, "Bad Request - Version (%s)" % version)
        #else: 
            # Success
            #if version == 'HTTP/1.1':
                # Test to see if request contains Host: header
                # Only needed in HTTP 1.1
                #if 'Host' not in headers:
                    #self.send_error(400, "Bad Request - No Host: header specified")
                
        # Specify path or absolute URL
        if words[1][:7] == 'http://':
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
        self.headers = headers
        
        #return 1 if was a sucesss, else 0
        return 1    
    
    def do_GET(self):
        
        try:
            # if the request is in CSS
            if self.path.contains(".css"):
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-Type', 'text/css')
                self.send_header('Content-length', 0)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            # if the request is in HTML
            if self.path.contains(".html"):   
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-Type', contenttype)
                self.send_header('Content-length', 0)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
        
        
        except:
            self.send_error(404, "File Not Found: %s" % self.path)        
    
    # Handles a single HTTP request 
    def handle(self):
        # gets the request line, sets it to raw_requestline
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        print self.request.sendall("OK")
        
        # If an error occurs during parsing
        # An error code has been sent, just exit
        if not self.parse_request(): 
            return
        
        # run do_GET if the command is GET
        if self.command == "GET":
            self.do_GET()
        # if the command is not GET, it is not supported
        else:
            self.send_error(501, "Unsupported method (%s)" % self.command)
            return        
        
        
    # called when an error occurs
    # matches the error code with a message
    # if a message was provided, that message is used instead
    def send_error(self, code, message=None):
        # list of responses used in this code
        responses = {200: ('OK', 'Request fulfilled, document follows'),
                     400: ('Bad request', 'Bad request syntax or unsupported method'),
                     404: ('Not Found', 'Nothing matches the given URI'), 
                     500: ('Internal error', 'Server got itself in trouble'),
                     501: ('Not implemented', 'Server does not support this operation')
                     }

        shortmsg, longmsg = responses[code]
        # if a message is provided, use that instead
        if not message:
            message = shortmsg
        
        #call print_error_msg to print output for client
        self.print_msg(code, message, longmsg)
    
    # prints the error message if an error message is sent
    # called by send error
    def print_msg(self, code, message, longmsg):
        # creates the html output to tell the client the error
        htmlres = "<html><body>\r\n<h2>" + message + "</h2>\r\n" + longmsg + "</body></html>"
        # counts the length of the html output
        length = len(htmlres)
        
        # writes the message that goes above the html output
        self.send_responseline(code, message)
        self.send_header("Content-type", 'text/html')
        self.send_header("Content-Length", str(length))
        self.end_headers()
        self.wfile.write(htmlres)
    
    def send_response(self, code, message=None):
        # list of responses used in this code
        responses = {200: ('OK', 'Request fulfilled, document follows'),
                     400: ('Bad request', 'Bad request syntax or unsupported method'),
                     404: ('Not Found', 'Nothing matches the given URI'),
                     500: ('Internal error', 'Server got itself in trouble'),
                     501: ('Not implemented', 'Server does not support this operation')
                     }

        shortmsg, longmsg = responses[code]
        # if a message is provided, use that instead
        if not message:
            message = shortmsg
        
             
        
        self.send_responseline(code, message) 
    
    def send_responseline(self, code, message):
        self.wfile.write(self.version + " " + str(code) + " " + message + "\r\n")
    
    def version_string(self):
        sys_version = "Python/" + str(sys.version.split()[0])      
        server_version = "MyWebServer/" + str(__version__)       
        return server_version + " " + sys_version
    
    # returns the date in the proper format for GMT
    def get_date(self):
        currTime = time.time(self)
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
        if self.version != 'HTTP/0.9':
            self.wfile.write("%s: %s" % (header, value))
    
    # sends the blank line that indicates no more MIME headers
    def end_headers(self):
        # no headers in HTTP/0.9
        if self.version != 'HTTP/0.9':
            self.wfile.write("\r\n")
            
    def address_string(self):
        
        host, port = self.client_address[:2]
        return socket.getfqdn(host) 
    
    
    
    protocol_version = "HTTP/1.1"


def main():
    HOST, PORT = "localhost", 8080
   
    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    
    
if __name__ == '__main__':
    main()


                
        
        
        
        
    
            
        





        