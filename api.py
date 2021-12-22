from flask import Flask, jsonify,session, abort, make_response
import json

app = Flask(__name__)


@app.route("/get-blockchain", methods=["GET"])
def get_Blockchain():
	addr = "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE7MJ1Yf1Tn67DoeIStkdNyS2awavvJgva\nRpbRx7AzzUISL/5/b9zwHS0E3tnERowiNzULHlc/4nGxqHdBq+thtw=="
	try:
		f = open('blockchain.json')
		blockchain = json.load(f)
		return blockchain
	except Exception as e:
		print(e)
		return 0

app.route("/get-txpool", methods = ["GET"])
def get_TXPOOL():
	from node import TX_POOL
	return TX_POOL
if __name__ == "__main__":
	while True:
		app.run(host = '127.0.0.1', port = 9999)
