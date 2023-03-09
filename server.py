# To execute a client-server program: first run the server application and
# leave the server running, listening to the right port.
# After that, you can run client program(s) that make requests to the server.

# TODO: Add a function that checks if db.xml exists and is readable.
# Optional: add some kind of a backup.
# TODO: Add multiple clients.
# (TODO: way to name notes.)
# (TODO: what to return from each function?)

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import timedelta
import xml.dom.minidom
import os
import requests
import datetime

def main():
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Listening on port 8000")
    server.register_function(new_entry, "new_entry")
    server.register_function(search_topic, "search_topic")
    server.register_function(get_notes, "get_notes")
    server.register_function(query, "query")

    # TODO: try-catch for KeyboardInterrupt
    server.serve_forever()
    return None

# TODO: Consider different return data types for get_notes (e.g. a list)

# This function is used for fetching all the notes of a certain topic.
# When a client calls get_notes, it gets back the timestamp and text of
# each note concatenated in one single string.
def get_notes(topic):
    tree = ET.parse("db.xml")
    root = tree.getroot()

    topic_found = search_topic(root, topic)
    str = ""
    for note in topic_found:
        str = str +note.find("timestamp").text +  ": " + note.find("text").text + "\n"
    return str

# This function creates a new entry in the database.
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

def query(topic):
    session = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"

    my_params = {
        "action": "opensearch",
        "namespace": "0",
        "search": topic,
        "limit": "5",
        "format": "json"
    }

    R = session.get(url=URL, params=my_params)
    data = R.json()

    str = ""
    for i in range (0, len(data[3])):
        str = str + data[3][i] + " ;  "
    print(str)

    dt = datetime.datetime.now()
    date_time = dt.strftime("%d/%m/%Y - %H:%M:%S")
    new_entry(topic, str, date_time)

    return 1

def search_topic(root, topic):
    str_find = ".//topic[@name='" + topic + "']"
    elem = root.find(str_find)
    return elem

# Reference:
# https://stackoverflow.com/questions/749796/pretty-printing-xml-in-python/38573964#38573964
def write_xml(root):
    xml_string = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
    xml_string = "\n".join([s for s in xml_string.splitlines() if s.strip()])
    f = open("db.xml", "w")
    f.write(xml_string)
    f.close()
    return None

main()
