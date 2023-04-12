from benchmark_reader import Benchmark
from benchmark_reader import select_files
import pandas as pd
from sklearn.feature_extraction.text import strip_accents_unicode
from unidecode import unidecode
import xml.dom.minidom
import os


path = os.path.abspath(os.curdir) +'/data/maltese/mt_train.xml'
outputPath = os.path.abspath(os.curdir) +'/2023-Challenge' + '/data/json'
b = Benchmark()

files = select_files(path)
b.fill_benchmark(files)
data_dct = b.to_dict()

mdata_dct={"input_text":[], "target_text":[]}
unique_props = set()

idx = 1
for st,unst in data_dct.items():
    for i in unst:

        # processing the input triples
        triples = []
        for triple in i[idx]['modifiedtripleset']:
            unique_props.add(i[idx]['modifiedtripleset'][0]['property'])

            string = i[idx]['modifiedtripleset'][0]['subject'] + ' | ' + i[idx]['modifiedtripleset'][0]['property'] + ' | ' + i[idx]['modifiedtripleset'][0]['object']
            string = string.replace('"', '').replace("’", ' ').replace(",", '').replace("_", ' ')  
            triples.append(string)
        
        # joining all mtriples, comma delimited
        input = unidecode((', ').join(triples))


        # processing the target texts
        target_text=[]
        for comment in i[idx]['lexicalisations']:
            if comment['lang'] == 'mt':
                # create entry for each Maltese lexicalisation
                mdata_dct['input_text'].append(input)
                mdata_dct['target_text'].append(unidecode(comment['lex'].replace('"', '').replace("’", ' ').replace(",", '').replace("_", ' ').replace("  ", " ")))

        idx+=1

df1 = pd.DataFrame(unique_props, columns=['properties'])
df1.sort_values('properties')
df1.to_csv('unique_props.csv', index=False)

df2=pd.DataFrame(mdata_dct)
df2.to_csv('webNLG2020_train.csv')


