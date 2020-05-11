from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import nltk
nltk.download('stopwords')
nltk.download('wordnet')


# In[5]:


tokenizer = RegexpTokenizer(r'\w+')
en_stopwords = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


# In[6]:

def removeLinksAndHashtags(text):
    word_list = text.split()
    url_regex='http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    for word in word_list:
        if(word[0] is"@" or word[0] is "#" or re.match(url_regex, word)):
            word_list.remove(word)
    return ' '.join(word_list)
def removeInvalidChar(text):
    otptstr= ""
    text = removeLinksAndHashtags(text)
    for i in text:
        num = ord(i)
        if (num >=0) :
            if (num <= 127):
                otptstr= otptstr + i
    return otptstr
def getStemmedReview(review):
    review = str(review)
    review = review.lower()
    review = removeInvalidChar(review)
    review = review.replace("<br /><br />"," ")
    review = review.replace("<br /><br />"," ")
#     print(review)
    # Tokenize
    tokens = tokenizer.tokenize(review)
    new_tokens = [token for token in tokens if token not in en_stopwords]
    stemmed_tokens = [lemmatizer.lemmatize(token) for token in new_tokens]
    
    cleaned_review = ' '.join(stemmed_tokens)
    return cleaned_review
def getStemmedDocument(X):
    cleaned_list = []
    for tweet in X:
        cleaned_review = getStemmedReview(tweet)
        cleaned_list.append(cleaned_review)
    return cleaned_list
