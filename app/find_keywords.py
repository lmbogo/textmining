"""
Created on Wed May  4 17:03:32 2022

@author: LMbogo
"""

#Load packages
import os
import re
#import sys
#sys.path.insert(0, python_root)
#import data_util

import pickle
import csv
import re
import pandas as pd
#text mining related packages
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

#to save files to esxel
import xlsxwriter

#set wd
#shared folder 'C:\Users\LMbogo\OneDrive - International Monetary Fund (PRD)\All_Raw_Data_By_Source'
#individual folders: 
# =============================================================================
#     AIV_2000-2021\txt
#     COM_Flagships\txt
#     Ereview\txt
#     Program_2021\txt
# =============================================================================
class read_files():
    def __init__(self, path):
        self.path = path
        os.chdir(self.path)
        
    #Read text file
    def __read_txt_file(self, file_path):
        with open(file_path, 'rb') as f:
            opened_file=f.readlines()
            return opened_file #opening file and returning content as string
    
    #def __parse_txt():
    
    #iterate through all files
    def iterate_through_files(self):
        opened_text_file=dict()
        for file in os.listdir():
            if file.endswith(".txt"):
                file_path = f"{self.path}/{file}"
                print(self.path, file_path, file)
                #call read text file function
                opened_text_file[file]=(self.__read_txt_file(file_path))
        return opened_text_file
    
class find_keywords():
    def __init__(self, keywords,content):
        self.keywords=keywords
        self.content=content
    
    ##Needs to have individual scenarios looked at and handled separately
    def regex_content(self):
        content=self.content.replace('U.S.','US')
        self.content=re.sub(r'[^a-zA-Z]',' ',content)    
        self.content=self.content.split()

    def iterate_through_content(self, key, keywords):
        iterator=0
        ind_word_dict=dict({'_Word_Count':0,'_key':key})
        for item in self.content:
            ##Where the code from the comment above goes
            if len(item)>1:
               # if item in ind_word_dict:
                    if any(item in word for word in keywords):#if the word is in any of the keywords
                        x=filter(lambda k: item in k,keywords)#filter the keywords to only keywords that the word are in
                        for occurrences in list(x):#iterate through filtered list
                            iter_1=iterator+1#counter to add next word in split counter
                            content_str=item
                            while(iter_1<len(self.content) and content_str in occurrences):#check through each word in the array element
                                if content_str.lower()== occurrences.lower():#if they are the same count up
                                    if occurrences in ind_word_dict:
                                        ind_word_dict[content_str]+=1
                                    else:
                                        ind_word_dict[occurrences]=1
                                content_str=content_str+' '+self.content[iter_1]
                                #making the next word in the array to check i.e. bank becomes bank profitability
                                iter_1+=1#iterates up the next content word
                    ind_word_dict['_Word_Count']+=1#word count
            iterator+=1#keeps count of where you are in the array
        return ind_word_dict

class retrieve_file_keywords():
    def __init__(self, basepath, keywords, filepaths, return_file):
        self.base_path=basepath
        self.keywords=keywords
        self.filepaths=filepaths
        self.return_file=return_file
        self.words_counted=[]
        self.content=dict()
        
    def __insert_dataframe(self): #to make sure code only returns dataframe
        v=self.keywords+['_Word_Count']
        return pd.DataFrame(data=self.words_counted, index=self.content, columns=v)
    
    def run(self):
        keyword_occurrences=dict()
        for filepath in self.filepaths:
            x = read_files(self.base_path+filepath)
            self.content=x.iterate_through_files()
            self.words_counted=[]
            for i in self.content:
                find_kwds=find_keywords(self.keywords, str(self.content[i]))
                newContent=find_kwds.regex_content()
                iterate_through=find_kwds.iterate_through_content(i,self.keywords)
                self.words_counted.append(iterate_through) 
            #keyword_occurrences is a dictionary that comprises the different folders as primary keys
            keyword_occurrences[filepath.split('/')[0]]=self.__insert_dataframe()
            print('done')
        self.__write_to_excel(keyword_occurrences)
    
    def __write_to_excel(self, keyword_occurrences):
        #you can change the path below to where you want the results save in your computer
        with pd.ExcelWriter(re.escape(self.return_file), engine='xlsxwriter') as writer:
            for df_key in self.filepaths:
                keyword_occurrences[df_key.split('/')[0]].to_excel(writer, sheet_name=df_key.split('/')[0])
        print('finished')
##NEEDS: more refinement on what is accepted as a word. i.e industries should 
## accept industry so you like do a x.slice(0,5) as a keyword and maybe
## do a dict dict_name[x.slice(0,5)][{'words':['industry', 'industries' 'industrialization'],count:3}    

   
