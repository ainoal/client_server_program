# To execute a client-server program: first run the server application and
# leave the server running, listening to the right port.
# After that, you can run client program(s) that make requests to the server.

# TODO: Optional: add some kind of a backup for db.xml.
# TODO: Add multiple clients.
# (TODO: way to name notes.)
# TODO: What to return from each function?
# TODO: error handling for if client crashes

from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
from datetime import datetime
import xml.dom.minidom
import requests
import datetime

client_list = []
request_list = []

def main():
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Listening on port 8000")
    server.register_function(new_entry, "new_entry")
    server.register_function(search_topic, "search_topic")
    server.register_function(get_notes, "get_notes")
    server.register_function(query, "query")
    server.register_function(add_client, "add_client")
    server.register_function(remove_client, "remove_client")
    server.register_function(request, "request")
    server.register_function(free_critical_section, "free_critical_section")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("KeyboardInterrupt. Shut down server.")
    return None

# TODO: Consider different return data types for get_notes (e.g. a list)

# This function is used for fetching all the notes of a certain topic.
# When a client calls get_notes, it gets back the timestamp and text of
# each note concatenated in one single string.
def get_notes(topic, timestamp, pid):
    req = request(pid, timestamp)

    # Make sure the xml file exists before trying read it.
    try:
        tree = ET.parse("db.xml")
    except FileNotFoundError:
        create_file("db.xml")
        tree = ET.parse("db.xml")
    root = tree.getroot()

    topic_found = search_topic(root, topic)
    free_critical_section(req)
    str = ""
    for note in topic_found:
        str = str +note.find("timestamp").text +  ": " + note.find("text").text + "\n"
    return str

# This function creates a new entry in the database.
def new_entry(topic, txt, timestamp, pid):
    req = request(pid, timestamp)

    # Make sure the xml file exists before trying write to it.
    try:
        tree = ET.parse("db.xml")
    except FileNotFoundError:
        create_file("db.xml")
        tree = ET.parse("db.xml")
    data = tree.getroot()

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

    free_critical_section(req)
    return topic

def query(topic, pid):
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

    dt = datetime.datetime.now()
    date_time = dt.strftime("%d/%m/%Y - %H:%M:%S")
    new_entry(topic, str, date_time, pid)
    return str

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

# Create a simple xml file that can be used to build the database.
def create_file(filename):
    root = ET.Element("data")
    tree = ET.ElementTree(root)
    tree.write("db.xml", encoding = "UTF-8", xml_declaration = True)
    return None

class Request:
    def __init__(self, pid, timestamp):
        self.pid = pid
        self.timestamp = timestamp

# Request access to a critical section. In this program, critical sections
# are ones where the xml is read and written.
def request(pid, timestamp):
    req = Request(pid, timestamp)
    request_list.append(req)

    # Loop until the client is the next in line for accessing
    # the critical section.
    access = 0
    temp = 1
    while access == 0:
        for r in request_list:
            if req.timestamp > r.timestamp:
                temp = 0
        access = temp
    return req

# Remove request from the list when done.
def free_critical_section(req):
    try:
        request_list.remove(req)
    except ValueError:
        print("Could not remove request because it doesn't exist in the current request list.")
    return request_list
   
def add_client(pid):
    client_list.append(pid)
    print(client_list)
    return client_list

def remove_client(pid):
    try:
        client_list.remove(pid)
    except ValueError:
        print("Could not remove client from the list because it does not exist in the current list.")
    return client_list

main()
