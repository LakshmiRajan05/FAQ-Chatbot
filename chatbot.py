import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import json
import pandas as pd
nltk.download('stopwords')
nltk.download('punkt_tab')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_text(query):
        tokens = word_tokenize(query.lower())
        # Remove stop words
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
        tokens = " ".join(tokens)
        return tokens

class ChatBot:
    
    def __init__(self):

        data1 = pd.read_csv("Mental_Health_FAQ.csv")
        data = data1.drop('Question_ID',axis=1)
        self.tokenized_faqs = []

        for i in range(data.shape[0]):
            self.tokenized_faqs.append({"question":preprocess_text(data.iloc[i,0]),"answer":data.iloc[i,1]})
        
    def query_matching(self, user_query):
        vectorizer = TfidfVectorizer()
        corpus = [faq['question'] for faq in self.tokenized_faqs] + [preprocess_text(user_query)]
        tfidf_matrix = vectorizer.fit_transform(corpus)
        cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        matched_index = cosine_sim.argmax()
        return self.tokenized_faqs[matched_index]['answer']