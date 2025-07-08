import requests
from flask import Flask, jsonify
from typing import List, Dict, Optional

from api.nonpaid import non_paid
from api.totalpaid import total
from api.paid import paid
from api.growth import growth
from api.tier import tier_analytics

from core.requests import PatreonAPI

from dotenv import load_dotenv
import os
load_dotenv()


# campaign will ne loaded automatically
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
client = PatreonAPI(ACCESS_TOKEN)
app = Flask(__name__)

app.register_blueprint(non_paid(client))
app.register_blueprint(tier_analytics(client))
app.register_blueprint(total(client))
app.register_blueprint(paid(client))
app.register_blueprint(growth(client))

if __name__ == "__main__":
    app.run(port=6969)