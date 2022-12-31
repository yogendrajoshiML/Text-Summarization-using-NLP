import spacy
from nltk.corpus import stopwords
from string import punctuation
from nltk.stem import LancasterStemmer,WordNetLemmatizer
import heapq




nlp=spacy.load("en_core_web_md")

#Removing Whitespaces and newlines

def white_spaces(data):
    import re 
    res=re.sub(r'\s+'," ",data)
    return res

stopwords_list=stopwords.words('english')

def text_summarizer(text):
    text=white_spaces(text)
    doc=nlp(text)
    words=[word.text.lower() for word in doc if (word.text.lower() not in stopwords_list) and (word.text.lower() not in punctuation)]

    word_frequencies_non_lemma={}
    for word in words:
        if word not in word_frequencies_non_lemma:
            word_frequencies_non_lemma[word]=1
        else:
            word_frequencies_non_lemma[word]+=1
            
    max_freq=max(word_frequencies_non_lemma.values())
    for key in word_frequencies_non_lemma:
        word_frequencies_non_lemma[key]= word_frequencies_non_lemma[key]/max_freq
        
    sent_score_non_lemma={}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_frequencies_non_lemma.keys():
                if sent not in sent_score_non_lemma:
                    sent_score_non_lemma[sent]=word_frequencies_non_lemma[word.text.lower()]
                else:
                    sent_score_non_lemma[sent]+=word_frequencies_non_lemma[word.text.lower()]
    sent_no=int(len(list(doc.sents))*.3)
    sent_list=heapq.nlargest(sent_no,sent_score_non_lemma,key=sent_score_non_lemma.get)
    text_data=[str(data) for data in sent_list ]
    return " ".join(text_data)

text_summarizer("Hi")
