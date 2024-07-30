import streamlit as st
from utils import (
    navigate_to,
    crawl_data,
    Add_Back_Img
)

def change_page():
    # Title for the main page
    st.title('메인 페이지')
    # Central buttons
    st.write('\n')  # Add some space before buttons
    st.write('### 선택해주세요:')  # Header for buttons section

    # Define two central buttons with some spacing in between
    col1, col2 = st.columns([1, 1])

    with col1:
        next_page = st.button('금기사항 물어보기')
        if (next_page):
            navigate_to("chat")
        #if st.button('금기사항 물어보기'):
        #st.write('금기사항 관련 페이지로 이동합니다.')
        #navigate_to("chat.py")
        # chat.py로 이동하는 코드
        # st.experimental_rerun() 사용 시, 선택적 리다이렉션 구현 가능

    with col2:
        the_next_page = st.button('의약품 정보 물어보기')
        if (the_next_page):
            navigate_to("chat")
   # if st.button('의약품 정보 물어보기'):
    #    st.write('의약품 정보 관련 페이지로 이동합니다.')
        # chat.py로 이동하는 코드
        # st.experimental_rerun() 사용 시, 선택적 리다이렉션 구현 가능

# Sidebar with navigation button
    st.sidebar.title('메뉴')
    if st.sidebar.button('메인으로 돌아가기'):
        # main.py로 돌아가는 코드
    # st.experimental_rerun() 사용 시, 선택적 리다이렉션 구현 가능
        st.write('메인 페이지로 돌아갑니다.')
