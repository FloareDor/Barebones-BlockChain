import hashlib as hash
import os
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
import json
import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6790
NODE_PORT_NO = 6789
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

def mine(block_str):
	nonce = 0
	block_Hash = 'x'
	while str(block_Hash)[0:2] != "00":
		nonce+=1
		block_Hash = hash.sha256(bytes((block_str+str(nonce)).encode("utf-8"))).hexdigest()
		print(f"mining: nonce -> {nonce}")
	serverSock.sendto(("MINED"+str(block_Hash)).encode(), (UDP_IP_ADDRESS, NODE_PORT_NO))
	print(f'"MINED"{str(block_Hash)}')
	return True

if __name__ == "__main__":
	print("Mining rig setup.")
	while True:
		data, addr = serverSock.recvfrom(1024)
		print(data.decode())
		block_str = data
		block_str = str(block_str.decode())
		if block_str[0:4] == "MINE":
			if mine(block_str.replace("MINE", "")):
				print("Mining successful!")