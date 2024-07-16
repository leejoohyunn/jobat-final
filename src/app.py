from tkinter.tix import COLUMN
from pyparsing import empty
import streamlit as st



# page
from main import main
from resume import resume
from loading_question import loading_question
from view_question import view_question
from interview import interview

# page 전환을 위한 session_state.page 생성
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# page 전환
if st.session_state.page == "main":
    main()

if st.session_state.page == "resume":
    resume()

if st.session_state.page == "loading_question":
    loading_question()

if st.session_state.page == "view_question":
    view_question()
    print('\n', "*"*20)
    print("view_question() 성공")
    print("*" * 20, '\n')

if st.session_state.page == "interview":
    interview()