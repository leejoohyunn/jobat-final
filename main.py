from tkinter.tix import COLUMN
from pyparsing import empty
import streamlit as st
from utils import (
    navigate_to,
    Add_Back_Img
)

def main():
    # TODO : 창 디자인
    # # 창 위에 뜨는 아이
    st.set_page_config(page_title="JOB Advise boT",page_icon="🦈")
    
    # 레이아웃 구성 방법
    # https://python-programming-diary.tistory.com/137
    empty1,con11,empty2 = st.columns([0.1,2.5,0.1])
    empty1,con21,con22,empty2 = st.columns([0.1,1.25,1.25,0.1])
    empty1,con31,empty2 = st.columns([0.1,2.5,0.1])
    hide_fullscreen_button = """
    <style>
    button[title="View fullscreen"] {
        display: none;
    }
    [data-testid="StyledFullScreenButton"] {
        display: none;
    }
    </style>
    """
    # TODO : 배경화면
    # Add_Back_Img("배경화면 이미지 링크")
    # main.py
    with empty1 :
        empty() # 여백부분1
    with empty2 :
        empty() # 여백부분2   
    with con11 : 
        # TODO : 꾸미기 사진
        st.image("https://i.imgur.com/W1pEg2c.png", width = 630)
        st.markdown(hide_fullscreen_button, unsafe_allow_html=True)
        st.subheader(":🦈 이력서기반 모의 면접 서비스 🦈:")
        st.write("- 1. 사용자는 자기소개서를 입력합니다.")
        st.write("- 2. 사용자의 자기소개서를 바탕으로 면접 질문을 생성합니다.")
        st.write("- 3. 사용자는 아래와 같은 서비스를 이용할 수 있습니다.")
        with st.expander("TODO : 설명"):
            st.write("TODO : 설명")


    with con21 :
        # TODO : 링크 버튼 -> 페이지 이동
        # TODO : 링크 버튼 디자인
        st.link_button("We Are...", url = "https://blog.naver.com/t-ave", use_container_width=True)
    with con22 :
        # 페이지 이동(resume)
        # TODO : 링크 버튼 디자인
        next_page = st.button("시작하기", use_container_width=True)
        if(next_page):
            # TODO : resume.py
            navigate_to("resume")

    with con31 :
        # TODO : 꾸미기 사진
        st.header("# TODO : 하단 이미지 첨부")
        # st.image("하단 이미지 링크", width = 630)
        # st.markdown(hide_fullscreen_button, unsafe_allow_html=True)