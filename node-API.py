from flask import Flask, jsonify,session, abort, make_response
import json
import flask
import json
from blockchain import Crypto
import requests
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 9999
MINER_IP_ADDRESS = "127.0.0.1"
MINER_PORT_NO = 49000
crypto = None
#serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
app = Flask(__name__)

def get_Hash():
	TXPOOL = crypto.get_TXPOOL()
	block_str = f"{TXPOOL}"
	data = requests.get(f'http://{MINER_IP_ADDRESS}:{MINER_PORT_NO}/mine', json = {"block_str":block_str}).text
	data = json.loads(data)
	Nonce = data["Nonce"]
	mined_block_hash = data["mined_block_hash"]
	return mined_block_hash, Nonce

@app.route("/get-blockchain", methods=["GET"])
def get_Blockchain():
	try:
		f = open('blockchain.json')
		blockchain = json.load(f)
		f.close()
		return blockchain
	except Exception as e:
		with open('blockchain.json', "w") as f:
			json.dump({})
		f.close()
		print(e)
		return {}

@app.route("/transact", methods = ["GET"])
def transact():
	TXPOOL = crypto.get_TXPOOL()
	print(TXPOOL)
	try:
		trans_dict = flask.request.json
		trans_str = str(trans_dict["trans_str"])
		trans_list = trans_str.split("|")
		value = trans_list[0]
		sender = str(trans_list[1])
		receiver = trans_list[2]
		timestamp = trans_list[3]
		sign = trans_list[4]
		verified_val = crypto.verify_Transaction(value, sender, receiver, timestamp, sign)
		if verified_val == 1:
			print(f"main TXPOOL index: {crypto.tx_index}")
			print(f"main Block Index: {crypto.block_Index}")
			crypto.transact(value, sender, receiver, timestamp, sign)
		elif verified_val == -2 :
			print("Authentication Failed!")
		elif verified_val == -1:
			print("Not enough Balance!")
		else:
			print('wtf')
		if crypto.tx_index == 3:
			mined_block_hash, Nonce = get_Hash()

			crypto.create_Block(mined_block_hash, Nonce)
		return "True"
	except Exception as e:
		print(e)
		return "False"

@app.route("/get-balance", methods = ["GET"])
def get_Balance():
	try:
		balance = flask.request.json
		address = balance["address"]
		balance = crypto.get_Balance(address)
		balance = {"balance":str(balance)}
		return balance
	except Exception as e:
		print(e)
		return {"balance":0}

@app.route("/get-all-transactions", methods = ["GET"])
def get_All_transactions():
	data = flask.request.json
	address = data["address"]
	transactions = crypto.get_All_transactions(address)
	return jsonify(transactions)

if __name__ == "__main__":
	crypto = Crypto()
	print("Node setup successfully!")
	app.run(host = '127.0.0.1', port = 9999, debug = True)
		
