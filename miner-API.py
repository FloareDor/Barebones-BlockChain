import hashlib as hash
import os
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
import json
import socket
import urllib.request
from flask import Flask, jsonify,session, abort, make_response
import json
import flask
import json

UDP_IP_ADDRESS = '127.0.0.1'
UDP_PORT_NO = 49000

NODE_IP_ADDRESS = "127.0.0.1"
NODE_PORT_NO = 9999
#serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

app = Flask(__name__)
@app.route("/mine", methods=["GET", "POST"])
def mine():
	data = flask.request.json
	block_str = data["block_str"]
	nonce = 0
	mined_block_hash = ""
	while str(mined_block_hash)[0:2] != "00":
		nonce+=1
		#block_Hash = hash.sha256(bytes((block_str+str(nonce)).encode("utf-8"))).hexdigest()
		mined_block_hash = hash.sha3_256(f"{block_str}{nonce}".encode('utf-8')).hexdigest()
		print(f"mining: nonce -> {nonce}\n{mined_block_hash}")

	return {"Nonce": nonce, "mined_block_hash": mined_block_hash}

if __name__ == "__main__":
	print("Rig setup successfully!")
	app.run(host = UDP_IP_ADDRESS, port = UDP_PORT_NO, debug = True)
