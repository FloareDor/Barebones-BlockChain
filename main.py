import hashlib as hash
import os
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
import json
from eth_account import Account
import uuid



class Block:
	def __init__(self,value, sender, receiver, prev = None):
		self.value = value
		self.sender = sender
		self.receiver = receiver
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
			block_str = f"|{self.value}|{self.sender.toPem()}|{self.receiver.toPem()}|"
		else:
			block_str = f"|{self.value}|{self.sender.toPem()}|{self.receiver.toPem()}|{self.prev}"
		block_hash = hash.sha256(bytes(block_str.encode("utf-8"))).hexdigest()
		print("added a block")
		if self.prev != None:
			block = {
				"value": self.value,
				"sender": self.sender.toPem(),
				"receiver": self.receiver.toPem(),
				"hash": block_hash,
				"previous_Hash": self.prev
			}
		else:
			block = {
				"value": self.value,
				"sender": self.sender.toPem(),
				"receiver": self.receiver.toPem(),
				"hash": block_hash,
			}
		f = open('blocks.json', 'r')
		blocks = json.load(f)
		with open(filename, 'w') as file:
			blocks.append(block)
			json.dump(blocks, file)
		f.close()
		file.close()
		return block_hash


class Sender:
	def __init__(self, publicKey = None, privateKey = None):
		if privateKey == None:
			acct = Account.create(str(uuid.uuid4().hex))
			Account.enable_unaudited_hdwallet_features()
			self.privateKey = acct.key
			self.publicKey = acct.address
		else:
			self.publicKey = publicKey
			self.privateKey = privateKey

	def sign(self, value, receiver):
		trans_str = f"|{value}|{str(self.publicKey)}|{receiver})|"
		signature = Ecdsa.sign(trans_str, self.privateKey)
		
		return signature, trans_str

	def verify_sign(self, trans_str, sign):
		return Ecdsa.verify(trans_str, sign, self.publicKey)

	def send(self, value, receiver):
		block = Block(value, self.publicKey, receiver)
		block.create_block()


if __name__ == "__main__":
	account1 = Sender()
	account2 = Sender()
	value = 22

	signature, trans_str = account1.sign(value ,account2.publicKey)
	if account1.verify_sign(trans_str, signature) == True:
		print("Verified")
	else:
		print("Verification failed.")
	account1.send(value , account2.publicKey)

		



