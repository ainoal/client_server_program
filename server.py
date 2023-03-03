# To execute a client-server program: first run the server application and
# leave the server running, listening to the right port.
# After that, you can run client program(s) that make requests to the server.

from xmlrpc.server import SimpleXMLRPCServer

def is_even(n):
    if (n % 2 == 0):
        return True
    else:
        return False

server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000")
server.register_function(is_even, "is_even")
server.serve_forever()
