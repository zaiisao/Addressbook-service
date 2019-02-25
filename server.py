import socket
import struct
HOST = '127.0.0.1'
PORT = 420

addressbook = {
	"jeremy.ahn@stonybrook.edu": "Jeremy Ahn",
	"arunab@cs.stonybrook.edu": "Aruna Balasubramanianaaaaaaaaaaaaaaaaaaaaaaaa",
	"steve@apple.com": "Steve Jobs",
	"luke@gmail.com": "Luke Skywalker",
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.bind((HOST, PORT))
	sock.listen()
	conn, addr = sock.accept()
	with conn:
		print('Connected by ', addr)
		while True:
			received_data = conn.recv(256)
			if not received_data:
				break

			# We don't know the length of the email so only get the message type and string length
			packer = struct.Struct('c c')

			# At first, we don't know the length of the returning message string after the two bytes,
			# so we must read the second byte first to learn how many characters we must read after 
			# [0:2] = b'R' + two char representation of the following byte
			unpacked_data = packer.unpack(received_data[0:2])

			length_string = int.from_bytes(unpacked_data[1], byteorder='little')

			# Now that we know the length of the string, redefine the packer structure and this time 
			# get all three returned property values of returned_data
			packer = struct.Struct('c c ' + str(length_string) + 's')
			unpacked_data = packer.unpack(received_data)

			email = (unpacked_data[2][:length_string]).decode("utf-8") 

			if email in addressbook:
				contact = addressbook[email]
				# Redefine packer structure once again to match size of the contact's name
				packer = struct.Struct('c c ' + str(len(contact)) + 's')
				packed_data = packer.pack(b'R', len(contact).to_bytes(1, 'little'), contact.encode('utf-8'))
				conn.sendall(packed_data)
			else:
				ret = "Error"
				# Redefine packer structure once again to match size of the "Error" string
				packer = struct.Struct('c c ' + str(len(ret)) + 's')
				packed_data = packer.pack(b'R', len(ret).to_bytes(1, 'little'), ret.encode('utf-8'))
				conn.sendall(packed_data)

		sock.close()