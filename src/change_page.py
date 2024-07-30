import streamlit as st
from utils import (
    navigate_to,
    crawl_data,
    Add_Back_Img
)

def change_page():
    # Title for the main page
    #st.title('메인 메뉴 돌아가기')
    # Central buttons
    #st.write('\n')  # Add some space before buttons
    #st.write('### 선택해주세요:')  # Header for buttons section

    # CSS to increase button size
    st.markdown("""
        <style>
        .big-button {
            font-size: 20px !important;
            height: 3em;
            width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Button for 금기사항 물어보기
    if st.button('금기사항 물어보기', key='button1'):
        st.write('금기사항 관련 페이지로 이동합니다.')
        navigate_to("chat")  # 실제 네비게이션 함수 호출

    # Button for 의약품 정보 물어보기
    if st.button('의약품 정보 물어보기', key='button2'):
        st.write('의약품 정보 관련 페이지로 이동합니다.')
        navigate_to("chat")  # 실제 네비게이션 함수 호출

    # Sidebar with navigation button
    st.sidebar.title('메뉴')
    if st.sidebar.button('메인으로 돌아가기'):
        st.write('메인 페이지로 돌아갑니다.')
        # 실제 네비게이션 코드 삽입 가능
