import streamlit as st
from googletrans import Translator
import time
import google.generativeai as genai
import os

os.environ['GOOGLE_API_KEY'] = 'AIzaSyCvobvQwSkcw2UgTAvV_ziY3GPHuqkFJrw'
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')


@st.cache_data
def update_chat_history(chat_history, role, text):
    chat_history.append((role, text))
    return chat_history

def translate_to_english(text):
    translator = Translator()
    translated_text = translator.translate(text, src='ta', dest='en')
    return translated_text.text
    
def translate_to_tamil(text):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='ta')
    return translated_text.text

def tamil_chatbot(input_text):
    translator = Translator()
    response = model.generate_content(translate_to_english(input_text))
    response_text = []
    for chunk in response:
        translation = translator.translate(chunk.text, dest='ta')
        response_text.append(translation.text)
    return response_text

def main():
    st.title('தமிழில் கேளுங்கள் (Tamizh Chatbot)')

    input_text = st.text_input('வாங்க பழகலாம்:')
    
    submit_button = st.button('Submit')

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history']=[]
    
    
    st.sidebar.title('Chat History: ')
    for role, text in st.session_state['chat_history']:
        st.sidebar.write(f'{role}: {text}')
        
    if submit_button and input_text:
        st.empty()
        with st.spinner(text='Processing...'):
            time.sleep(15)
        response_text = tamil_chatbot(input_text)
        
        if input_text.strip():
            st.session_state['chat_history'] = update_chat_history(st.session_state['chat_history'], 'You', input_text)
        
        st.header('Response:')
        
       
        for word in response_text:
            st.write(word)
            st.session_state['chat_history'] = update_chat_history(st.session_state['chat_history'], 'Bot', word)

        input_text=''

if __name__ == '__main__':
    main()
