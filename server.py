# To execute a client-server program: first run the server application and
# leave the server running, listening to the right port.
# After that, you can run client program(s) that make requests to the server.

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import timedelta

import xml.dom.minidom
import os

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
    ET.SubElement(note, "timestamp").text = timestamp
    write_xml(data)

    # TODO: Return information about the XML file.
    temp_ret = 3
    return temp_ret

# Reference:
# https://stackoverflow.com/questions/749796/pretty-printing-xml-in-python/38573964#38573964
def write_xml(root):
    xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
    xml_string = '\n'.join([s for s in xml_string.splitlines() if s.strip()])
    f = open("db.xml", "w")
    f.write(xml_string)
    f.close()
    return None

# Test program, should be deleted later
def is_even(n):
    if (n % 2 == 0):
        return True
    else:
        return False

main()
