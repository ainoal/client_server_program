# Distributed Systems Assignment 2
## Client-server program using RPC

This is a simple distributed system written for distributed systems course. The client-server program uses Remote Procedure Calls (RPC) for communication between server and its clients. The system serves as a notebook, where the user can:

- Add a new self-written note
- Search the notebook for notes related to a certain topic
- Query Wikipedia and add links to the found Wikipedia pages as a note
  - Maximum of 5 pages will be linked
  - If no Wikipedia pages were found with your query, no new note is added

This directory contains 3 identical clients. With these clients, the server can be tested for handling several requests at the same time, and more new clients can also be added. The program works when both the server and the clients are running on the same computer. Should this program be used actually as a distributed system, with clients running on different computers, it can be achieved with small adjustments: instead of PID, we can use a unique ID of each client machine to handle the clients.
