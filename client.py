import socket
import sys
import threading
import os

def display():
	print("1. List all existing room")
	print("2. Create a new chat room")
	print("3. Join an existing room")

def list_all(c):
	c.send('ROOMS'.encode('utf8'))
	data = c.recv(1024).decode('utf8')
	print(data)

def create_chat_room(c):
	c.send(f'CREATE'.encode('utf8'))
	id = int(c.recv(1024).decode('utf8'))
	print(f"Room created with ID	{id}")
	return id

def join_room(c,id):
	c.send("JOIN".encode('utf8'))
	c.send(f'{id}'.encode('utf8'))

def start(c, name):
	d = c.recv(1024)
	c.send(name.encode('utf8'))
	while True:
		display()
		try:
			ch = int(input("Enter your choice: "))
		except Exception as e:
			print(e)
			sys.exit()
		if ch==1:
			list_all(c)
		elif ch==2:
			id = create_chat_room(c)
			join_room(c,id)
		elif ch==3:
			id = int(input("Enter the id of room: "))
			join_room(c,id)
		if ch==2 or ch==3:
			d = c.recv(1024).decode('utf8')
			if d=='FAILURE':
				print("Invalid id")
			elif d=="SUCCESS":
				os.system('cls')
				print(f"Room joined with id {id}")
				break


def listen_input(c):
	while True:
		data = c.recv(1024).decode('utf8')
		if data != "":
			print(data)

def take_input(c):
	print("Please leave for exit")
	msg = input()
	while msg != "":
		c.send(msg.encode('utf8'))
		msg = input()


def main():
	name = input("Please enter your nickname: ")
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = "127.0.0.1"
	port = 8000
	try:
		soc.connect((host, port))
	except:
		print("Connection Error")
		sys.exit()

	start(soc, name)
	t1 = threading.Thread(target=listen_input, args=(soc,))
	t1.daemon = True
	t2 = threading.Thread(target=take_input, args=(soc,))

	t1.start()
	t2.start()

	t2.join()
	soc.send(b'--QUIT--')
	sys.exit()


if __name__ == "__main__":
   main()
