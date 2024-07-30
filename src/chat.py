import openai
import streamlit as st
from streamlit_chat import message
from utils import (
    navigate_to,
    crawl_data,
    Add_Back_Img
)

# Streamlit의 secrets 기능을 사용하여 API 키 로드
openai.api_key = st.secrets["OPENAI_API_KEY"]

# OpenAI 클라이언트 인스턴스 생성
client = openai.OpenAI(api_key=openai.api_key)

def generate_response(prompt):
    try:
        # 챗 완성 요청
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        # 응답에서 메시지 내용 추출
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        return f"Error: {str(e)}"
def chat():
    st.header("DUR Chat Bot(Demo)")

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    with st.form('form', clear_on_submit=True):
        user_input = st.text_input('사용자: ', '', key='input')
        submitted = st.form_submit_button('제출')

    if submitted and user_input:
        output = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
