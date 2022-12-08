import socket
import sys
import threading


def listen_input(c, name):
	while True:
		data = c.recv(1024).decode('utf8')
		if data != "":
			if data!="NICKNAME":

				print(data)
			else:
				c.send(name.encode('utf8'))

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
	t1 = threading.Thread(target=listen_input, args=(soc,name))
	t1.daemon = True
	t2 = threading.Thread(target=take_input, args=(soc,))

	t1.start()
	t2.start()

	t2.join()
	soc.send(b'--QUIT--')
	sys.exit()


if __name__ == "__main__":
   main()