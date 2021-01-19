# -*- coding: utf-8 -
import os
import sys
import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
ps = PorterStemmer()

path=sys.argv[1]
# path='./corpus'
path = path+'/'
docid=0
termid=0
stemmed_tokens= []
    


f1=open('stoplist.txt','r')
content=f1.read()
stop_words=content.split()
f1.close()

f1=open('docids.txt','w+')


entries = os.listdir(path)
for entry in entries:
    f=open(path+entry,'r')
    try:
        soup = BeautifulSoup(f,'html.parser').find('html')
        if soup:
            for script in soup(["script", "style"]): # remove all javascript and stylesheet code
                script.extract()
        
            text= soup.text        
            text=text.lower()
            words=text.split()
            tokenized_words=[]
            
            for word in words:
                word = re.sub(r'[^a-zA-Z]', '', word)
                if word !='':
                    tokenized_words.append(word)                
            final_words=[word for word in tokenized_words if word not in stop_words]
            
            for token in final_words:
                token=ps.stem(token)
                if token not in stemmed_tokens:
                    stemmed_tokens.append(token)
                        
            f1.write(str(docid)+'\t'+entry+'\n')
            docid=docid+1
    except Exception as e:
            print("an error occured in html parsing of this file:"+ entry+'EXCEPTION')
            print(e)
    finally:        
        f.close()
    
f1.close()
f1=open('termids.txt','w+')
for token in stemmed_tokens:
    f1.write(str(termid)+'\t'+token+'\n')
    termid= termid+1
f1.close()    