import time

class myClass:
    def send_error(code, message):
        print (message)
    
    def parse_request():
        requestline = "GET /path/file.html HTTP/1.1\r\nHost: www.host1.com:80\r\n"
        #requestline = "GET http://www.somehost.com/path/file.html HTTP/1.2\r\nHost: www.host1.com:80\r\n"
        print requestline
        words = requestline.split()
        print words
        
        command = words[0]
        print "Command: " + command
        
        if words[1][:7] == 'http://':
            # absolute URL
            absoluteURL = words[1]
            print "Absolute URL: " + absoluteURL
        else:
            # path
            path = words[1]
            print "Path: " + path
        
        if words[2][:5] != 'HTTP/':
            send_error(400, "Bad Request Version (%s)" % version)
            return 0
        else: 
            version = words[2]
            print "Version: " + version
        
        return 1


    def parse_request(code, message=None):   
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
    get_date()


    



       
                


    