# ML Model Integrity Verification with Blockchain

## Overview

This project demonstrates the integration of machine learning (ML) with blockchain technology to ensure the integrity of ML model data. The project covers everything from setting up a blockchain environment using Ganache, training a neural network model, storing and verifying model data on the blockchain, and using utility scripts for backup and data manipulation. The core idea is to leverage blockchain's decentralized and immutable nature to prevent tampering with ML model data (i.e. model parameters and metadata).

## Table of Contents

1. [Project Structure](#project-structure)
2. [Setup and Prerequisites](#setup-and-prerequisites)
3. [ECS Instance and Ganache Setup](#ecs-instance-and-ganache-setup)
4. [Test Ganache Connection](#test-ganache-connection)
5. [Smart Contract](#smart-contract)
6. [Model Training and Data Storage](#model-training-and-data-storage)
7. [Hash Storage and Verification](#hash-storage-and-verification)
8. [Utility Scripts](#utility-scripts)
9. [Security Considerations](#security-considerations)

## Project Structure

### Core Scripts

- **`ecs_instance.py`**: Automates the creation and configuration of an ECS instance on Alibaba Cloud, sets up Docker, and runs Ganache, a private blockchain for Ethereum development.
- **`test_ganache_connection.py`**: Verifies the connection to the Ganache blockchain and retrieves the current block number.
- **`ModelStorage.sol`**: A Solidity smart contract for storing hashes of model parameters and metadata.
- **`deploy_contract.py`**: Compiles and deploys the Solidity smart contract to the Ganache blockchain.
- **`neural_network.py`**: Trains a neural network model, serializes its weights and metadata, and saves them locally.
- **`store_hashes_on_blockchain.py`**: Computes hashes of the model's weights and metadata, then stores these hashes on the blockchain.
- **`verify_integrity_and_predict.py`**: Verifies the model data's integrity using the blockchain-stored hashes and makes predictions if verification is successful.

### Utility Scripts

- **`util_backup_restore.py`**: Provides functions to backup and restore model data.
- **`util_tamper_weights.py`**: Simulates tampering with model weights to test the integrity verification process.

### Configuration and Data Files

- **`abi.json`**: Contains the ABI (Application Binary Interface) of the deployed smart contract.
- **`config.json`**: Alibaba Cloud configuration, including access keys and IDs.
- **`contract_info.json`**: Stores the address of the deployed smart contract.
- **`eip_info.json`**: Contains the Elastic IP (EIP) address of the ECS instance.
- **`model_data.json`**: Stores the serialized model weights and metadata.
- **`model_data_backup.json`**: Backup of `model_data.json`.

## Setup and Prerequisites

### Required Tools and Libraries

1. **Python 3.x**: The main programming language used.
2. **Alibaba Cloud SDK for Python**: To interact with Alibaba Cloud services.
3. **Web3.py**: For interacting with the Ethereum blockchain.
4. **Solc**: Solidity compiler for compiling smart contracts.

### Initial Configuration

1. **Install Dependencies**:
   ```bash
   pip install aliyun-python-sdk-core aliyun-python-sdk-ecs aliyun-python-sdk-vpc web3 py-solc-x
   ```

2. **Configure Alibaba Cloud Access**:
   - Fill in the `config.json` with your Alibaba Cloud access details.
   - This includes `access_key_id`, `access_key_secret`, `region_id`, `vpc_id`, `security_group_id`, and `vswitch_id`.

## ECS Instance and Ganache Setup

### `ecs_instance.py`

This script automates the creation of an ECS instance on Alibaba Cloud and installs Docker and Ganache. It also associates an Elastic IP (EIP) with the instance for external access.

**Key Functions**:
- `create_ecs_instance()`: Creates the ECS instance with specified configurations.
- `allocate_eip()`: Allocates an EIP for the instance.
- `associate_eip_with_instance()`: Links the allocated EIP with the ECS instance.
- `save_eip_to_file()`: Saves the EIP to a JSON file for later use.

**Execution**:
- Run the script to set up the ECS instance and Ganache:
  ```bash
  python ecs_instance.py
  ```

## Test Ganache Connection

### `test_ganache_connection.py`

This script is used to test the connection to the Ganache blockchain instance deployed on the ECS server. It verifies the network setup and ensures that the Ganache instance is running and accessible.

**Key Steps**:
1. **Load EIP Address**: The script reads the EIP address from the `eip_info.json` file.
2. **Connect to Ganache**: Utilizes the Web3.py library to establish a connection with the Ganache blockchain using the provided EIP address.
3. **Check Connection Status**: Verifies if the connection is successful and prints the current block number to confirm the blockchain is active.

**Execution**:
- Run the script to test the connection:
  ```bash
  python test_ganache_connection.py
  ```

### Output

- A confirmation message if connected successfully.
- The current block number from the Ganache blockchain.

## Smart Contract

### `ModelStorage.sol`

A Solidity smart contract designed to store hashes of the ML model parameters and metadata. The contract uses a mapping to associate a unique ID with each set of hashes.

**Key Functions**:
- `storeModelHash(uint256 _id, string memory _parametersHash, string memory _metadataHash)`: Stores the hashes on the blockchain.
- `getModelData(uint256 _id)`: Retrieves the stored hashes for a given ID.

### `deploy_contract.py`

This script compiles and deploys the `ModelStorage.sol` contract to the Ganache blockchain.

**Key Steps**:
1. **Compile the Contract**: Uses `solcx` to compile the Solidity code.
2. **Deploy the Contract**: Connects to Ganache and deploys the compiled contract.
3. **Save Contract Details**: The deployed contract's address is saved to `contract_info.json`.

**Execution**:
- Run the script to deploy the contract:
  ```bash
  python deploy_contract.py
  ```

## Model Training and Data Storage

### `neural_network.py`

Trains a simple neural network model and saves its weights and metadata.

**Key Features**:
- **Model Architecture**: Consists of three dense layers and an output layer.
- **Data Serialization**: Serializes the trained model's weights and metadata into `model_data.json`.

**Execution**:
- Train the model and save data:
  ```bash
  python neural_network.py
  ```

## Hash Storage and Verification

### `store_hashes_on_blockchain.py`

This script computes hashes of the model's parameters and metadata and stores these hashes on the blockchain.

**Execution**:
- Store the hashes on the blockchain:
  ```bash
  python store_hashes_on_blockchain.py
  ```

### `verify_integrity_and_predict.py`

Verifies the integrity of the model data using the stored blockchain hashes and makes predictions if the verification is successful.

**Execution**:
- Verify data integrity and make predictions:
  ```bash
  python verify_integrity_and_predict.py
  ```

## Utility Scripts

### `util_backup_restore.py`

Provides functionalities to backup and restore model data.

**Key Functions**:
- `backup_model_data()`: Backs up the current `model_data.json`.
- `restore_model_data()`: Restores the model data from the backup.

### `util_tamper_weights.py`

Alters the model weights to simulate a scenario where the model data has been tampered with.

## Security Considerations

- **Data Integrity**: The use of blockchain ensures that the hashes of the model's parameters and metadata cannot be tampered with without detection.
- **Confidentiality**: The actual model data is not stored on the blockchain, only the hashes. This approach maintains data confidentiality while ensuring integrity.

---
