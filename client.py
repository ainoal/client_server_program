#https://docs.python.org/3/library/xmlrpc.client.html#module-xmlrpc.client

import xmlrpc.client
import datetime

def main():
    with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
        topic, text = get_input()
        print(topic)
        print(text)
        dt = datetime.datetime.now()
        print(dt)
        proxy.new_entry(topic, text, dt)
        #print("3 is even: %s" % str(proxy.is_even(3)))
        #print("100 is even: %s" % str(proxy.is_even(100)))
    return None

def get_input():
    topic = input("Topic: ")
    text = input("Text: ")
    return (topic, text)

main()
