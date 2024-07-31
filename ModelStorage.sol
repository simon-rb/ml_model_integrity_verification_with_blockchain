// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ModelStorage {
    struct ModelData {  // Custom data type
        uint256 id;
        string parametersHash; // Hash of the parameters stored as a string
        string metadataHash;   // Hash of the metadata stored as a string
    }

    mapping(uint256 => ModelData) public models;

    function storeModelHash(uint256 _id, string memory _parametersHash, string memory _metadataHash) public {
        models[_id] = ModelData(_id, _parametersHash, _metadataHash);
    }

    function getModelData(uint256 _id) public view returns (string memory, string memory) {
        ModelData memory data = models[_id];
        return (data.parametersHash, data.metadataHash);
    }
}
