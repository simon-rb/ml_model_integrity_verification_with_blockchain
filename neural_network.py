import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import json

# Generate synthetic data
np.random.seed(0)
X = np.linspace(0, 2, 100).reshape(-1, 1)
y = 0.5 * X**2

# Convert to TensorFlow tensors
X = tf.convert_to_tensor(X, dtype=tf.float32)
y = tf.convert_to_tensor(y, dtype=tf.float32)

# Build the model
model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Dense(24, activation="relu"),
        tf.keras.layers.Dense(24, activation="relu"),
        tf.keras.layers.Dense(24, activation="relu"),
        tf.keras.layers.Dense(1),
    ]
)

# Compile the model
model.compile(optimizer="adam", loss="mse")

# Train the model
history = model.fit(X, y, epochs=250, verbose=1)

# Evaluate the model
mse = model.evaluate(X, y, verbose=0)
print("Mean squared error:", mse)

# Serialize the model weights
weights = model.get_weights()
weights_serialized = json.dumps([w.tolist() for w in weights])

# Serialize metadata
metadata = {"epochs": 250, "loss": mse}
metadata_serialized = json.dumps(metadata)

# Save serialized data to local storage
with open("model_data.json", "w") as f:
    json.dump({"parameters": weights_serialized, "metadata": metadata_serialized}, f)

print("Model data saved locally in 'model_data.json'.")

# Plot training loss
plt.figure(figsize=(10, 6))
plt.plot(history.history["loss"])
plt.title("Model loss over epochs")
plt.ylabel("Loss (MSE)")
plt.xlabel("Epoch")
plt.grid(True)
plt.show()

# Generate new data for predictions
new_X = np.linspace(0, 2, 100).reshape(-1, 1)
new_X_tensor = tf.convert_to_tensor(new_X, dtype=tf.float32)

# Make predictions
predictions = model.predict(new_X_tensor)

# Plot training data and predictions
plt.figure(figsize=(10, 6))
plt.scatter(X.numpy(), y.numpy(), color="red", label="Training data (true y)", s=10)
plt.plot(new_X, predictions, color="blue", label="Model predictions", linewidth=2)
plt.title("Training data and model predictions")
plt.xlabel("Input (X)")
plt.ylabel("Output (y)")
plt.legend(loc="best")
plt.grid(True)
plt.show()
