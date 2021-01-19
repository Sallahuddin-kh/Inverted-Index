# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 22:45:58 2020

@author: SALLAHUDDIN
"""

import sys
import re
import linecache
from nltk.stem import PorterStemmer
import os

print(sys.argv[1])
ps = PorterStemmer()
def document_information():
    argument2 = sys.argv[2]
    print(argument2)
    f1 = open('docids.txt','r')
    document_id = -1
    doc_flag = 0
    while doc_flag == 0:
        line = f1.readline()
        line = line.split('\t')
        p = str(line[1])
        p = p.strip()
        if argument2 == p:
            doc_flag = 1
            document_id = line[0]
            print(document_id)
    
    f1.close()
    
    f1 = open('doc_index.txt','r')
    lines = f1.readlines()
    quit_flag = 0
    document_count = 0
    word_count = 0 
    for line in lines:
        if quit_flag == 2:
            break
        docs = line.split('\t')
        if docs[0] == document_id:
            document_count = document_count+1
            word_count = word_count + len(docs)-3
        elif int(docs[0])>int(document_id):
            break
    
    print('Listing for document: ',argument2)
    print('DOCID: ',document_id)
    print('Distinct terms: ',document_count)
    print('Total terms: ',word_count )

def get_term_information():
    try:
        argument2 = sys.argv[2]
        term = ps.stem(argument2)
        f1 = open('termids.txt','r')
        word_id = -1
        word_flag = 0
        i = 0
        while word_flag == 0:
            i = i+1
            line = f1.readline()
            line = line.split('\t')
            t = len(line)
            if len(line) == 1:
                break
            else:
                p = str(line[1])
                p = p.strip()
                if term == p:
                    word_flag = 1
                    word_id = line[0]
            
        if word_id!=-1:
            f1 = open('term_info.txt','r')
            lines = f1.readlines()
            for line in lines:
                line = line.split('\t')
                if line[0]==word_id:
                    print('listing for the term: ', argument2 )
                    print('id:',line[0])
                    print('offset:',line[1])
                    print('Total occurence in entire dataset',line[2])
                    print('Total number of documents containing the term',line[3])
                    break
            f1.close()
        else:
            print('Dataset does not contain the word!')
        
        
    except Exception as e:
        print(e)

def get_inverted_list():
    argument1 = sys.argv[4]
    
    f1 = open('docids.txt','r')
    document_id = -1
    doc_flag = 0
    while doc_flag == 0:
        line = f1.readline()
        line = line.split('\t')
        p = str(line[1])
        p = p.strip()
        if argument1 == p:
            doc_flag = 1
            document_id = line[0]
    
    f1.close()
    argument2 = sys.argv[2]
    term = ps.stem(argument2)
    f1 = open('termids.txt','r')
    word_id = -1
    word_flag = 0
    i = 0
    while word_flag == 0:
        i = i+1
        line = f1.readline()
        line = line.split('\t')
        t = len(line)
        if len(line) == 1:
            break
        else:
            p = str(line[1])
            p = p.strip()
            if term == p:
                word_flag = 1
                word_id = line[0]
                
    #print(document_id)
    #print(word_id)
    if word_id!=-1:
        offset = -1
        f1 = open('term_info.txt','r')
        lines = f1.readlines()
        for line in lines:
            line = line.split('\t')
            if line[0]==word_id:
                offset = int(line[1])
                break
        f1.close()
        f = open('termindex1.txt','r')
        f.seek(offset,os.SEEK_SET)
        #print(f.tell())
        line = f.readline()
        blocks = line.split('  ')
        positions = []
        block_length = len(blocks)
        doc_position=0
        word_position_array = []
        for i in range(1,block_length):
            marker = 0
            b = blocks[i].split(':')
            doc_position = doc_position + int(b[0])
            if doc_position==int(document_id):
                gl = b[1].split(' ')
                for word_pos in gl:
                    if word_pos !=' ':
                        marker = marker+int(word_pos)
                        word_position_array.append(marker)
            #print(word_position_array)
        
        print('Inverted List for the term: ', argument2)
        print('In document: ', argument1)
        print('TERMID: ', word_id)
        print('DOCID: ',document_id)
        print('term frequency', len(word_position_array))
        print('Positions',word_position_array)
    else:
        print('Dataset does not contain the word!')
    
    
    
    
    
arg_len = len(sys.argv)
if arg_len == 3:
    if str(sys.argv[1]) == '--doc':
        document_information()
    elif str(sys.argv[1]) == '--term':
        get_term_information()
    else:
        print('invalid keyword')
elif arg_len == 5:
    if str(sys.argv[1]) == '--term' and str(sys.argv[3]) == '--doc':
        get_inverted_list()
    else:
        print('invalid keyword')
else:
    print("invalid Arguments")