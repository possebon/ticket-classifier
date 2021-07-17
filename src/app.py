import json
import re
import nltk
from nltk import corpus

from nltk.corpus import stopwords
from nltk.corpus import mac_morpho
from nltk.corpus.reader.chasen import test

import pandas as pd

from bs4 import BeautifulSoup
import requests
import unicodedata

def strip_accents(text):

    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text)

# Get last name content to create a dataset
page = requests.get("http://www.tiltedlogic.org/Familia/surnames-all.php", headers={"User-Agent": "XY"})
soup = BeautifulSoup(page.content, 'html.parser')
lastNamesList = soup.select("a[href*=mylastname]")

lastNames = [name.text.lower() for name in lastNamesList]

data = pd.read_csv('/data/preprocess/nomes.csv')

data['first_name'] = data['first_name'].str.lower()

names = data['first_name'].tolist()

stopwords = set(stopwords.words('portuguese'))

stopwords = [strip_accents(word) for word in stopwords]

# Start process the ticket data
with open('/data/preprocess/tickets_labeled.json', 'r') as file:
    data = json.load(file)
    
    data_phase_one = []

    for item in data:

        test_str = item['article_body'].lower()

        test_str = strip_accents(test_str)

        # Remove \xa0
        test_str = test_str.replace('\xa0', '')

        # Remove \n
        regex = r'\n{1,}'
        subst = " "
        result = re.sub(regex, subst, test_str, 0, re.MULTILINE)

        # Remove URLs
        regex = r'\b(?:(?:https?|ftp|file)://|www\.|ftp\.)(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[A-Z0-9+&@#/%=~_|$])'
        subst = " "
        test_str = result
        result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.IGNORECASE)

        # Remove e-mails
        regex = r'\S*@\S*\s?'
        test_str = result
        subst = " "
        result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.IGNORECASE)

        # Remove telephone numbers
        regex = r'\(\d{2,3}\)|(\d{2,3}).-?'
        test_str = result
        subst = " "
        result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.IGNORECASE)

        # Removing punctuations in string
        result = re.sub(r'[^\w\s]', ' ', result, 0, re.MULTILINE)

        result = re.sub(r'\\xa[0]', ' ', result, 0, re.MULTILINE)

        # Remove [digits] that could still exist
        regex = r'\d'
        subst = " "
        test_str = result
        result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.IGNORECASE)

        # Remove more than 2 spaces consecutives
        regex = r'\s{2,}'
        subst = " "
        test_str = result
        result = re.sub(regex, subst, test_str, 0, re.MULTILINE)

        #TODO: Need to deal with result and the output
        # tokens = nltk.word_tokenize(result)
        # tagged_sents = mac_morpho.tagged_sents()
        # unigram_tagger = nltk.tag.UnigramTagger(tagged_sents)
        # unigram_tagger.tag(tokens)  

        # Remove stop words
        output = []
        for word in result.split():
            temp_list = []
            if word.lower() not in stopwords:
                temp_list.append(word)
                output.append(' '.join(temp_list))

        # Remove person names
        result = [element for element in output if element not in names]
        # Remove person last names
        result = [element for element in result if element not in lastNames]

        # Remove duplicates
        result_uinque = []
        [result_uinque.append(element) for element in result if element not in result_uinque]

        # Remove not relevant terms
        irrelevant_terms = ['aguardo', 'obrigado', 'obrigada','alegre', 'bairro','lombroso','cj', 'rs',
            'desde','cipriani','mainroute','technology','business','facta', 'obs', 'ola', 'oi']
        result = [element for element in result_uinque if element not in irrelevant_terms]
        

        print('Prepare data phase completed.')