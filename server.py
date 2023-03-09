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
    server.register_function(search_topic, "search_topic")

    # TODO: try-catch for KeyboardInterrupt
    server.serve_forever()
    return None

def search_topic(root, topic):
    str_find = ".//topic[@name='" + topic + "']"
    elem = root.find(str_find)
    return elem

def new_entry(topic, txt, timestamp):
    tree = ET.parse("db.xml")
    data = tree.getroot()
    print(data.tag)

    # Search for the topic in the xml file.
    topic_found = search_topic(data, topic)

    # Append the new entry to the XML file.
    if topic_found==None:
        tpc = ET.SubElement(data, "topic", name=topic)
        note = ET.SubElement(tpc, "note", name="Note 1")
    else:
        note = ET.SubElement(topic_found, "note", name="Note x")
    ET.SubElement(note, "text").text = txt
    ET.SubElement(note, "timestamp").text = timestamp
    write_xml(data)

    # TODO: Return something that makes sense.
    temp_ret = 3
    return temp_ret

# Reference:
# https://stackoverflow.com/questions/749796/pretty-printing-xml-in-python/38573964#38573964
def write_xml(root):
    xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
    xml_string = "\n".join([s for s in xml_string.splitlines() if s.strip()])
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
