import socket
import struct
HOST = '127.0.0.1'
PORT = 420

addressbook = {
	"jeremy.ahn@stonybrook.edu": "Jeremy Ahn",
	"arunab@cs.stonybrook.edu": "Aruna Balasubramanian",
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
			received_data = conn.recv(257)
			if not received_data:
				break

			packer = struct.Struct('c c 255s')
			unpacked_data = packer.unpack(received_data)

			length_string = int.from_bytes(unpacked_data[1], byteorder='little')
			email = (unpacked_data[2][:length_string]).decode("utf-8") 

			if email in addressbook:
				contact = addressbook[email]
				packed_data = packer.pack(b'R', len(contact).to_bytes(1, 'little'), contact.encode('utf-8'))
				conn.sendall(packed_data)
			else:
				print("Nope")
				ret = "Error"
				packed_data = packer.pack(b'R', len(ret).to_bytes(1, 'little'), ret.encode('utf-8'))
				conn.sendall(packed_data)