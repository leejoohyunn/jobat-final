#######################################
####  very very bad coding style   ####
#######################################
from tkinter.tix import COLUMN
from pyparsing import empty
import streamlit as st
import copy
from utils import (
    navigate_to,
    crawl_data,
    Add_Back_Img
)

def dataframe_to_string(df_info):
    if not df_info.empty:
        jd_text = ""
        if '포지션 상세' in df_info.columns:
            jd_text += "포지션 상세 :"
            for item in df_info['포지션 상세']:
                jd_text += " " + item

        if '주요업무' in df_info.columns:
            jd_text += "주요업무 :"
            for item in df_info['주요업무']:
                jd_text += " " + item

        if '자격요건' in df_info.columns:
            jd_text += "자격요건 :"
            for item in df_info['자격요건']:
                jd_text += " " + item

        return jd_text
    else:
        return ""

            


def resume():
    # 창 위에 뜨는 아이
    st.set_page_config(page_title="Resume",page_icon="🦈")
    st.subheader("🦈 이력서 및 채용공고에 대한 정보를 입력해주세요")
    st.subheader(" ")


    # 이력서를 입력하는데 창 크기를 사용자가 집적 늘려야함...
    # 더 찾아보는중...(그래서 pdf로 이력서를 입력받는거같기도하고)


    # 사용자의 입력인 세션 변수 resume 생성
    if "resume" not in st.session_state:
        st.session_state.resume = ""

    if "url_to_type" not in st.session_state:
        st.session_state.url_to_type = False
    if "prev_url_to_type" not in st.session_state:
        st.session_state.prev_url_to_type = False

    if "jd" not in st.session_state:
        st.session_state.jd = ""

    if "no_resume" not in st.session_state:
        st.session_state.no_resume = False
    if "prev_no_resume" not in st.session_state:
        st.session_state.prev_no_resume = False
    if "no_jd" not in st.session_state:
        st.session_state.no_jd = False
    if "prev_no_jd" not in st.session_state:
        st.session_state.prev_no_jd = False





    # 이력서 입력
    st.subheader("이력서를 입력해 주세요")
    resume = st.text_area('',max_chars=4000)
    st.session_state.resume = resume





    st.subheader("TODO: url 입력 어떻게 하는지 설명창 만들어야함")





    # 채용공고 입력 URL and typing
    if st.session_state.url_to_type == True:
        st.subheader(" "), st.subheader("직접 채용공고 입력해!")
        if(st.button("url로 채용공고 입력하기")):
            st.session_state.url_to_type = False
        # 채용공고 직접 넣는 부분.
        jd = st.text_area('TODO : 직접 채용공고에 대한 내용을 넣거나, 원티드 공고 url을 넣는 부분',max_chars=1200)


    elif st.session_state.url_to_type == False:
        st.subheader(" "), st.subheader("url로 채용공고 자동 입력")
        if(st.button("직접 채용공고 입력하기")):
            st.session_state.url_to_type = True
        # 채용공고 url 입력
        url = st.text_input('url을 복사해서 입력해주세요')
        toggle = st.toggle("자동으로 입력된 채용공고 보기")
        
        if st.session_state.url_to_type == False:
            if url:
                if(toggle):
                    df_info = crawl_data(url)
                    st.write(df_info.head())  # 데이터프레임의 처음 몇 줄 출력
                    if not df_info.empty:
                        st.title("포지션 상세")
                        if '포지션 상세' in df_info.columns:
                            st.session_state["jd"] += "포지션 상세 :"
                            for item in df_info['포지션 상세']:
                                st.write(item)
                                st.session_state["jd"] += " " + item
                        else:
                            st.write("포지션 상세 데이터가 없습니다.")

                        st.title("주요업무")
                        if '주요업무' in df_info.columns:
                            st.session_state["jd"] += "주요업무 :"
                            for item in df_info['주요업무']:
                                st.write(item)
                                st.session_state["jd"] += " " + item
                        else:
                            st.write("주요업무 데이터가 없습니다.")

                        st.title("자격요건")
                        if '자격요건' in df_info.columns:
                            st.session_state["jd"] += "자격요건 :"
                            for item in df_info['자격요건']:
                                st.write(item)
                                st.session_state["jd"] += " " + item
                        else:
                            st.write("자격요건 데이터가 없습니다.")
                    else:
                        st.write("url을 재입력 후 버튼을 다시 눌러주세요")








    # 페이지 리셋
    if st.session_state.url_to_type != st.session_state.prev_url_to_type:
        a = st.session_state["url_to_type"]
        st.session_state.prev_url_to_type = a
        navigate_to("resume")



    # 레이아웃
    con11,con12 = st.columns([1.25,1.25])

    with con11 :
        main = st.button("Home 화면", use_container_width=True)
        if(main): navigate_to("main")

    with con12 :
        # 면접 질문 생성 버튼 클릭 시 세션 상태에 입력된 텍스트 저장
        gen_question = st.button("면접 질문 생성", use_container_width=True)
        if gen_question:
            st.session_state.resume = resume
            
            if st.session_state["url_to_type"]==False: 
                jd = crawl_data(url)
                st.session_state.jd = dataframe_to_string(jd)
            else: st.session_state.jd = jd
            

            # 입력 안하면 다음으로 안넘어가게 했다.
            if st.session_state.resume == "": st.session_state.no_resume = True
            else: st.session_state.no_resume = False
            

            if st.session_state.jd == "": st.session_state.no_jd = True
            else: st.session_state.no_jd = False            
            

            if st.session_state.resume == "" or st.session_state.jd == "": None
            else: navigate_to("loading_question")






    # 몰랐는데 bool 타입 변수는 일반적인 변수랑 다르게 카피할 필요 없다네요?,,, 
    if st.session_state.no_resume==True:
        st.write("""
        <div style="text-align: center;">
            <h2>이력서를 입력해 주세요</h2>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state['no_resume'] != st.session_state['prev_no_resume']:
            st.session_state['prev_no_resume'] = st.session_state['no_resume']
            if gen_question:
                navigate_to("resume")
    else:
        None

    if st.session_state.no_jd==True:
        st.write("""
        <div style="text-align: center;">
            <h2>채용공고를 입력해 주세요</h2>
        </div>
        """, unsafe_allow_html=True)
        if st.session_state['no_jd'] != st.session_state['prev_no_jd']:
            st.session_state['prev_no_jd'] = st.session_state['no_jd']
            if gen_question:
                navigate_to("resume")
    else:
        None