
import requests
import json
from datetime import datetime, timezone
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
import socket


UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789


clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.connect((UDP_IP_ADDRESS, UDP_PORT_NO))

def get(command):
	api = requests.get(f'http://127.0.0.1:9999/{command}')
	data = api.text
	if data != "-1":
		data = json.loads(data)

	return data

class Wallet():
	def __init__(self, public_Addr, private_Key):
		self.public_Addr = public_Addr
		self.private_Key = private_Key

	def get_Balance(self):
		data = requests.get(f'http://127.0.0.1:9999/get-balance', json = {"address":self.public_Addr}).text
		balance = json.loads(data)
		balance = balance["balance"]
		return balance

	def send(self, value, receiver):
		timestamp = str(datetime.now(timezone.utc))
		trans_str = f"{value}|{self.public_Addr}|{receiver.replace('-----BEGIN PUBLIC KEY-----', '').replace('-----END PUBLIC KEY-----', '').strip()}|{timestamp}"
		signature = Ecdsa.sign(trans_str,PrivateKey.fromString(self.private_Key))
		print(signature)
		signature = signature._toString()
		#test = Signature._fromString(signature)
		#print(test)
		#print(signature)
		Message = f"{value}|{self.public_Addr}|{receiver.replace('-----BEGIN PUBLIC KEY-----', '').replace('-----END PUBLIC KEY-----', '').strip()}|{timestamp}|{signature}"
		trans_dict = {"trans_str":Message}
		try:
			#clientSock.sendto(Message.encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))
			response = requests.get(f'http://127.0.0.1:9999/transact', json = trans_dict)
			#print(f"####{x}####")
			response = response.json()
			print(response["response"])
		except Exception as e:
			print(e)
			print("Connection Failed. Funds were not processed.")
	
	def get_All_transactions(self):
		data = requests.get(f'http://127.0.0.1:9999/get-all-transactions', json = {"address":self.public_Addr}).text
		transactions = json.load(data)
		return transactions

def in_Wallet(wallet):
	print("Logged in to your wallet successfully!")
	while True:
		ans = input("Send monies or check balance or link discord?(send/balance/discord)").lower()
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
		elif ans == "discord":
			res = input("Linking your discord account inevitably makes your funds prone to discord hecxser men. Do you still want to proceed?(Y/n)").lower()
			if res == "y":
				id = input("Please enter your discord id, including the four digit number: ")
				json = {id:wallet.public_Addr}
				print(json)
				response = requests.get(f'http://127.0.0.1:9999/discord-link', json = json).text
				print(response)




			
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
				wallet = Wallet(public_Key.toString(), private_Key.toString())
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


		





	
