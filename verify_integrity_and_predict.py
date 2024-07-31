import json
import hashlib
import numpy as np
import tensorflow as tf
from web3 import Web3
from matplotlib import pyplot as plt
from tensorflow.keras.layers import Input

# Load local model data
with open("model_data.json", "r") as f:
    model_data = json.load(f)

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

# Load contract ABI from file
with open("abi.json", "r") as abi_file:
    abi = json.load(abi_file)

# Load contract address from file
with open("contract_info.json", "r") as address_file:
    contract_info = json.load(address_file)
contract_address = contract_info["contract_address"]

# Create the contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

# Retrieve the stored hashes from the blockchain
model_id = 1
stored_parameters_hash, stored_metadata_hash = contract.functions.getModelData(
    model_id
).call()

# Print retrieved hashes for debugging
print("Stored Parameters Hash:", stored_parameters_hash)
print("Stored Metadata Hash:", stored_metadata_hash)

# Compare the hashes
if (
    local_parameters_hash == stored_parameters_hash
    and local_metadata_hash == stored_metadata_hash
):
    print("Hashes match. Model data is verified and intact.")
    # Deserialize the model weights
    weights = json.loads(parameters_serialized)
    weights = [np.array(w) for w in weights]

    # Rebuild the model with the correct architecture
    model = tf.keras.models.Sequential(
        [
            Input(shape=(1,)),  # Explicit input layer definition
            tf.keras.layers.Dense(24, activation="relu"),
            tf.keras.layers.Dense(24, activation="relu"),
            tf.keras.layers.Dense(24, activation="relu"),
            tf.keras.layers.Dense(1),
        ]
    )

    # Verify the length of weights
    print(f"Number of weights in the model: {len(model.get_weights())}")
    print(f"Number of weights to be loaded: {len(weights)}")

    # Set the weights
    model.set_weights(weights)

    # Generate new data for predictions
    new_X = np.linspace(0, 2, 100).reshape(-1, 1)
    new_X_tensor = tf.convert_to_tensor(new_X, dtype=tf.float32)

    # Make predictions
    predictions = model.predict(new_X_tensor)

    # Print prediction summary
    print("Predictions made successfully. Displaying plot...")

    # Plot the predictions
    plt.figure(figsize=(10, 6))
    plt.plot(new_X, predictions, color="blue", label="Model predictions", linewidth=2)
    plt.title("Model predictions")
    plt.xlabel("Input (X)")
    plt.ylabel("Output (y)")
    plt.legend(loc="best")
    plt.grid(True)
    plt.show()
else:
    print("Model data integrity check failed.")
