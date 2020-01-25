import re
import pandas as pd
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords as s
import heapq
import json
import csv
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import time
# plotting
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

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
    stopwords = s.words('english')

    data = []
    with open('C:\\Users\\Rish\Desktop\\Boilermake\\presentationgenerator\\python\\sample.txt',encoding='utf-8') as myfile:
        data = myfile.readlines()

    data = [x.strip() for x in data]
    slides = [] 
    for p in data:
        sents = sent_tokenize(p)
        # print(split_sentences(sents,n_groups=2))
        ct = 0
        slide = []
        for group in split_sentences(sents,n_groups=2):
            # ct+=1
            # print(ct,".")
            # print(group)
            # print()
            summary = summarize_text(article_text=group,n_sent=1)
            slide.append(summary)
            # print(summary)
        slides.append(slide)
    return slides

def predict_use_images(headline,embedder, k=2):
    """
    Predicts the closest matching image caption given an article headline
    Returns a list of image ids
    """
    # finding the embedding. No pre-processing is needed
    emb = embedder([headline])
    
    # normalizing the embeddings
    emb = emb/np.linalg.norm(emb)
    
    # calculating the cosine distance. 
    # since the embeddings are normalized: this is the dot product of the embedding vector and the matrix
    scores_images = np.dot(emb,use_img_embedding.T).flatten()
    
    # predict top k images
    top_k_images = image_df.iloc[np.argsort(-scores_images)[:k]]
    return top_k_images


# loading the dataset
with open('data/captioning_dataset.json') as json_file:
    data = json.load(json_file)

min_words = 5
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






# embed = hub.load('model\embed')

# start_time = time.time()

# # saving the use embeddings for all the image captions to a numpy array
# use_img_embedding = np.zeros((len(image_df),512))
# for i, text in enumerate(image_df.caption.values):
#     if i % 100000 == 0 and i > 0:
#         print(f'{i} out of {len(image_df.caption.values)} done in {time.time() - start_time:.2f}s')
#     emb = embed([text])
#     use_img_embedding[i] = emb
# print(f'{i} out of {len(image_df.caption.values)} done')

# # normalize embeddings
# use_img_embedding_normalized = use_img_embedding/np.linalg.norm(use_img_embedding,axis=1).reshape(-1,1)




# use predictions
# results_use = predict_use_images(headline,embed, 2)

# fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(14,5))
# idx = results_use.article_idx.values
# captions = results_use.caption.values
# nums = results_use.number.values

# print('USE Predictions')
# for i in range(k):
#     img = plt.imread(f'data/images/{idx[i]}_{nums[i]}.jpg')
#     ax[i].imshow(img)
#     ax[i].set_axis_off()
#     ax[i].set_title(captions[i])
# fig.tight_layout()