import socket
from threading import Thread
from _thread import *


clients = []
names = {}

def broadcast(msg,emit=None):
	for client in clients:
		if client != emit:
			client.send(msg)


def main():
	host = ''
	port = 8000

	s = socket.socket()
	s.bind((host, port))

	print("Socket created")
	s.listen(5)

	print("Listening...")

	while True:
		c, addr = s.accept()
		print(f"Connected to {addr[0]}: {addr[1]}")
		c.send('NICKNAME'.encode('utf8'))
		nickname = c.recv(1024).decode('utf8')
		broadcast(f"{nickname} joined".encode('utf8'))
		clients.append(c)
		names[c] = nickname

		t1 = Thread(target=threaded, args=(c,))
		t1.daemon = True
		t1.start()

	s.close()


def threaded(c):
	while True:
		try:
			data = c.recv(1024)
			if data.decode('utf8')=='--QUIT--':
				print('Bye')
				break

			broadcast(data, c)
		except Exception as e:
			break

	clients.remove(c)
	broadcast(f"{names[c]} left".encode("utf8"))
	del names[c]

	c.close()

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print(e)


