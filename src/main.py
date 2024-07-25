from tkinter.tix import COLUMN
from pyparsing import empty
import streamlit as st
from PIL import Image  # 위에서 선언 후 사용해야한다.
from utils import (
    navigate_to,
    Add_Back_Img
)


def main():
    # TODO : 창 디자인
    # # 창 위에 뜨는 아이
    st.set_page_config(page_title="JOB Advise boT", page_icon="🦈")

    # 레이아웃 구성 방법
    # https://python-programming-diary.tistory.com/137
    empty1, con11, empty2 = st.columns([0.1, 2.5, 0.1])
    empty1, con21, con22, empty2 = st.columns([0.1, 1.25, 1.25, 0.1])
    empty1, con31, con32, empty2 = st.columns([0.1, 1.25, 1.25, 0.1])
    # empty1,con31,empty2 = st.columns([0.1,2.5,0.1])
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
    # Add_Back_Img("배경화면 이미지 링크")
    # main.py
    with empty1:
        empty()  # 여백부분1
    with empty2:
        empty()  # 여백부분2
    with con11:
        # TODO : 꾸미기 사진
        st.image("https://i.imgur.com/W1pEg2c.png", width=500)
        st.markdown(hide_fullscreen_button, unsafe_allow_html=True)
        st.subheader("(⩌⩊⩌)DUR 정보 기반 질의응답 서비스")
        st.write("__□ (。O ⩊ O。)사용자는 DUR 의약품에 관해 궁금한점을 입력합니다!__")
        #st.write("__□ (˶• ﻌ •˶)사용자의 입력을 바탕으로 알맞은 질문을 생성합니다!!__")
        st.write("__□ (๓° ˘ °๓)사용자는 아래와 같은 서비스를 이용할 수 있습니다!!!__")
        #st.write("__□생성된 질문에 대한 힌트 및 답변 피드백 & 꼬리물기 면접 서비스□__")

    with con21:
        img1 = Image.open('web_images/main1.png')
        st.image(img1)
    with con22:
        img2 = Image.open('web_images/main2.png')
        st.image(img2)
        st.subheader("")

    with con31:
        # TODO : 링크 버튼 -> 페이지 이동
        # TODO : 링크 버튼 디자인
        st.link_button("We Are...", url="https://blog.naver.com/t-ave", use_container_width=True)
    with con32:
        # 페이지 이동(resume)
        # TODO : 링크 버튼 디자인
        next_page = st.button("시작하기", use_container_width=True)
        if (next_page):
            # TODO : resume.py
            navigate_to("resume")

    # with con31 :
    #     # TODO : 꾸미기 사진
    #     st.header("# TODO : 하단 이미지 첨부")
    #     # st.web_images("하단 이미지 링크", width = 630)
    #     # st.markdown(hide_fullscreen_button, unsafe_allow_html=True)
