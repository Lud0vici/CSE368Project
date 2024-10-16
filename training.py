# importing the required modules. 
import random
import json
import pickle
import numpy as np
import nltk

nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')

import tensorflow as tf
from tensorflow.keras.models import Sequential
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

print(tf.__version__)

lemmatizer = WordNetLemmatizer()

# reading the json file
intents = json.loads(open("intents.json").read())

# creating empty lists to store data
words = []
classes = []
documents = []
ignore_letters = ["?", "!", ".", ","]

# Process intents and extract words and classes
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # separating words from patterns
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)  # adding to words list

        # associating patterns with respective tags
        documents.append((word_list, intent['tag']))

        # appending the tags to the class list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

    # storing the root words or lemma
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

# saving the words and classes list to binary files
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Prepare training data
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]

    # Create bag of words
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    # Making a copy of the output_empty
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1

    # Append the bag and output row to training
    training.append([bag, output_row])

# Shuffle the training data
random.shuffle(training)

# Convert training to numpy array
training = np.array(training, dtype=object)  # use dtype=object to avoid shape issues

# splitting the data
train_x = list(training[:, 0])
train_y = list(training[:, 1])

# Convert train_x and train_y to numpy arrays
train_x = np.array(train_x)
train_y = np.array(train_y)

# creating a Sequential machine learning model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# compiling the model
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train the model
hist = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# saving the model
model.save("my_model.keras")
# model.save('my_model.keras')?

# print statement to show the successful training of the Chatbot model
print("Yay!") 
