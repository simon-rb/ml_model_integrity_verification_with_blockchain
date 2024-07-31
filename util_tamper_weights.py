import json
import numpy as np

# Load existing model data
with open("model_data.json", "r") as f:
    model_data = json.load(f)

# Deserialize and alter the weights slightly
weights = json.loads(model_data["parameters"])
weights[0] = (
    np.array(weights[0]) + 0.01
).tolist()  # Add a small value to the first weight array

# Re-serialize the weights
model_data["parameters"] = json.dumps(weights)

# Save the modified model data back to file
with open("model_data.json", "w") as f:
    json.dump(model_data, f)

print("Model weights have been tampered with.")
