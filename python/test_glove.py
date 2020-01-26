import csv
import time
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))

def vec(w, D=50):
    """
    Converts a word to an embedding vector
    """
    try:
        return np.array(words_dict[w])
    # if the word is not in our vocabulary, we return zeros
    except:
        return np.zeros(D)

def average_embedding(sentence, D=50):
    """
    Computes the average embedding of a sentence
    """
    total_embeddings = np.zeros(D)
    num_words = len(sentence.split())
    
    # a sanity check
    if num_words == 0:
        return total_embeddings
    
    # getting the embedding for each word
    for word in sentence.split():
        emb = vec(word)
        total_embeddings += emb
        
    # averaging the embeddings
    avg_embeddings = total_embeddings/num_words
    
    # so that we are not dividing by zero
    if np.linalg.norm(avg_embeddings) > 1e-10:
        return avg_embeddings/np.linalg.norm(avg_embeddings)
    else:
        return avg_embeddings

def preprocessing(sentence):
    """
    Preprocessing. Removes punctuation and stop words
    """
    # removing extra whitespace and making the sentence lower case
    sentence = sentence.lower().strip()
    
    # removing punctuation
    bad_chars = '-.?;,!@#$%^&*()+/{}[]\\":\'“’'
    for char in bad_chars:
        sentence = sentence.replace(char, ' ').strip()
    all_words = sentence.split()
    
    # removing stop words
    filtered_sentence = [w for w in all_words if not w in stopwords]
    return ' '.join(filtered_sentence)

D = 50

glove_data_file = f'model\glove\glove.6B.{D}d.txt'

words = pd.read_csv(glove_data_file, sep=" ", index_col=0, header=None, quoting=csv.QUOTE_NONE)

# creating a dictionary for accessing words quickly
words_dict = {word: embed for word, embed in zip(words.index, words.values.tolist())}
print(f'Loaded {len(words_dict.keys())} words from the GloVe file')


test_sentence = "Hello, this is a short test sentence."
start_time = time.time()

image_embeddings = np.zeros(shape=(10, D))

text_prep = preprocessing(test_sentence)
emb = average_embedding(text_prep)
image_embeddings[0] = emb
duration = time.time()-start_time
print(duration)
print(test_sentence)
print(emb)
