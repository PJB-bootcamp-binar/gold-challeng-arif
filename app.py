import streamlit as st
from streamlit_option_menu import option_menu
import os

import re
import string
import pandas as pd

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


# Atur layout page
st.set_page_config(layout='wide')


# Ambil data kamusalay
df_kamusalay = pd.read_csv("new_kamusalay.csv", encoding = 'ISO-8859-1', header=None,index_col=0,squeeze=True)
dict_kamusalay = df_kamusalay.to_dict()

#Ambil data stopword Bahasa Indonesia
df_stopwords = pd.read_csv("stopwordbahasa.csv", encoding = 'ISO-8859-1')
list_stopwords = df_stopwords["stopwordbahasa"].tolist()

# Fuction Cleaning text
def cleansingData(data):
    data = remove_emoji (data)
    data = lowercase (data)
    data = stemming (data)
    data = tokenization (data)
    data = normalization (data)
    data = remove_number (data)
    data = remove_punctuation (data)
    data = stopwords (data)
    data = to_string (data)
    return data

# Menghilangkan karakter emoji
def remove_emoji (data):
    # Remove UTF-8 format emoji 
    data = re.sub(r'\\x[0-9A-Fa-f]{2}', '', data)
    #return data
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', data)
        
# case folding
def lowercase (data):
    data = data.lower()
    return data

# Stemming
def stemming (data) :
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    data = stemmer.stem(data)
    return data

# Tokenization
def tokenization (data) :
    data = data.split()
    return data

# Normalization (Kamus Alay)
def normalization (data) :
    for i in data :
        for key, value in dict_kamusalay.items():
            if key not in data:
                continue
            index = data.index(key)
            data[index] = value
    return data

# Menghilangkan angka
def remove_number (data):
    data = str(data)
    data = re.sub(r'\d+','',data)
    data = data.split() 
    return data

# Menghilangkan Punctuation
def remove_punctuation (data):
    data = str(data)
    data = re.sub('-', ' ', data)
    data = re.sub(r'[^\w\s]', ' ', data)
    data = data.split()
    return data

# Stopwords
def stopwords (data) :
    for i in reversed (data) :
        if i in list_stopwords :
            data.remove(i)
    return data
# List to String
def to_string (data) :
    data = ' '.join(map(str,data))
    return data

# Main Page
st.title ("Cleansing Data Text")

tab1, tab2 = st.tabs(["Input Text", "Upload CSV"])
# Input Text
with tab1:
        
    input_text = st.text_area('Input text', '', height=200)
    output_text = cleansingData(input_text)
    st.markdown('**:blue[Hasil cleansing data text:]**')
    st.write(output_text)
    
# Input CSV
with tab2:
    st.subheader ("Upload File CSV")
    upload_file1 = st.file_uploader ("***File CSV yang diupload harus memiliki attribute atau kolom dengan header 'Tweet'", type = "csv", label_visibility="visible")
    if upload_file1 is not None :
        csv_data_uploaded = pd.read_csv(upload_file1, encoding = 'ISO-8859-1')
     
    clicked = st.button ("Upload And Process")
    if clicked :
        #upload_csv (upload_file1)
        csv_data = pd.DataFrame(csv_data_uploaded["Tweet"])
        csv_data = csv_data[:50]
        for i, row in csv_data.iterrows():
            text_origin = str(csv_data.loc[i,"Tweet"])
            text_clean = cleansingData(text_origin)
            csv_data.loc[i,"Twett clean"] = text_clean
        st.dataframe (csv_data, width=2000, height = 200)
        csv = csv_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='hasil_text.csv',
            mime='text/csv',
        )
