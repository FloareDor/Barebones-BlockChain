from ellipticcurve import signature
import requests
import json
from datetime import datetime, timezone
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
import socket

from ellipticcurve.signature import Signature

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789


clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.connect((UDP_IP_ADDRESS, UDP_PORT_NO))

def get(command):
	api = requests.get(f'http://127.0.0.1:9999/{command}')
	data = api.text
	data = json.loads(data)

	return data

class Wallet():
	def __init__(self, public_Addr, private_Addr):
		self.public_Addr = public_Addr
		self.private_Addr = private_Addr

	def get_Balance(self):
		blockchain = get("get-blockchain")
		TXPOOL = get("get-txpool")
		addr = self.public_Addr
		try:
			balance = 0
			for block_index in blockchain:
				for tx_Index in blockchain[block_index]["TXPOOL"]:
					if blockchain[block_index]["TXPOOL"][tx_Index]["sender"] == addr:
						balance-=float(blockchain[block_index]["TXPOOL"][tx_Index]["value"])
					elif blockchain[block_index]["TXPOOL"][tx_Index]["receiver"] == addr:
						balance+=float(blockchain[block_index]["TXPOOL"][tx_Index]["value"])
			for tx_Index in TXPOOL:
				if TXPOOL[tx_Index]["sender"] == addr:
					balance-=float(TXPOOL[tx_Index]["value"])
				elif TXPOOL[tx_Index]["receiver"] == addr:
					balance+=float(TXPOOL[tx_Index]["value"])
			return balance
		except Exception as e:
			print(e)
			return 0

	def send(self, value, receiver):
		timestamp = str(datetime.now(timezone.utc))
		trans_str = f"{value}|{self.public_Addr}|{receiver.replace('-----BEGIN PUBLIC KEY-----', '').replace('-----END PUBLIC KEY-----', '').strip()}|{timestamp}"
		signature = Ecdsa.sign(trans_str,PrivateKey.fromString(self.private_Addr))
		print(signature)
		signature = signature._toString()
		#test = Signature._fromString(signature)
		#print(test)
		#print(signature)
		Message = f"{value}|{self.public_Addr}|{receiver.replace('-----BEGIN PUBLIC KEY-----', '').replace('-----END PUBLIC KEY-----', '').strip()}|{timestamp}|{signature}"
		try:
			clientSock.sendto(Message.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))
			#print(f"####{x}####")
			print("Transaction Successful!")
		except:
			print("Connection Failed. Funds were not processed.")
	
	def get_All_transactions(self):
		blockchain = get("get-blockchain")
		TXPOOL = get("get-txpool")
		addr = self.public_Addr
		transactions = {}
		ind = 0
		try:
			balance = 0
			for block_index in blockchain:
				for tx_Index in blockchain[block_index]["TXPOOL"]:
					if blockchain[block_index]["TXPOOL"][tx_Index]["sender"] == addr or blockchain[block_index]["TXPOOL"][tx_Index]["receiver"] == addr:
						transactions[ind] = blockchain[block_index]["TXPOOL"][tx_Index]
						ind+=1
			for tx_Index in TXPOOL:
				if TXPOOL[tx_Index]["sender"] == addr or TXPOOL[tx_Index]["receiver"]:
					transactions[ind] = TXPOOL[tx_Index]
					ind+=1
			return transactions
		except Exception as e:
			print(e)
			return transactions

def in_Wallet(wallet):
	print("Logged in to your wallet successfully!")
	while True:
		ans = input("Send monies or check balance?(send/balance)").lower()
		if ans == "send":
			try:
				value = float(input("how many coins?"))
				try:
					receiver = input("Address of the receiver:\n")
					PublicKey.fromString(receiver)
					wallet.send(value, receiver)
				except Exception as e:
					print(e)
					print("Address invalid!")

			except:
				print("Please enter a number.")
		elif ans == "balance":
			balance = wallet.get_Balance()
			if balance == "None":
				balance = 0
			print(f"Your current balance: {balance}")

			
def main():
	while True:
		ans = input("Do you have an account already?(Y/n)").lower()
		if ans == 'y':
			try:
				public_Key = input("Pls enter your public key:\n")
				private_Key = input("Pls enter your private key:\n")
				msg = "Signing in"
				signature = Ecdsa.sign(msg, PrivateKey.fromString(private_Key))
			except:
				print("Keys are invalid. Try again!")
			if Ecdsa.verify(msg, signature, PublicKey.fromString(public_Key)):
				wallet = Wallet(public_Key, private_Key)
				print("Keys match! Logging you in....")
				in_Wallet(wallet)
				break
			else:
				print("Keys do not match. Try again!")
		elif ans == 'n' :
			ans = input("Do you wanna generate an account?(Y/n)")
			if ans == "y":
				private_Key = PrivateKey()
				public_Key = private_Key.publicKey()
				wallet = Wallet(public_Key, private_Key)
				print(f"Your Public Key / Address:\n{public_Key.toString()}")
				print(f"Your Private Key (Keep this safe af):\n{private_Key.toString()}")
				print("Logging you in....")
				print("Dude note the keys down in a safe place.")
				while True:
					reply = input("Log in to your wallet?(Y/n) (Please note the keys down in a safe place)").lower()
					if reply == "y":
						in_Wallet(wallet)
					else:
						print("Ok, waiting..")

			elif ans == 'n':
				print("Ok Byee")
		else:
			print("Invalid input!")

if __name__ == "__main__":
	main()


		





	
