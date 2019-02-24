import sys
import socket
import re
import struct

HOST = '127.0.0.1'
PORT = 420

def is_valid_email(email):
	if len(email) > 7:
		return bool(re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.connect((HOST, PORT))
	while True:
		email = input('Enter an email: ')
		if len(email) <= 255 and is_valid_email(email):
			packer = struct.Struct('c c 255s')
			packed_data = packer.pack(b'Q', len(email).to_bytes(1, 'little'), email.encode('utf-8'))

			sock.sendall(packed_data)
			returned_data = sock.recv(257)
			unpacked_data = packer.unpack(returned_data)

			length_string = int.from_bytes(unpacked_data[1], byteorder='little')
			name = (unpacked_data[2][:length_string]).decode("utf-8")
			if name == "Error":
				print("No such name in directory! Try again.")
			else:
				print("Name:", name)
			#print('Received', repr(data))
			#print('Size', len(data))
		elif len(email) > 255:
			print("Email input too long.")
		elif not is_valid_email(email):
			print("Not a valid email")
