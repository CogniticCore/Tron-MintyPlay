import os
from dotenv import load_dotenv

from tronpy import Tron
# from tronpy.keys import PrivateKey

load_dotenv()

client = Tron(network='nile')
contract = client.get_contract(os.getenv("CONTRACT_ADDRESS"))
# PRIVATE_KEY = PrivateKey(bytes.fromhex(os.getenv("PRIVATE_KEY_STRING")))