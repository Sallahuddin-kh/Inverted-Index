# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 21:29:12 2020

@author: SALLAHUDDIN
"""

# -*- coding: utf-8 -*-

import os
import re
import pandas as pd 
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer

ps = PorterStemmer()

term_id_dict ={}
doc_id_dict ={}
list_tuples = []



class term_detail:
    def __init__(self, termid, oic, oid, position_list_tuple):
        self.termid = termid
        self.corpus_occurence = oic
        self.doc_occurence = oid
        self.term_positions = position_list_tuple

    



def read_IDS():

    
    global term_id_dict
    global doc_id_dict
    
    f=open('termids.txt','r')
    lines=f.readlines()
    f.close()
    
    
    
    for line in lines:
        key =[]
        value =[]
    
        found_value = False
        
    
        for i in line:
           if not found_value:
               if i =='\t':
                   found_value=True
               else:    
                   value.append(i)
           else:
               if i =='\n':
                   break
               key.append(i)    
           
        key=''.join(key)
        value = ''.join(value)
        term_id_dict[key]=int(value)
    

    
    
    f=open('docids.txt','r')
    lines=f.readlines()
    f.close()
    
    
    
    for line in lines:
        key =[]
        value =[]
    
        found_value = False
        
    
        for i in line:
           if not found_value:
               if i =='\t':
                   found_value=True
               else:    
                   value.append(i)
           else:
               if i =='\n':
                   break
               key.append(i)    
           
        key=''.join(key) 
        value = ''.join(value)
        doc_id_dict[key]=int(value)
        
        
        
def create_tuple_list():


    path='corpus/'
    
    f33=open('doc_index.txt','w+')
    f1=open('stoplist.txt','r')
    content=f1.read()
    stop_words=content.split()
    f1.close()
    
    
    
    entries = os.listdir(path)
    for entry in entries:
        stemmed_tokens= []
        
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
                    word = re.sub(r'[^a-zA-Z ]', '', word)
                    if word !='':
                        tokenized_words.append(word)               
                final_words=[word for word in tokenized_words if word not in stop_words]
                
                for token in final_words:
                    stemmed_tokens.append(ps.stem(token))
                    
                unique_words = []
                for token in stemmed_tokens:
                    if token not in unique_words:
                        unique_words.append(token)
                    
                did= doc_id_dict.get(entry)
                i=0
                for token in stemmed_tokens:
                    tid = term_id_dict.get(token)
                    list_tuples.append((int(tid),int(did),int(i)))
                    i=i+1
                try:
                    for uniq_token in unique_words:
                        tid = term_id_dict.get(uniq_token)
                        index_array = []
                        i = 0
                        for st_tok in stemmed_tokens:
                            if uniq_token == st_tok:
                                index_array.append(i)
                            i=i+1
                        f33.write(str(did)+'\t'+str(tid)+'\t')
                        for item in index_array:
                             f33.write(str(item)+'\t')
                        f33.write('\n')
                except Exception as e:
                    print(e)
                            
     
        except:
                print("an error occured in html parsing of this file:"+ entry)
        finally:        
            f.close()
    f33.close()
        
    
        
   
read_IDS()
create_tuple_list()




