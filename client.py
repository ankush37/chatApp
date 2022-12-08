import socket
from threading import Thread, Lock
import random


names = {}
rooms = {}
user_to_room = {}

lock = Lock()

def create_room(num):
	rooms[num] = []

def join_room(id, c):
	if id in rooms:
		return True
	return False

def deal_with_client(c):
	c.send('NICKNAME'.encode('utf8'))
	nickname = c.recv(1024).decode('utf8')
	while True:
		data = c.recv(1024).decode('utf8')
		if data == 'ROOMS':
			if len(rooms.keys()) == 0:
				c.send('No rooms available'.encode('utf8'))
			else:
				c.send(str(list(rooms)).encode('utf8'))
		elif data == 'CREATE':
			num = random.randint(1,1000)
			while num in rooms:
				num = random.randint(1,1000)
				if len(rooms) >= 999:
					break
					sys.exit()
			create_room(num)
			c.send(f'{num}'.encode('utf8'))

		elif data == 'JOIN':
			id = int(c.recv(1024).decode('utf8'))
			if join_room(id,c):
				break
			else:
				c.send('FAILURE'.encode('utf8'))

	c.send('SUCCESS'.encode('utf8'))
	names[c] = nickname
	rooms[id].append(c)
	user_to_room[c] = id
	names[c] = nickname
	
	lock.acquire()
	broadcast(f"{nickname} joined".encode('utf8'), c)
	
	t1 = Thread(target=threaded, args=(c,))
	t1.daemon = True
	t1.start()



def broadcast(msg,emit):
	clients = rooms[user_to_room[emit]]
	for client in clients:

		if client != emit:
			client.send(msg)

	lock.release()


def main():
	host = ''
	port = 8000

	s = socket.socket()
	s.bind((host, port))

	print("Socket created")
	s.listen(100)

	print("Listening...")

	while True:
		c, addr = s.accept()
		print(f"Connected to {addr[0]}: {addr[1]}")

		t1 = Thread(target=deal_with_client, args=(c,))
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
			data = f"[{names[c]}]	" + data.decode('utf8')
			lock.acquire()
			broadcast(data.encode('utf8'), c)
		except Exception as e:
			break

	rooms[user_to_room[c]].remove(c)
	del user_to_room[c]
	lock.acquire()
	broadcast(f"{names[c]} left".encode("utf8"),c)
	del names[c]

	c.close()

if __name__ == '__main__':
	main()


