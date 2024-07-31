from solcx import (
    compile_standard,
    install_solc,
)  # A Python library for compiling Solidity code
from web3 import Web3  # A Python library for interacting with Ethereum blockchain nodes
import json

# Install Solidity compiler version 0.8.0
install_solc("0.8.0")

# Read Solidity contract
with open("ModelStorage.sol", "r") as file:
    contract_source_code = file.read()

# Compile the contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"ModelStorage.sol": {"content": contract_source_code}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

# Bytecode and ABI
# ABI (Application Binary Interface): Defines the contract's functions and structures
# Bytecode: The compiled contract code that will be deployed on the blockchain
bytecode = compiled_sol["contracts"]["ModelStorage.sol"]["ModelStorage"]["evm"][
    "bytecode"
]["object"]
abi = json.loads(
    compiled_sol["contracts"]["ModelStorage.sol"]["ModelStorage"]["metadata"]
)["output"]["abi"]

# Load EIP address from file
with open("eip_info.json", "r") as eip_file:
    eip_info = json.load(eip_file)
ganache_url = f"http://{eip_info['eip_address']}:8545"

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Ensure there's an account to use
if web3.eth.accounts:
    default_account = web3.eth.accounts[0]
else:
    raise ValueError("No accounts found in the connected Ganache instance.")

# Deploy contract
ModelStorage = web3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = ModelStorage.constructor().transact({"from": default_account})
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# Store the contract address
contract_address = tx_receipt.contractAddress
print(f"Contract deployed at address: {contract_address}")

# Save the contract address to a JSON file
contract_info = {"contract_address": contract_address}

with open("contract_info.json", "w") as contract_file:
    json.dump(contract_info, contract_file)

print("Contract address saved to 'contract_info.json'.")
