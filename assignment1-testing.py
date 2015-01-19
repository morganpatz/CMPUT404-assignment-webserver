import time
from mimetools import Message
from StringIO import StringIO

class myClass:
    def send_error(code, message):
        print (message)
    
    def parse_request():
        print "hello"
        #requestline = "GET /path/file.html HTTP/1.1\r\nHost: www.host1.com:80\r\n"
        #requestline = "GET http://www.somehost.com/path/file.html HTTP/1.2\r\nHost: www.host1.com:80\r\n"
        raw_requestline = 'GET http://www.hello.ca/search?sourceid=chrome&ie=UTF-8&q=ergterst HTTP/1.1\r\nConnection: keep-alive\r\nAccept: application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5\r\nUser-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.45 Safari/534.13\r\nAccept-Encoding: gzip,deflate,sdch\r\nAvail-Dictionary: GeNLY2f-\r\nAccept-Language: en-US,en;q=0.8\r\n'
        
        requestline, headers_alone = raw_requestline.split('\r\n', 1)
        headers = Message(StringIO(headers_alone))
        
        words = requestline.split()
        
        command = words[0]
        print "Command: " + command
        
        if words[1][1] != '/':
            # absolute URL
            path = words[1][7:]
            url, path = path.split('/', 1)
            path = "/" + path
        else:
            # path
            path = words[1]
            print "Path: " + path
        # tests if version is in correct form, must be 'HTTP/x.x
        if words[2][:5] != 'HTTP/':
            send_error(400, "Bad Request Version (%s)" % version)
            return 0
        else: 
            version = words[2]
            print "Version: " + version
        
        
        if 'Host' in headers:
            print "Host: " + headers['Host']
        else:
            print "400 error -- No Host"
        
        return 1


    def send_error(code, message=None):   
        responses = {200: ('OK', 'Request fulfilled, document follows'),
                     400: ('Bad request', 'Bad request syntax or unsupported method'),
                     500: ('Internal error', 'Server got itself in trouble'),
                     501: ('Not implemented', 'Server does not support this operation')
                     }

        shortmsg, longmsg = responses[code]
        if not message:
                message = shortmsg
        
        print_msg(code, message, longmsg)

    def print_msg(code, message, longmsg):
        version = "HTTP/1.1"
        htmlres = "<html><body>\r\n<h2>" + message + "</h2>\r\n" + longmsg+ "\r\n</body></html>"
        length = len(htmlres)
    
    
        print(version + " " + str(code) + " " + message)
        print("Content-Type: text/html")
        print("Content-Length: " + str(length))
        print("\r\n")
        print(htmlres)
    

    def get_date():
        currTime = time.time()
        year, mm, dd, h, m, s, wday, yday, isdst = time.gmtime(currTime)
        
        month = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        mm = month[mm]
        wday = day[wday]
        
        date = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (wday, dd, mm, year, h, m, s)
        
        return date
                
        
    if __name__ == '__main__':
        parse_request()


    



       
                


    