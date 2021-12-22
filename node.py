import hashlib as hash

from ellipticcurve.ecdsa import Ecdsa
import json
import socket
from datetime import datetime, timezone

from ellipticcurve.publicKey import PublicKey
from ellipticcurve.signature import Signature

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
MINER_PORT_NO = 49000

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
TX_POOL = {}
class Crypto:
	def __init__(self, block_Index = None, TXPOOL = None, tx_index = None):
		try:
			f = open('blockchain.json')
			data = json.load(f)
			self.block_Index = len(data)
			self.TXPOOL = data[str(self.block_Index - 1)]["TXPOOL"]
			self.tx_index = len(self.TXPOOL)
			if self.tx_index == 3:
				self.TXPOOL = {}
				self.tx_index = 0
		except Exception as e:
			print(e)
			data = {}
			with open("blockchain.json", "w") as f:
				json.dump(data,f)
			self.block_Index = 0
			self.TXPOOL = {}
			self.tx_index = 0

	def update_variables(self):
		if self.block_Index != 0 and self.tx_index != 0:
			f = open('blockchain.json')
			data = json.load(f)
			self.block_Index = len(data)

	def balance(self, address):
		balance = 0
		if not self.block_Index == 0 and not self.tx_index == 0:
			f = open('blockchain.json')
			blockchain = json.load(f)
			for block_index in blockchain:
				for tx_index in blockchain[block_index]["TXPOOL"]:
					if blockchain[block_index]["TXPOOL"][tx_index]["sender"] == address:
						balance-=float(blockchain[block_index]["TXPOOL"][tx_index]["value"])
					elif blockchain[block_index]["TXPOOL"][tx_index]["receiver"] == address:
						balance+=float(blockchain[block_index]["TXPOOL"][tx_index]["value"])
			return balance
		else:
			return 0

	def transact(self, value, sender, receiver, timestamp, sign):
		print(f"trans TXPOOL index: {self.tx_index}")
		print(f"trans Block Index: {self.block_Index}")
		transaction = {
			"value": value,
			"sender": sender,
			"receiver": receiver,
			"timestamp": timestamp,
			"signature": sign
			
		}
		self.update_variables()
		self.TXPOOL[str(self.tx_index)] = transaction
		self.tx_index+=1
		print(f"{value} coin(s) sent from {sender} to {receiver} at {timestamp}")
		TX_POOL = self.TXPOOL

	def get_TXPOOL(self):
		return self.TXPOOL

	def create_Block(self, Nonce = None):
		print(f"TXPOOL index: {self.tx_index}")
		print(f"Block Index: {self.block_Index}")
		try:
			f = open('blockchain.json')
			blockchain = json.load(f)
		except Exception as e:
			print(e)
			pass
		try:
			block_Timestamp = str(datetime.now(timezone.utc))
			self.update_variables()
			#self.block_Index+=1
			block_Hash = hash.sha256(f"{self.TXPOOL}|{Nonce}|{block_Timestamp}".encode()).hexdigest()
			if self.block_Index > 0:
				f = open('blockchain.json')
				blockchain = json.load(f)
				block = {
					"TXPOOL": self.TXPOOL,
					"Nonce": Nonce,
					"hash": block_Hash,
					"previous_Hash": blockchain[str(self.block_Index - 1)]["hash"]
				}
			else:
				block = {
					"TXPOOL": self.TXPOOL,
					"Nonce": Nonce,
					"hash": block_Hash
				}
			f = open('blockchain.json', 'r')
			blocks = json.load(f)
			with open('blockchain.json', 'w') as file:
				blocks[self.block_Index] = block
				json.dump(blocks, file)
			f.close()
			file.close()
			self.tx_index = 0
			self.block_Index+=1
			self.TXPOOL = {}
			return block_Hash
		except Exception as e:
			print(e)

	def verify_Transaction(self, value, sender, receiver, sign, timestamp):
		transaction_str = f"{value}|{sender}|{receiver}|{timestamp}"
		
		
		#struct.upack("h", sign)
		sign = Signature._fromString(sign)
		balance = self.balance(sender)
		sender_Key = PublicKey.fromString(sender)
		if not Ecdsa.verify(transaction_str, sign, sender_Key):
			return -2
		if float(value) > balance:
			return -1
		return 1

if __name__ == "__main__":
	print("Node setup successfully!")
	block = Crypto()
	while True:
		data, addr = serverSock.recvfrom(1024)
		if str(data)[0:4] != "MINED" and data != None:
			trans_list = str(data.decode()).split("|")
			value = trans_list[0]
			sender = str(trans_list[1])
			receiver = trans_list[2]
			timestamp = trans_list[3]
			sign = trans_list[4]
			verified_val = block.verify_Transaction(value, sender, receiver, sign, timestamp)
			if verified_val == 1:
				print(f"main TXPOOL index: {block.tx_index}")
				print(f"main Block Index: {block.block_Index}")
				block.transact(value, sender, receiver, sign, timestamp)
			elif verified_val == -2 :
				print("Authentication Failed!")
			elif verified_val == -1:
				print("Not enough Balance!")
			else:
				print('wtf')
			if block.tx_index == 3:
				block.create_Block()
		elif data.decode() == "BAL":
			serverSock.sendto("LETSGOOOOO".encode(), (addr[0], addr[1]))
		if str(data.decode()).islower() == "stop":
			break


		



