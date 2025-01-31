import os 
import streamlit as st
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


##### available models
# models = genai.list_models()
# for model in models:
#   print(model.name)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def get_gemini_response(question):
  response = chat.send_message(question, stream=True)
  return response

##streamlit app
st.set_page_config(page_title="QA chatbot")
st.header("Gemini LLM Application")

# Initialize ssssion state for chat history if it does not exist

if 'chat-history' not in st.session_state:
  st.session_state['chat-history'] = []

input = st.text_input("Input: ",key='Input')
submit = st.button("Ask the question") 

if submit and input:
  response = get_gemini_response(input)

  # add user query and response to session history
  st.session_state['chat-history'].append(('You',input))
  st.subheader('The Response is') 

  for chunk in response:
    st.write(chunk.text)
    st.session_state['chat-history'].append(('Bot',chunk.text))
st.subheader("The Response is:")

for role,text in st.session_state['chat-history']:
  st.write(f'{role}:{text}')




