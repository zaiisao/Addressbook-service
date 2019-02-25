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
		if len(email) < 255 and is_valid_email(email):
			# Set a dynamically-sized structure of size 2 + len(email)
			packer = struct.Struct('c c ' + str(len(email)) + 's')
			packed_data = packer.pack(b'Q', len(email).to_bytes(1, 'little'), email.encode('utf-8'))

			# Send to server
			sock.sendall(packed_data)

			# Holds until hearing response to the server
			# At first, we don't know the length of the returning message string after the two bytes,
			# so we must read the second byte first to learn how many characters we must read after 
			packer = struct.Struct('c c')
			returned_data = sock.recv(256)
			# [0:2] = b'R' + two char representation of the following byte
			unpacked_data = packer.unpack(returned_data[0:2])

			length_string = int.from_bytes(unpacked_data[1], byteorder='little')

			# Now that we know the length of the string, redefine the packer structure and this time 
			# get all three returned property values of returned_data
			packer = struct.Struct('c c ' + str(length_string) + 's')
			unpacked_data = packer.unpack(returned_data)

			name = (unpacked_data[2][:length_string]).decode("utf-8")
			if name == "Error":
				print("No such name in directory!")
			else:
				print("Name:", name)
		elif len(email) == 0:
			# Empty input ends the client-sided service
			break
		elif len(email) >= 255:
			# Client-sided character limit
			print("Email input too long.")
		elif not is_valid_email(email):
			# We check if inputs are in valid email formats or not before bothering the server
			print("Not a valid email")

	# Close the socket when the while loop above is broken
	sock.close()
