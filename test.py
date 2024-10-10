# Create and save words.pkl
import pickle

words = ["hello", "world", "example"]  # Replace with your actual list
pickle.dump(words, open('words.pkl', 'wb'))

# Now you can load it
words = pickle.load(open('words.pkl', 'rb'))
