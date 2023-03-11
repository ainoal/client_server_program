#https://docs.python.org/3/library/xmlrpc.client.html#module-xmlrpc.client

import xmlrpc.client
import datetime
import os

def main():
    with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
        pid = os.getpid()
        proxy.add_client(pid)
        
        topic, text = get_input()
        print(topic)
        print(text)
        dt = datetime.datetime.now()
        date_time = dt.strftime("%d/%m/%Y - %H:%M:%S")
        print(dt)
        print(date_time)
        proxy.new_entry(topic, text, date_time, pid)

        notes = proxy.get_notes(topic, datetime.datetime.now(), pid)
        print("Here are all the entries of that topic:")
        print(notes)

        q = input("Topic to query: ")
        query_results = proxy.query(q, pid)
        print("These Wikipedia articles were found and added to your notes:",
              query_results)

        proxy.remove_client(pid)
    return None

def get_input():
    topic = input("Topic: ")
    text = input("Text: ")
    return (topic, text)

main()
