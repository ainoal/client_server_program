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
        proxy.new_entry(topic, text, date_time)

        notes = proxy.get_notes(topic)
        print("Here are all the entries of that topic:")
        print(notes)

        q = input("Topic to query: ")
        proxy.query(q)

        proxy.remove_client(pid)
    return None

def get_input():
    topic = input("Topic: ")
    text = input("Text: ")
    return (topic, text)

main()
