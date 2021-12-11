from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey

import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789


clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)




class Sender:
	def __init__(self, publicKey = None, privateKey = None):
		if privateKey == None:
			self.privateKey = PrivateKey()
			self.publicKey = self.privateKey.publicKey()
		else:
			self.publicKey = str(publicKey).replace('-----BEGIN EC PRIVATE KEY-----', '').replace('-----END EC PRIVATE KEY-----', '')
			self.privateKey = str(privateKey).replace('-----BEGIN EC PRIVATE KEY-----', '').replace('-----END EC PRIVATE KEY-----', '')
		print(f"HERE's YOUR ADDRESS / PUBLICKEY:\n------------------------------------------------------------\n{self.publicKey.toPem().replace('-----BEGIN PUBLIC KEY-----', '').replace('-----END PUBLIC KEY-----', '').strip()}\n----------------------------------------------------------------------")
		print(f"HERE's YOUR PRIVATE KEY, KEEP THIS SAFE AF!:\n------------------------------------------------------------------\n{self.privateKey.toPem().replace('-----BEGIN PUBLIC KEY-----', '').replace('-----END PUBLIC KEY-----', '').strip()}\n----------------------------------------------------------------------")

	def sign(self, value, receiver):
		trans_str = f"|{value}|{self.publicKey.toPem().replace('-----BEGIN PUBLIC KEY-----', '').replace('-----END PUBLIC KEY-----', '').strip()}|{receiver.replace('-----BEGIN PUBLIC KEY-----', '').replace('-----END PUBLIC KEY-----', '').strip()})|"
		signature = Ecdsa.sign(trans_str, self.privateKey)
		return signature, trans_str

	def verify_sign(self, trans_str, sign):
		return Ecdsa.verify(trans_str, sign, self.publicKey)

	def send(self, value, receiver):
		Message = f"{value}|{self.publicKey.toPem().replace('-----BEGIN PUBLIC KEY-----', '').replace('-----END PUBLIC KEY-----', '').strip()}|{receiver.replace('-----BEGIN PUBLIC KEY-----', '').replace('-----END PUBLIC KEY-----', '').strip()}"
		try:
			clientSock.sendto(Message.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))
			print("Transaction Successful!")
		except:
			print("Connection Failed. Funds were not processed.")



if __name__ == "__main__":
	account1 = Sender()
	account2 = Sender()
	while(True):
		value = input("Number of Coins: ")
		
		receiver = input("Input the address/publicKey- To:\n")
		receiver = f"-----BEGIN PUBLIC KEY-----\n{receiver}\n-----END PUBLIC KEY-----"

		#receiver = account2.publicKey.toPem()
		#print(PublicKey.fromPem(receiver))
		receiver = account2.publicKey.toPem()
		signature, trans_str = account1.sign(value ,receiver)
		if account1.verify_sign(trans_str, signature) == True:
			print("Verified.")
			account1.send(value , receiver)
		else:
			print("Verification failed.")
	
	