import time

import re

import streamlit as st
import hydralit_components as hc
from utils import *


from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_core.output_parsers import CommaSeparatedListOutputParser





# 로딩 창에서 JOB AT의 팁을 보여주면서 동시에 면접 질문 생성과 생성된 질문에 대한 Hint를 생성



def loading_question():
    job_postings =  st.session_state.jd
    user_resume = st.session_state.resume

    if "hint_list" not in st.session_state:
        st.session_state.hint_list = None

    context = summarize_job_openings(job_postings)

    
    # # 팁 생성기
    # tip_prompt = PromptTemplate.from_template(
    #     template = """
    #     너는 매우 친절한 adviser입니다.
    #     {context} 해당 분야의 면접을 보러 갈때 팁을 문장으로 생성해주세요.

    #     아래와 같은 형식으로 대답해주세요.
        
    #     1...
    #     2...
    #     3...
        
    #     위의 형식 외의 대답이나 추가적인 설명은 하지 마세요
    #     """
    # )

    
    tip_llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=1.0)
    # tip_chain = tip_prompt | tip_llm

    # hint 생성기
    hint_prompt = PromptTemplate.from_template(
        template = """
        당신은 매우 친절한 adviser입니다.
        {questions} 를 읽고 해당 질문에 대한 면접 대답 힌트를 한문단으로 생성해주세요
        """
    )
    
    hint_chain = hint_prompt | tip_llm

    st.title("질문을 생성 중입니다.")
    with hc.HyLoader('',hc.Loaders.pulse_bars,):
        # tip = tip_chain.invoke({"context" : context})
        # if(tip):
        #     st.header("🦈JOB Advise boT's TIP🦈")
        #     st.write(tip.content)

        vector_db = embed_text(user_resume)
        question_list = mk_questions(context, vector_db)


        text = question_list['answer']
        questions = re.findall(r'\d+\.\s(.+?)(?=\n\d+\.|$)', text, re.DOTALL)

        st.session_state.questions = questions
        hint_list = []

        for i in range(len(st.session_state.questions)):
            questions = st.session_state.questions
            hint = hint_chain.invoke({questions[i]})
            hint_list.append(hint.content)
            
        st.session_state.hint_list = hint_list


    navigate_to("view_question")




