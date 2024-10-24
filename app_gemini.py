import time
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '✨'

st.session_state.chat_id = new_chat_id


st.write('# "🔥🔥🔥"¡hola! :wave: soy firm-bot. Puedo brindar información sobre incendios.🔥🔥🔥"')
st.session_state.messages = []
st.session_state.gemini_history = []
st.session_state.model = genai.GenerativeModel('gemini-pro')
st.session_state.chat = st.session_state.model.start_chat(
    history=st.session_state.gemini_history,
)

for message in st.session_state.messages:
    with st.chat_message(
        name=message['role'],
        avatar=message.get('avatar'),
    ):
        st.markdown(message['content'])

if prompt := st.chat_input('Su consulta aqui...'):
    with st.chat_message('user'):
        st.markdown(prompt)
        st.session_state.messages.append(
            dict(
                role='user',
                content=prompt,
            )
        )
    response = st.session_state.chat.send_message(
        prompt,
        stream=True,
    )
    with st.chat_message(
        name=MODEL_ROLE,
        avatar=AI_AVATAR_ICON,
    ):
        message_placeholder = st.empty()
        full_response = ''
        assistant_response = response
        for chunk in response:
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.05)
                message_placeholder.write(full_response + '▌')
        message_placeholder.write(full_response)

    st.session_state.messages.append(
        dict(
            role=MODEL_ROLE,
            content=st.session_state.chat.history[-1].parts[0].text,
            avatar=AI_AVATAR_ICON,
        )
    )
    st.session_state.gemini_history = st.session_state.chat.history
    