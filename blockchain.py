TX_POOL = {}
import hashlib as hash
from ellipticcurve.ecdsa import Ecdsa
import json
from datetime import datetime, timezone

from ellipticcurve.publicKey import PublicKey
from ellipticcurve.signature import Signature

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
API_PORT_NO = 55555
MINER_PORT_NO = 49000

class Crypto:
	def __init__(self, block_Index = None, TXPOOL = None, tx_index = None):
		try:
			f = open('blockchain.json')
			data = json.load(f)
			self.block_Index = len(data)
			self.TXPOOL = data[str(self.block_Index-1)]["TXPOOL"]
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
		return

	def get_Balance(self, address):
		balance = 0
		
		try:
			if len(self.TXPOOL) != 0:
				for tx_index in self.TXPOOL:
					if self.TXPOOL[tx_index]["sender"] == address:
						balance-=float(self.TXPOOL[tx_index]["value"])
					elif self.TXPOOL[tx_index]["receiver"] == address:
						balance+=float(self.TXPOOL[tx_index]["value"])
			f = open('blockchain.json')
			blockchain = json.load(f)
			for block_index in blockchain:
				for tx_index in blockchain[block_index]["TXPOOL"]:
					if blockchain[block_index]["TXPOOL"][tx_index]["sender"] == address:
						balance-=float(blockchain[block_index]["TXPOOL"][tx_index]["value"])
					elif blockchain[block_index]["TXPOOL"][tx_index]["receiver"] == address:
						balance+=float(blockchain[block_index]["TXPOOL"][tx_index]["value"])
			f.close()
			print(f"MY FUCKING BALANCE: {balance}")
			return balance
		except Exception as e:
			print(e)
			return 0

	def get_All_transactions(self, address):
		transactions = {}
		ind = 0
		f = open('blockchain.json')
		blockchain = json.load(f)
		for block_index in blockchain:
			for tx_index in blockchain[block_index]["TXPOOL"]:
				if blockchain[block_index]["TXPOOL"][tx_index]["sender"] == address or blockchain[block_index]["TXPOOL"][tx_index]["receiver"] == address:
					transactions[str(ind)] = blockchain[block_index]["TXPOOL"][tx_index]
					ind+=1
		if len(self.TXPOOL) != 0:
			for tx_index in self.TXPOOL:
				if self.TXPOOL[tx_index]["sender"] == address or self.TXPOOL[tx_index]["receiver"] == address:
					transactions[str(ind)] = self.TXPOOL[tx_index]
					ind+=1
		return transactions

	def transact(self, value, sender, receiver, timestamp):
		transaction = {
			"value": value,
			"sender": sender,
			"receiver": receiver,
			"timestamp": timestamp,
		}
		tx_hash = hash.sha3_256(str(transaction).encode()).hexdigest()
		transaction["tx_hash"] = tx_hash
		self.update_variables()
		self.TXPOOL[str(self.tx_index)] = transaction
		self.tx_index+=1
		TX_POOL = self.TXPOOL
		return True
		#print(f"{value} coin(s) sent from {sender} to {receiver} at {timestamp}")

	def get_TXPOOL(self):
		return self.TXPOOL

	def create_Block(self, Nonce = None):
		try:
			f = open('blockchain.json')
			blockchain = json.load(f)
			block_Timestamp = str(datetime.now(timezone.utc))
			self.update_variables()
			#self.block_Index+=1
			block_Hash = hash.sha3_256(f"{self.TXPOOL}|{Nonce}|{block_Timestamp}".encode()).hexdigest()
			if self.block_Index > 0:
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
					"hash": block_Hash,
					"previous_Hash": "0"
				}
			with open('blockchain.json', 'w') as file:
				blockchain[self.block_Index] = block
				json.dump(blockchain, file)
			f.close()
			file.close()
			self.tx_index = 0
			self.block_Index+=1
			self.TXPOOL = {}
			TX_POOl = {}
			return block_Hash
		except Exception as e:
			print(f"found you: {e}")
			return

	def verify_Transaction(self, value, sender, receiver, timestamp, sign):
		transaction_str = f"{value}|{sender}|{receiver}|{timestamp}"
		#struct.upack("h", sign)
		sign = Signature._fromString(sign)
		balance = self.get_Balance(sender)
		sender_Key = PublicKey.fromString(sender)
		if not Ecdsa.verify(transaction_str, sign, sender_Key):
			return -2
		if float(value) > balance and sender!="a163137532f511a4991eb105fa89f5ebb2953b82ceb08573e6bff3844c34c6a8eb316b321c1f59573b610c0d9c360fd2543d60364487fc0bd3e96da72bce22dc":
			return -1
		return 1


		



