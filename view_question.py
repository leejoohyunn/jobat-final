import streamlit as st
from utils import (
    navigate_to,
    Add_Back_Img
)

from langchain_openai import ChatOpenAI
from langchain import PromptTemplate


def feedback(question, ask):
    prompt = PromptTemplate.from_template(
        template="""
        당신은 면접을 피드백해주는 adviser입니다.
        {question} 은 면접 질문입니다.
        {ask} 은 면접 질문에 대한 답변입니다.

        답변을 읽고, 당신이 판단하기에 나쁜점 혹은 수정해야 할 부분이 있다면 지적해주고 부가 설명을 해주세요.

        만약 면접 질문과 상관없는 답변이라면 반드시 지적해 주세요.

        당신의 답변은 한문단 이내여야 하며 한국어로 해주세요.
        """
    )

    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.1)
    chain = prompt | llm

    feedback = chain.invoke({"question": question, "ask": ask})
    return feedback.content


def view_question():
    st.set_page_config(page_title="Interview Question", page_icon="🦈")
    st.title("🦈 JOB AT's 예상 면접 질문")

    print('\n', "*" * 20)
    print("questions = st.session_state.questions \n", st.session_state.questions)
    print("*" * 20, '\n')

    questions = st.session_state.questions
    hint_list = st.session_state.hint_list

    for i in range(len(questions)):
        with st.expander(questions[i]):
            ask = st.text_area('__질문에 대한 답변을 해보세요!__', key=f"input_{i}")

            # TODO : 답변에 대한 피드백 생성
            if (st.button('피드백 받기', key=f"feedback_{i}")):
                st.write(feedback(questions[i], ask))

            if (st.button('Hint 받기', key=f"hint_{i}")):
                st.write(hint_list[i])

    con11, con12 = st.columns([1.25, 1.25])
    with con11:
        main = st.button("Home 화면", use_container_width=True)
        if (main):
            st.session_state.clear()
            navigate_to("main")
    with con12:
        prev = st.button("모의 면접 서비스", use_container_width=True)
        if (prev):
            navigate_to("interview")