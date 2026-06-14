import streamlit as st
import uuid
from agent import chat
from memory import init_db, get_history, get_profile

st.set_page_config(page_title='Emergency Preparedness Guide', page_icon='🚨', layout='wide')
init_db()

if 'student_id' not in st.session_state:
    st.session_state.student_id = str(uuid.uuid4())[:8]
if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'assistant', 'content': 'Hi! I am your Emergency Preparedness Assistant. Tell me your city and housing type (hostel, PG, apartment) and I will help you stay safe during any disaster!'}]
if 'reflection' not in st.session_state:
    st.session_state.reflection = ''
if 'quick' not in st.session_state:
    st.session_state.quick = ''

with st.sidebar:
    st.title('Emergency Guide')
    st.caption(f"Session: {st.session_state.student_id}")
    st.divider()
    st.subheader('Quick Actions')
    if st.button('Fire Safety'):
        st.session_state.quick = 'Give me a fire safety checklist'
    if st.button('Flood Preparedness'):
        st.session_state.quick = 'How do I prepare for floods?'
    if st.button('Earthquake Safety'):
        st.session_state.quick = 'Give me an earthquake preparedness checklist'
    if st.button('Cyclone Safety'):
        st.session_state.quick = 'What should I do to prepare for a cyclone?'
    if st.button('Emergency Numbers'):
        st.session_state.quick = 'What are the emergency numbers in Bangalore?'
    st.divider()
    profile = get_profile(st.session_state.student_id)
    if profile:
        st.subheader('Your Profile')
        st.write(f"Location: {profile.get('location','N/A').title()}")
        st.write(f"Housing: {profile.get('housing_type','N/A').title()}")
    if st.button('Conversation History'):
        history = get_history(st.session_state.student_id, limit=20)
        if history:
            for role, msg in history:
                st.write(f'{role.title()}: {msg}')
        else:
            st.info('No history yet.')
    if st.session_state.reflection:
        st.divider()
        st.subheader('Agent Reflection')
        st.info(st.session_state.reflection)

st.title('Emergency Preparedness Guide for Students')
st.caption('AI-powered | Memory | Reflection | Replanning')
st.divider()

for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

def handle_message(user_input):
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.write(user_input)
    with st.chat_message('assistant'):
        with st.spinner('Thinking...'):
            history = [(m['role'], m['content']) for m in st.session_state.messages]
            response, reflection = chat(st.session_state.student_id, user_input, history)
        st.write(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
    if reflection:
        st.session_state.reflection = reflection

if st.session_state.quick:
    quick = st.session_state.quick
    st.session_state.quick = ''
    handle_message(quick)
    st.rerun()

if prompt := st.chat_input('Ask me anything about emergency preparedness...'):
    handle_message(prompt)
    st.rerun()
