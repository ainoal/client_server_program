# To execute a client-server program: first run the server application and
# leave the server running, listening to the right port.
# After that, you can run client program(s) that make requests to the server.

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET

def main():
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Listening on port 8000")
    server.register_function(is_even, "is_even")
    server.register_function(new_entry, "new_entry")
    server.register_function(get_tree, "get_tree")

    # TODO: try-catch for KeyboardInterrupt
    server.serve_forever()
    return None

def get_tree():
    tree = ET.parse("db.xml")
    root = tree.getroot()
    return root

def new_entry(topic, txt, timestamp):
    #data = get_tree()
    tree = ET.parse("db.xml")
    data = tree.getroot()

    print(data.tag)

    # Append the new entry to the XML file.
    # TODO: make the XML style more beautiful.
    note = ET.SubElement(data, "topic", name=topic)
    ET.SubElement(note, "text").text = txt
    ET.SubElement(note, "timestamp")   #.text = timestamp

    #data.append(entry)
    tree.write("db.xml")

    # TODO: Return information about the XML file.
    temp_ret = 3
    return temp_ret

# Test program, should be deleted later
def is_even(n):
    if (n % 2 == 0):
        return True
    else:
        return False

main()
