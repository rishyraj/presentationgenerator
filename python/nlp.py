import bs4 as bs
import urllib.request
import re
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords as s
import heapq
import pke
import RAKE

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



# scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')
# article = scraped_data.read()

# parsed_article = bs.BeautifulSoup(article,'lxml')

# paragraphs = parsed_article.find_all('p')
# article_text = ""

# for p in paragraphs:
#     article_text += p.text


stopwords = s.words('english')
rake_object=RAKE.Rake(stopwords)

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
    # print()
    # print()
    # break
    # keywords = rake_object.run(p)
    # print("keywords: ",keywords)
    # break
    # summary = summarize_text(article_text=p,n_sent=7)    
    # print(summary)

# extractor = pke.unsupervised.TopicalPageRank()

# extractor.load_document(input='C:\\Users\\Rish\Desktop\\Boilermake\\presentationgenerator\\python\\sample.txt',language='en')

# extractor.candidate_selection(pos={'NOUN', 'PROPN', 'ADJ','VERB'})

# extractor.candidate_weighting()

# keyphrases = extractor.get_n_best(n=10)

# print(keyphrases)

# explanatory_connectors = ["because","due","since","when"]
test = "Today, the world is more connected than ever, due to advancements in digital technology."
keywords = rake_object.run(test)
print("keywords: ",keywords)
# test = re.sub("\W"," ",test).lower()

