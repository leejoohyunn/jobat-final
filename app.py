from tkinter.tix import COLUMN
from pyparsing import empty
import streamlit as st


# my fuction
from utils import (
    Add_Back_Img
)

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

if st.session_state.page == "interview":
    interview()

