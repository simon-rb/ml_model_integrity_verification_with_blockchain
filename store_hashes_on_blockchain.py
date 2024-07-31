import json
import hashlib
from web3 import Web3

# Load local model data
with open("model_data.json", "r") as f:
    model_data = json.load(f)

# Ensure that 'parameters' and 'metadata' exist in the loaded data
if "parameters" not in model_data or "metadata" not in model_data:
    raise ValueError(
        "Model data file is missing required fields: 'parameters' or 'metadata'"
    )

parameters_serialized = model_data["parameters"]
metadata_serialized = model_data["metadata"]

# Compute local hashes
local_parameters_hash = hashlib.sha256(parameters_serialized.encode()).hexdigest()
local_metadata_hash = hashlib.sha256(metadata_serialized.encode()).hexdigest()

# Print computed local hashes for debugging
print("Local Parameters Hash:", local_parameters_hash)
print("Local Metadata Hash:", local_metadata_hash)

# Load EIP address from file
with open("eip_info.json", "r") as eip_file:
    eip_info = json.load(eip_file)
ganache_url = f"http://{eip_info['eip_address']}:8545"

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider(ganache_url))

if not web3.is_connected():
    raise ConnectionError("Failed to connect to Ganache.")

print("Connected to Ganache.")

# Retrieve the first account from Ganache to use as the default account
default_account = web3.eth.accounts[0]
print("Using default account:", default_account)

# Load contract address from file
with open("contract_info.json", "r") as contract_file:
    contract_info = json.load(contract_file)
contract_address = contract_info["contract_address"]

# Load ABI from file
with open("abi.json", "r") as abi_file:
    abi = json.load(abi_file)

# Create the contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

# Store the hashes on the blockchain
model_id = 1
print("Storing model data on blockchain...")
print(f"Parameters Hash being stored: {local_parameters_hash}")
print(f"Metadata Hash being stored: {local_metadata_hash}")
tx_hash = contract.functions.storeModelHash(
    model_id, local_parameters_hash, local_metadata_hash
).transact({"from": default_account})

# Wait for transaction receipt to confirm successful storage
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print("Transaction receipt:", receipt)

# Re-fetch the stored data to ensure it matches the local hashes
stored_parameters_hash, stored_metadata_hash = contract.functions.getModelData(
    model_id
).call()

# Print fetched hashes for debugging
print("Re-Fetched Stored Parameters Hash:", stored_parameters_hash)
print("Re-Fetched Stored Metadata Hash:", stored_metadata_hash)

# Check if they match the local hashes
if (
    local_parameters_hash == stored_parameters_hash
    and local_metadata_hash == stored_metadata_hash
):
    print("Data stored and verified successfully.")
else:
    print("Data mismatch after storage. Check transaction and contract logic.")
