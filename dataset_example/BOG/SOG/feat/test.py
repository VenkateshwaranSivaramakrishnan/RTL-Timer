import pickle

# Path to your .pkl file
file_path = 'Rocket.pkl'

# Load and print the contents
with open(file_path, 'rb') as f:
    data = pickle.load(f)

# Print contents (pretty print if it's a dict)
print(data)
