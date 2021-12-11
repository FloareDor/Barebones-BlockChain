import hashlib as hash
import os
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
import json
import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
MINER_PORT_NO = 49000

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

class Block:
	def __init__(self,value, sender, receiver, prev = None):
		self.value = value
		self.sender = str(sender).replace('-----BEGIN EC PRIVATE KEY-----', '').replace('-----END EC PRIVATE KEY-----', '')
		self.receiver = str(receiver).replace('-----BEGIN EC PRIVATE KEY-----', '').replace('-----END EC PRIVATE KEY-----', '')
		if prev == None:
			try:
				with open("blocks.json", 'r') as f:
					data = json.load(f)
				self.prev = data[len(data)-1]['hash']
				f.close()
			except:
				self.prev = prev
		else:
			self.prev = prev

	def mine_block(self):
		filename = "blocks.json"
		try:
			if os.stat(filename).st_size == 0:
				blocks = []
				with open(filename, mode = 'w') as f:
					json.dump(blocks,f)
		except:
			blocks = []
			with open(filename, mode = 'w') as f:
				json.dump(blocks,f)

		if os.stat(filename).st_size == 0:
			block_str = f"|{self.value}|{self.sender}|{self.receiver}|"
		else:
			block_str = f"|{self.value}|{self.sender}|{self.receiver}|{self.prev}|"
		serverSock.sendto(("MINE"+block_str).encode(), (UDP_IP_ADDRESS, MINER_PORT_NO))
		block_Hash, addr = serverSock.recvfrom(1024)
		block_Hash = str(block_Hash.decode()).replace("MINED", "")
		print(f"Added a block : {block_Hash}")
		if self.prev != None:
			block = {
				"value": self.value,
				"sender": self.sender,
				"receiver": self.receiver,
				"hash": block_Hash,
				"previous_Hash": self.prev
			}
		else:
			block = {
				"value": self.value,
				"sender": self.sender,
				"receiver": self.receiver,
				"hash": block_Hash,
			}
		f = open('blocks.json', 'r')
		blocks = json.load(f)
		with open(filename, 'w') as file:
			blocks.append(block)
			json.dump(blocks, file)
		f.close()
		file.close()
		return block_Hash
	
	def create_block(self):
		filename = "blocks.json"
		try:
			if os.stat(filename).st_size == 0:
				blocks = []
				with open(filename, mode = 'w') as f:
					json.dump(blocks,f)
		except:
			blocks = []
			with open(filename, mode = 'w') as f:
				json.dump(blocks,f)

		if os.stat(filename).st_size == 0:
			block_str = f"|{self.value}|{self.sender}|{self.receiver}|"
		else:
			block_str = f"|{self.value}|{self.sender}|{self.receiver}|{self.prev}|"
			nonce = 0
		block_Hash = 'x'
		while str(block_Hash)[0:2] != "00":
			nonce+=1
			block_Hash = hash.sha256(bytes((block_str+str(nonce)).encode("utf-8"))).hexdigest()
			print(f"mining: nonce -> {nonce}")
		# serverSock.sendto(("MINE"+block_str).encode(), (UDP_IP_ADDRESS, MINER_PORT_NO))
		# block_Hash, addr = serverSock.recvfrom(1024)
		#block_Hash = str(block_Hash.decode()).replace("MINED", "")
		print(f"Added a block : {block_Hash}")
		if self.prev != None:
			block = {
				"value": self.value,
				"sender": self.sender,
				"receiver": self.receiver,
				"hash": block_Hash,
				"previous_Hash": self.prev
			}
		else:
			block = {
				"value": self.value,
				"sender": self.sender,
				"receiver": self.receiver,
				"hash": block_Hash,
			}
		f = open('blocks.json', 'r')
		blocks = json.load(f)
		with open(filename, 'w') as file:
			blocks.append(block)
			json.dump(blocks, file)
		f.close()
		file.close()
		return block_Hash



print("Node setup successfully!")

while True:
	data, addr = serverSock.recvfrom(1024)
	print(str(data.decode()))
	if str(data)[0:4] != "MINED":
		trans_list = str(data.decode()).split("|")
		value = trans_list[0]
		sender = trans_list[1]
		receiver = trans_list[2]
		block = Block(value, sender, receiver)
		block.mine_block()

	
	if str(data.decode()).islower() == "stop":
		break


		



