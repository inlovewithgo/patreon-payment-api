import requests
from flask import Flask, jsonify
from typing import List, Dict, Optional
from api.nonpaid import non_paid
from api.paid import paid
from core.requests import PatreonAPI
from dotenv import load_dotenv
import os
load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
client = PatreonAPI(ACCESS_TOKEN)
app = Flask(__name__)
app.register_blueprint(non_paid(client))
app.register_blueprint(paid(client))

if __name__ == "__main__":
    app.run(port=6969)