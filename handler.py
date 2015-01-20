from server import MyWebServer
import SocketServer

PORT_NUMBER = 80

class MyHandler(MyWebServer):
    
    def do_GET(self):
        try:
            reply = False
            if self.path[-4:] == ".css":
                self.contenttype = "text/css"
                reply = True
            if self.path[-5:] == ".html":   
                self.contenttype = "text/html"
                reply = True
            
            if reply == True:
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', MyHandler.contenttype)
                self.send_header('Content-length', 0)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            else:
                self.send_error(404, "File Not Found: %s" % self.path)
        
        except:
            self.send_error(404, "File Not Found: %s" % self.path)

        
    def do_POST(self):
        self.send_error(501, 'do_POST not implemented')
                

    
    def do_HEAD(self):
        self.send_error(501, 'do_HEAD not implemented')
    """
    # provided 
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.request.sendall("OK")  
    """


    
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
    