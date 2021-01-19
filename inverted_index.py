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

forward_index_dict = []
term_index_list= []

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


    path='files/'
    
    
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
                
                
                did= doc_id_dict.get(entry)
                
                i=0
                for token in stemmed_tokens:
                    tid = term_id_dict.get(token)
                    list_tuples.append((int(tid),int(did),int(i)))
                    i=i+1
     
        except:
                print("an error occured in html parsing of this file:"+ entry)
        finally:        
            f.close()
        
    
        
def read_doc_index():
    global forward_index_dict
    f1=open('doc_index.txt','r')
    content=f1.read()
    lines=content.split('\n')
    f1.close()
    for line in lines:
        content = line.split()
        forward_index_dict.append(content)

def read_word_id_doc():
    global term_index_list
    f1=open('termids.txt' , 'r')
    content = f1.read()
    lines = content.split('\n')
    f1.close()
    for line in lines:
        content = line.split()
        term_index_list.append(content[0])
    
def create_inverted_index():
    f1=open('termindex1.txt','w+')

    for unique_word in term_index_list:
        temp1 = 0
        temp2 = 0
        f1.write(unique_word+' ')
        for doc_list in forward_index_dict:
            if len(doc_list)!= 0:
                if(doc_list[1] == unique_word):
                    #f1.write(' '+doc_list[0]+':')
                    temp1 = int(doc_list[0])
                    doc_delta = temp1 - temp2
                    temp2 = temp1
                    f1.write(' '+str(doc_delta)+':')
                    pos = int(doc_list[2])
                    f1.write(str(pos)+' ')
                    for i in range(3,len(doc_list)):
                        t = int(doc_list[i])-int(pos)
                        f1.write(str(t)+' ')
                        pos = int(doc_list[i])
        f1.write('\n')
   


def getSize(filename):
    st = os.stat(filename)
    return st.st_size
                
def create_term_info():
    f = open('termindex1.txt','r')
    f_info = open('term_info.txt','w+')
    index_size = getSize('termindex1.txt')
    i=1
    # while i<index_size:
    #     if f.read(i) == ' ':
    #         print(f.read(i+1))
    #     i=i+1
    byte = []
    size = 1
    byte.append(size)
    line = f.readline()
    
    pages = line.split('  ')
    word_id = pages[0]
    doc_appearance = 0
    word_appearance = 0
    for i in range(1, len(pages)):
        doc_appearance = doc_appearance + 1
        word_doc_info = pages[i]
        word_temp = word_doc_info.split(' ')
        word_appearance = word_appearance+len(word_temp)
    word_appearance = word_appearance -1
    m = 1
    f_info.write(str(word_id)+'\t'+str(m)+'\t'+str(word_appearance)+'\t'+str(doc_appearance)+'\n')
    
    p = f.tell()
    byte.append(p)
    while line:
        line = f.readline()
        pages = line.split('  ')
        word_id = pages[0]
        doc_appearance = 0
        word_appearance = 0
        for i in range(1, len(pages)):
            doc_appearance = doc_appearance + 1
            word_doc_info = pages[i]
            word_temp = word_doc_info.split(' ')
            word_appearance = word_appearance+len(word_temp)
        word_appearance = word_appearance -1
    
        f_info.write(str(word_id)+'\t'+str(p)+'\t'+str(word_appearance)+'\t'+str(doc_appearance)+'\n')
        
        
        p = f.tell()
        byte.append(p)
    
    

read_doc_index()
read_word_id_doc()
create_inverted_index()
create_term_info()





