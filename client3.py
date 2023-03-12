######################################################################
# Client program for Distributed Systems course
# Assignment 2
# client3.py
# Author: ainoal
######################################################################

import xmlrpc.client
import datetime
import os

def main():
    with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
        pid = os.getpid()
        proxy.add_client(pid)
        while(True):
            action = menu()
            if (action == 1):
                # Make a new note
                make_new_note(proxy, pid)
            elif (action == 2):
                # Get contents of certain topic
                get_contents(proxy, pid)
            elif (action == 3):
                # Query Wikipedia
                query(proxy, pid)
            elif (action == 0):
                # End program
                print("Closing the connection. Thank you for using the program.")
                proxy.remove_client(pid)
                break
            else:
                # End program
                # This section should never be reached.
                print("An error has occurred. Ending client program.")
                proxy.remove_client(pid)
                break
    return None

def menu():
    while(True):
        print("What do you want to do:")
        print("1) Make a new note")
        print("2) Get the contents of the notebook for a certain topic")
        print("3) Query Wikipedia and add links to relevant articles to your notebook")
        print("0) Stop")
        choice = input("Your choice: ")
        try:
            choice = int(choice)
            if(0 <= choice <= 3):
                break
            else:
                print("Not a valid choice, please try again.\n")
                continue
        except ValueError:
            print("Please input your choice as an integer.\n")
    return choice

# Ask user for input and make a new note based on the input.
def make_new_note(proxy, pid):
    topic = input("Topic: ")
    text = input("Text: ")
    dt = datetime.datetime.now()
    date_time = dt.strftime("%d/%m/%Y - %H:%M:%S")
    proxy.new_entry(topic, text, date_time, pid)
    return None

# Ask user for a topic and search for contents of that topic in the notebook.
def get_contents(proxy, pid):
    topic = input("Which topic do you want to search: ")
    notes = proxy.get_notes(topic, datetime.datetime.now(), pid)
    if (notes == "NNF"):
        print("No notes found for that topic.")
    else:
        print("Here are all the entries of that topic:")
        print(notes)
    return None

# Ask user for a topic to query Wikipedia. If results are found, add them
# as a note to the notebook and inform the user.
def query(proxy, pid):
    q = input("Topic to query: ")
    query_results = proxy.query(q, pid)
    if (query_results == "NAF"):
        print("No Wikipedia articles found for your query.")
    else:
        print("These Wikipedia articles were found and added to your notes:",
            query_results)
    return None

main()

######################################################################
# eof
