import json
import re
import nltk
from nltk import corpus

from nltk.corpus import stopwords
nltk.download('stopwords')

stopwords = set(stopwords.words('portuguese'))
print(stopwords)

def clean_text(input):

    # Removing punctuations in string
    result = re.sub(r'[^\w\s]', '', input)

    result = result.replace('\n',' ')
 
    return result

with open('/data/preprocess/tickets_labeled.json', 'r') as file:
    data = json.load(file)
    
    data_phase_one = []

    for item in data:

        test_str = item['article_body']

        # Remove \n
        regex = r'\n{1,}'
        subst = " "
        result = re.sub(regex, subst, test_str, 0, re.MULTILINE)

        # Remove [digits]
        regex = r'\[\d{1,}\]'
        subst = " "
        test_str = result
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

        # Remove other common characters not relementvant
        result = clean_text(result)

        # Remove more than 2 spaces consecutives
        regex = r'\s{2,}'
        subst = " "
        test_str = result
        result = re.sub(regex, subst, test_str, 0, re.MULTILINE)
   
\
        # Remove stop words
        output = []
        for word in result.split():
            temp_list = []
            if word.lower() not in stopwords:
                temp_list.append(word)
                output.append(' '.join(temp_list))

        print('Prepare data phase completed.')