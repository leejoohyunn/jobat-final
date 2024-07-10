import streamlit as st
from utils import (
    navigate_to,
    Add_Back_Img
)

import streamlit as st
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory



# 스트리밍 해주는 함수
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)




# 이전 대화기록을 출력해 주는 코드
# role : user, assistant
# message : 대화내용
# def print_messages():
#     if "messages" in st.session_state and len(st.session_state["messages"])>0:
#         for role, message in st.session_state["messages"]:
#             st.chat_message(role).write(message)

def print_messages():
    if "messages" in st.session_state and len(st.session_state["messages"])>0:
        for chat_message in st.session_state["messages"]:
            st.chat_message(chat_message.role).write(chat_message.content)



def interview():
    # 창 위에 뜨는 아이
    st.set_page_config(page_title="ChatGPT",page_icon="🦈")
    st.title("🦈 JOB AT")

    if "cnt" not in st.session_state:
        st.session_state.cnt = 0

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # streamlit으로 구현을 하면 채팅 입력할 때마다 코드가 처음부터 끝까지 다시 실행됨
    # 대화기록을 state에 넣어서 캐싱해준다.
    # 채팅 대화기록을 저장하는 store 세션 상태 변수
    if "store" not in st.session_state:
        st.session_state["store"] = dict()

    # 이전 대화기록을 출력해 주는 코드
    print_messages()

    # 세션  ID를 기반으로 세션 기록을 가져오는 함수
    def get_session_history(session_ids:str)->BaseChatMessageHistory:
        # print(session_ids)
        if session_ids not in st.session_state["store"]:    # 세션 ID가 store에 없는 경우
            # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
            st.session_state["store"][session_ids] = ChatMessageHistory()
        return st.session_state["store"][session_ids]


    # 유저 입력이 있을때 유저 입력을 보여준다.
    if user_input:= st.chat_input("유저가 메세지 입력"):
        # 사용자가 입력한 내용
        st.chat_message("user").write(f"{user_input}")
        # st.session_state["messages"].append(("user", user_input))
        st.session_state["messages"].append(ChatMessage(role="user", content=user_input))

        # # LLM 을 사용하여 AI답변을 생성
        # prompt = ChatPromptTemplate.from_template(
        #     """질문에 대하여 간결하게 답변해 주세요.
        #     {question}
        #     """
        # )

        # chain = prompt | ChatOpenAI()
        # response = chain.invoke({"question": user_input})
        # msg = response.content

        # chain = prompt | ChatOpenAI() | StrOutputParser()
        # msg = chain.invoke({"question": user_input})


        # AI의 답변
        with st.chat_message("assistant"):    # "assistant" : streamlit이 말함
            # StreamHandler : 토큰 하나하나를 준다.
            stream_handler = StreamHandler(st.empty())
            # 1. 모델 생성
            llm = ChatOpenAI(streaming=True, callbacks=[stream_handler])

            # 2. 프롬프트 생성
            # 중간에 대화기록이 들어가야 하기 때문에 ChatPromptTemplate.from_messages를 사용
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "질문에 짧고 간결하게 답변해 주세요.",
                    ),
                    # 대화 기록을 변수로 사용, history가 MessageHistory 의 key 가 됨
                    MessagesPlaceholder(variable_name="history"),
                    ("human", "{question}"),   # 사용자 질문을 입력
                ]
            )

            chain = prompt | llm   # 프롬프트와 모델을 연결하여 runnable 객체 생성

            chain_with_memory = (
                RunnableWithMessageHistory( # RunnableWithMessageHistory 객체 생성
                    chain,   # 생성할 Runnable 객체
                    get_session_history,    # 세션 기록을 가져오는 함수
                    input_messages_key="question", # 사용자 질문의 키
                    history_messages_key="history", # 기록 메시지의 키
                )
            )

            response = chain_with_memory.invoke(
                {"question":user_input},
                # 세션 ID를 설정 
                config={"configurable":{"session_id":session_id}},
            )
            msg = response.content
            # msg = "당신이 입력한 내용: {user_input}"
            # st.write(msg)
            # st.session_state["messages"].append(("assistant", msg))
            st.session_state["messages"].append(
                ChatMessage(role="assistant", content=msg)
            )
            st.session_state.cnt += 1


    with st.sidebar:
        main = st.button("Home 화면", use_container_width=True)
        if(main):
            navigate_to("main")
        prev = st.button("질문 다시 보기", use_container_width=True)
        if(prev):
            navigate_to("view_question")


