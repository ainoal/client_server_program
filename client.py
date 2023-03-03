#https://docs.python.org/3/library/xmlrpc.client.html#module-xmlrpc.client

import xmlrpc.client

# Test program to run the client and server
with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
    print("3 is even: %s" % str(proxy.is_even(3)))
    print("100 is even: %s" % str(proxy.is_even(100)))
