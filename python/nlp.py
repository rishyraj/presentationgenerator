import re
import pandas as pd
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords as s
import heapq
import json
import csv
import numpy as np
import time
from PIL import Image
import pickle
# plotting
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
stopwords = s.words('english')
np.seterr(divide='ignore', invalid='ignore')

def summarize_text(article_text,n_sent):
    
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = sent_tokenize(article_text)

    stopwords = s.words('english')

    word_frequencies = {}
    for word in word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                # if len(sent.split(' ')) < 30:
                    # print("hit")
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

    # print(sentence_scores)
    summary_sentences = heapq.nlargest(n_sent, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    return summary

def split_sentences(sentences,n_groups=3):
    n_of_sent = len(sentences)
    # print(n_of_sent)
    remainder = n_of_sent % n_groups
    grouped_sents = []
    sent = ""
    for i in range(n_of_sent):
        # print(i)
        if (i > n_of_sent-remainder-2):
            break
        sent+=sentences[i]+" "
        if ((i+1)%n_groups==0 and i!=0):
            grouped_sents.append(sent)
            sent=""
    sent=""
    for i in range(n_of_sent-1,n_of_sent):
        # print(i)
        sent+=sentences[i]
    grouped_sents.append(sent)
    return grouped_sents

def create_slides_text(filepath):

    data = []
    with open('C:\\Users\\Rish\Desktop\\Boilermake\\presentationgenerator\\python\\sample.txt',encoding='utf-8') as myfile:
        data = myfile.readlines()

    data = [x.strip() for x in data]
    slides = [] 
    for p in data:
        sents = sent_tokenize(p)
        # print(split_sentences(sents,n_groups=2))
        slide = []
        for group in split_sentences(sents,n_groups=2):
            summary = summarize_text(article_text=group,n_sent=1)
            slide.append(summary)
        slides.append(slide)
    return slides

def vec(w,words_dict, D=50):
    """
    Converts a word to an embedding vector
    """
    try:
        return np.array(words_dict[w])
    # if the word is not in our vocabulary, we return zeros
    except:
        return np.zeros(D)

def average_embedding(sentence,glove_vectors, D=50):
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
        emb = vec(word,glove_vectors)
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

def predict_glove_images(headline,glove_vectors,image_df,image_embeddings, k=2):
    """
    Predicts the closest matching image caption given an article headline
    Returns a list of image ids
    """
    # pre-processes the headline
    text_prep = preprocessing(headline)
    
    # finding the average embedding for the headline
    emb = average_embedding(text_prep,glove_vectors)
    
    # normalizing the embeddings
    # print(emb)
    emb = emb.reshape(-1,1)/np.linalg.norm(emb)
    
    # calculating the cosine distance. 
    # since the embeddings are normalized: this is the dot product of the embedding vector and the matrix
    scores_images = np.dot(image_embeddings, emb).flatten()
    
    # predict top k images
    top_k_images = image_df.iloc[np.argsort(-scores_images)[:k]]
    return top_k_images

def load_glove(D=50):
    try:
        f = open('data/indexed_data/glove_vectors.pickle','rb')
        words_dict = pickle.load(f)
        f.close()
        print("Loaded From Disk")
        return words_dict
    except:
        # loading glove data file
        print("No glove_vectors.pickle found: Getting Glove Vectors...")
        glove_data_file = f'model/glove/glove.6B.{D}d.txt'
        words = pd.read_csv(glove_data_file, sep=" ", index_col=0, header=None, quoting=csv.QUOTE_NONE)
        # creating a dictionary for accessing words quickly
        words_dict = {word: embed for word, embed in zip(words.index, words.values.tolist())}
        print(f'Loaded {len(words_dict.keys())} words from the GloVe file')
        f = open('data/indexed_data/glove_vectors.pickle','wb')
        pickle.dump(words_dict,f)
        print("Saved at data/indexed_data/glove_vectors for faster loading")
        f.close()
        return words_dict

def train(captions,min_words,D):
    # loading the dataset
    with open(captions) as json_file:
        data = json.load(json_file)

    ids, headlines, urls, all_images, articles, lens = [], [], [], [], [], []

    for i,idx in enumerate(data):
        try:
            headline = data[idx]['headline']['main'].strip()
            num_words = len(headline.split(' '))
            
            # removing article headlines if the number of words in the headline is less than 5
            if num_words < min_words:
                continue

            headlines.append(headline)
            lens.append(num_words)
            all_images.append(data[idx]['images'])
            urls.append(data[idx]['article_url'])
            articles.append(data[idx]['article'])
            ids.append(idx)
        
        # deals with situations where articles are missing a headline
        except:
            continue

    # creating a dataframe with our results
    article_df = pd.DataFrame({'idx': ids, 'headline': headlines, 'text': articles, 'url': urls, 'num_words': lens})
    print(f'Number of Articles: {article_df.shape[0]}')

    img_captions, img_article_ids, caption_lens, nums = [], [], [], []

    for i, img in enumerate(all_images):
        for k in img.keys():
            caption = img[k].strip()
            num_words = len(caption.split(' '))
            
            # removing article headlines if the number of words in the headline is less than 5
            if num_words < min_words:
                continue
            
            nums.append(k)
            img_captions.append(caption)
            caption_lens.append(num_words)
            img_article_ids.append(ids[i])
            
    # creating a dataframe with our results        
    image_df = pd.DataFrame({'article_idx': img_article_ids, 'caption': img_captions, 
                            'num_words': caption_lens, 'number': nums})
    print(f'Number of Images: {image_df.shape[0]}')

    # loading glove data file
    words_dict = load_glove(D)
    # image embeddings
    start_time = time.time()

    # saving the embeddings for all the image captions to a numpy array
    image_embeddings = np.zeros(shape=(len(image_df), D))
    for i, text in enumerate(image_df.caption.values):
        if i % 100000 == 0 and i > 0:
            print(f'{i} out of {len(image_df.caption.values)} done in {time.time() - start_time:.2f}s')
        text_prep = preprocessing(text)
        # emb = average_embedding(text_prep)
        image_embeddings[i] = average_embedding(text_prep,words_dict,D)
    print(f'{i} out of {len(image_df.caption.values)} done in {time.time() - start_time:.2f}s')
    print(image_embeddings)
    image_df.to_csv('data/indexed_data/image_df.csv')
    np.save('data/indexed_data/embeddings.npy',image_embeddings)
    print('files saved at data/indexed_data')

# captions = 'data/captioning_dataset.json'
# min_words = 5
# D = 50
# train(captions,min_words,D)

start_time = time.time()
#load indexed data

image_df = pd.read_csv('data/indexed_data/image_df.csv')
image_embeddings = np.load('data/indexed_data/embeddings.npy')

# print(image_embeddings)

# Load Glove Vectors
words_dict = load_glove()


k = 1

slides = create_slides_text('sample.txt')
print(slides[1])

images_data = [predict_glove_images(text,words_dict,image_df,image_embeddings, k) for text in slides[1]]
duration = time.time()-start_time

print("Created Metadata in",duration,"seconds")


images = []

for img_data in images_data:
    img_name = img_data.article_idx.values
    img_nums = img_data.number.values
    img_description = img_data.caption.values
    print(img_name,img_nums,img_description)
    images.append(Image.open(f'data/images/resized/{img_name[0]}_{img_nums[0]}.jpg'))

for img in images:
    img.show()