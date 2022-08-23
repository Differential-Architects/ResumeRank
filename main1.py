# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 18:44:35 2022

@author: barsuraj1
"""

from flask import Flask, render_template, request
import os
#import pickle
import pandas as pd
#import numpy as np
import docx2txt
import re
#import spacy
import spacy_universal_sentence_encoder


app = Flask(__name__)
#df = pd.read_pickle("Final_csv")

model = spacy_universal_sentence_encoder.load_model('en_use_md')

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/uploader', methods = ["GET","POST"])
def uploader():
    if request.method =="POST":
        #file = request.files["file"]
        #file.save(os.path.join("JD_Uploads", file.filename))
        
        #JD = docx2txt.process(file)
        #!!!!!!! CHANGES MADE!!!!! JD has to be in str format because model is expecting as str format to do vectorization.
        JD1 = "Business Analyst/ Senior Business Analyst /Analyst Proficient in MS Office, Microsoft Power BI," \
              "Tableau, Zoho Analytics, SQL, T-SQL, SAS BUSINESS INTELLIGENCE, ELT Tools, Advance Excel Certificate in Business Analysis"
        # list_JD = re.split(pattern = r"\n\n\t\n\n\t", string = JD )
        # Total_exp = ' \n '.join(str(e) for e in list_JD[2])
        # Total_exp = re.findall(pattern ="[0-9]+", string = Total_exp)
        # Avg_tenu = ' \n '.join(str(e) for e in list_JD[3])
        # Avg_tenu = re.findall(pattern ="[0-9]+", string = Avg_tenu)
        # strings = [str(Total_exp) for Total_exp in Total_exp]
        # a_string = "". join(strings)
        # Total_exp = int(a_string)
        Total_exp = 3 ##### !!!!!!!!CHANGES MADE !!!!!!!
        # strings = [str(Avg_tenu) for Avg_tenu in Avg_tenu]
        # a_string = "". join(strings)
        # Avg_tenu = int(a_string)
        Avg_tenu = 1 ##### !!!!!!!!CHANGES MADE !!!!!!!
        
        #### Filtering Based on Total Exp and Avg Tenure
        
        df = pd.read_csv("cleaned_df.csv")
        df = df[df['Total Derived Experience'] >= Total_exp]
        df = df[df['Average Tenure'] >= Avg_tenu] ### Uncomment if Avg Tenure is not req.
        df.set_index("Filename", inplace = True)
        df.to_csv('filtered_df.csv')
        df = pd.read_csv(r'C:\Users\barsuraj1\Desktop\Resume Ranking prediction\Sample_Resume\filtered_df.csv', delimiter=";")
        df = df.rename(columns={'Filename,Degree,Graduation,Total Derived Experience,Average Tenure,Roles,DomainSkills,ToolSkills,TechSkills,Skills,LANGUAGE,CERTIFICATION':'Candidate Details'})
        df_list = df.values.tolist()
        
        org_list= []
        cv_name = []
        cosine_score = []
        
        for elem in df_list:
            candidate_entities = elem
            Job_Desc_vector = model(JD1) ##### !!!!!!!!CHANGES MADE !!!!!!!
                        
            for sent in candidate_entities:
                sentences_embedding = model(sent)
                similar = sentences_embedding.similarity(Job_Desc_vector)
                similar = round(similar*100, 2)
                org_list.append(similar)
                filename = sent.split(',')[0]
                cv_name.append(filename)
                                
        mapped = zip(cv_name, org_list)
        mapped = list(mapped)
        resume_sort = sorted(mapped, key = lambda x: x[1], reverse=True)
        top_20 = resume_sort[:20]
        
        return render_template("index2.html", message = "The Job Description : ", Job_desc=JD1, top20= top_20 ) ##### !!!!!!!!CHANGES MADE !!!!!!!
        
       
if __name__ == "__main__":
    app.run()