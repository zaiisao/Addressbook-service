# Addressbook-service

## About
This project was made by Jeremy Ahn for CSE 310 assignment 1 at Stony Brook University. A TCP socket app, this requires both a server and a client. The client sends the server an email address and the server refers to its directory to check and see if a corresponding first and last name is available.

This service was written in Python 3.

## Usage
To use the service, the server IP address and port must first be initialized. At the top both `server.py` and `client.py` source codes, the corresponding variables `HOST` (a string) and `PORT` (an integer) can be adjusted appropriately.

After the IP and port number is defined in both files, the `server.py` script would be run on the server and `client.py` on the client. Both can be run via the following commands:

**On Linux:**

(server)
```
sudo python server.py
```

(client)
```
python client.py
```

**On Windows:**

(server)
```
py server.py
```

(client)
```
py client.py
```

### Client information

* If you press enter without giving any input, the client will terminate.
* Input must be less than 255 characters long.
* Input must be of proper email format `(XX@XX.XX)`.

### Server information

#### Adding to the address book

To enter new emails into the address book, you can go to the top of the `server.py` file and add to the `addressbook` dictionary. Just like how as aforementioned emails must be less than 255 characters long, name strings (first + last names or theoretically anything you want) must be less than 255 characters long.

## Miscellaneous

In this version, multithreading is not supported.
