from web3 import Web3  # A Python library for interacting with Ethereum blockchain nodes
import json

# Load EIP address from file
with open("eip_info.json", "r") as eip_file:
    eip_info = json.load(eip_file)
ganache_url = f"http://{eip_info['eip_address']}:8545"

# Connect to Ganache
# HTTPProvider is a subclass of Web3 that allows communication with an Ethereum node over HTTP
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check if connection is successful
if web3.is_connected():
    print("Connected to Ganache.")
else:
    print("Failed to connect to Ganache.")

# Fetch the current block number
block_number = web3.eth.block_number
print(f"Current block number: {block_number}")
