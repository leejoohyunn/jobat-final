import re

import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import numpy as np

from langchain_core.callbacks.base import BaseCallbackHandler


#####################
###  페이지 전환   ###
#####################
def navigate_to(page):
    st.session_state.page = page  # session_state["page"]에 값 할당
    main = st.empty()
    main.empty()
    time.sleep(.2)  # Bug workaround to enforce main.empty()
    st.experimental_rerun()  # 페이지 새로 고침


#####################
###    배경화면    ###
#####################
def Add_Back_Img(Image_link):
    # https://velog.io/@sjy1410/streamlit-%EB%B0%B0%EA%B2%BD%EC%82%AC%EC%A7%84-%EB%84%A3%EB%8A%94-%EB%B2%95
    # streamlit은 폴더 내부 사진의 경로를 읽을 수가 없어
    # 사진을 호스팅 한다음 그 사진의 링크를 불러와야한다.
    # background-image: url("사진의 링크")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{Image_link}");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


#####################
### 1..           ###
### 2..           ###
### 3..           ###
### 이런식으로 표현된 문장을 리스트로 분할
#####################
def split_questions(text):
    # 정규식을 이용해 숫자와 점을 제거하고 문자열을 나눔
    sentences = re.sub(r'\d+\.\s*', '', text).strip().split('\n')

    # 빈 문자열 제거
    sentences = [sentence for sentence in sentences if sentence]

    # 결과 출력
    return sentences


# 임베딩...
def init_model():
    from langchain_openai import ChatOpenAI

    MODEL_NAME = 'gpt-3.5-turbo'
    return ChatOpenAI(model=MODEL_NAME, temperature=0.5)


def embed_text(text: str):
    from langchain_community.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma

    chunks = split_text(text)
    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
    docs = Chroma.from_texts(chunks, embeddings)
    return docs


def split_text(text: str):
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_text(text)


def summarize_job_openings(job_openings):
    from langchain import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    llm = init_model()
    template = '''
    You are an expert AI researcher. Extract the essentials from a given job posting.
    Please answer as Korean, and formatted as a paragraph.

    Paragraph: {paragraph}
    '''

    prompt = PromptTemplate.from_template(template=template)

    summarize_chain = prompt | llm | StrOutputParser()
    return summarize_chain.invoke(dict(paragraph=job_openings))


def mk_questions(context, vector_db):
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain import PromptTemplate
    from langchain.chains import create_retrieval_chain
    from langchain_core.output_parsers import CommaSeparatedListOutputParser

    output_parser = CommaSeparatedListOutputParser()
    format_instructions = output_parser.get_format_instructions()

    template = '''
    You are an expert AI interviewer.
    Use the given context to generate 10 different predictive interview questions in Korean.
    Order your questions to match the interview scenario.
    Please only generate the questions, don't add any explanations.

    <context>
    {context}
    </context>

    {format_instructions}
    '''

    prompt = PromptTemplate(
        template=template,
        input_variables=["context"],
        partial_variables={"format_instructions": format_instructions},
    )

    llm = init_model()

    # print(prompt)

    qa_chain = create_stuff_documents_chain(llm, prompt)

    retriever = vector_db.as_retriever(
        search_type='similarity',
        search_kwargs={
            'k': 3,  # Select top k search results
        }
    )

    rag_chain = create_retrieval_chain(retriever, qa_chain)

    return rag_chain.invoke(dict(input=context))


#################################################
# 크롤링
def crawl_data(link):
    def scroll_down(driver):
        last_height = driver.execute_script("return document.body.scrollHeight")

        for i in range(1):
            # 스크롤을 페이지 아래로 내립니다.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # 페이지 로드를 기다립니다.
            time.sleep(0.5)

            # 새로운 높이를 계산하고 이전 높이와 비교합니다.
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    ### Chrome 브라우저를 설정하고 실행합니다. ###
    # 로컬
    # driver = webdriver.Chrome()

    # ec2
    # driver_path = '/usr/bin/chromedriver'
    # driver = webdriver.Chrome(driver_path)

    # from selenium import webdriver
    # from selenium.webdriver.chrome.service import Service
    # from webdriver_manager.chrome import ChromeDriverManager
    # from selenium.webdriver.chrome.options import Options
    # import time
    # from selenium.webdriver.common.by import By
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 브라우저를 머리 없는 모드로 실행하려면 주석을 해제하세요.
    #
    # # Service 객체를 사용하여 ChromeDriverManager를 통해 경로를 설정합니다.
    # service = Service(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=service, options=chrome_options)

    from pyvirtualdisplay import Display
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    driver_options = webdriver.ChromeOptions()

    # 헤드리스 옵션 사용 여부
    driver_options.add_argument("headless")

    # 가상 웹브라우저 설정
    display = Display(visible=0, size=(1024, 768))

    # 가상 웹브라우저 실행
    display.start()

    # 하드웨어 가속 사용 여부
    driver_options.add_argument("disable-gpu")

    # 사용 언어
    driver_options.add_argument("lang=ko_KR")

    service = Service(ChromeDriverManager.install())

    # 드라이버 생성
    driver = webdriver.Chrome(service=service, options=driver_options)



    info_list = []
    try:
        # 페이지로 이동
        driver.get(link)
        time.sleep(0.5)  # 페이지가 로드될 때까지 대기 (필요에 따라 조정)

        scroll_down(driver)

        # 버튼 클릭
        try:
            button = driver.find_element(By.XPATH,
                                         '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/button')
            driver.execute_script("arguments[0].click();", button)
            time.sleep(0.5)  # 클릭 후 페이지가 로드될 때까지 대기 (필요에 따라 조정)
        except NoSuchElementException:
            pass  # 버튼을 찾지 못한 경우에는 그냥 넘어갑니다

        # 필요한 정보들을 가져옵니다.
        try:
            company_element = driver.find_element(By.XPATH, '//*[@data-attribute-id="company__click"]')
            company_name = company_element.get_attribute('data-company-name')
        except (NoSuchElementException, TimeoutException):
            company_name = ''

        try:
            location = driver.find_element(By.XPATH,
                                           '//*[@id="__next"]/main/div[1]/div/section/header/div/div[1]/span[2]').text
        except (NoSuchElementException, TimeoutException):
            location = ''

        try:
            year = driver.find_element(By.XPATH,
                                       '//*[@id="__next"]/main/div[1]/div/section/header/div/div[1]/span[4]').text
        except (NoSuchElementException, TimeoutException):
            year = ''

        try:
            job = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/header/h1').text
        except (NoSuchElementException, TimeoutException):
            job = ''

        try:
            about_position = driver.find_element(By.XPATH,
                                                 '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/p').text
        except (NoSuchElementException, TimeoutException):
            about_position = ''

        try:
            about_work = driver.find_element(By.XPATH,
                                             '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[1]/p').text
        except (NoSuchElementException, TimeoutException):
            about_work = ''

        try:
            about_who = driver.find_element(By.XPATH,
                                            '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[2]/p').text
        except (NoSuchElementException, TimeoutException):
            about_who = ''

        try:
            about_better = driver.find_element(By.XPATH,
                                               '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[3]/p').text
        except (NoSuchElementException, TimeoutException):
            about_better = ''

        try:
            about_good = driver.find_element(By.XPATH,
                                             '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[4]/p').text
        except (NoSuchElementException, TimeoutException):
            about_good = ''

        # 기술스택과 태그를 가져오는데 있어서 예외 처리 추가
        try:
            if driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[3]/ul'):
                tags_xpath = '//*[@id="__next"]/main/div[1]/div/section/section/article[3]/ul'
                tool_xpath = '//*[@id="__next"]/main/div[1]/div/section/section/article[2]/ul'
        except NoSuchElementException:
            tags_xpath = '//*[@id="__next"]/main/div[1]/div/section/section/article[2]/ul'
            tool_xpath = ''

        # 기술스택 가져오기
        try:
            if tool_xpath:
                tool_element = driver.find_element(By.XPATH, tool_xpath)
                tool = tool_element.text
            else:
                tool = ''
        except NoSuchElementException:
            tool = ''

        # 태그 가져오기
        try:
            tags_element = driver.find_element(By.XPATH, tags_xpath)
            tags = tags_element.text
        except NoSuchElementException:
            tags = ''

        try:
            date = driver.find_element(By.XPATH,
                                       '//*[@id="__next"]/main/div[1]/div/section/section/article[3]/span').text
        except (NoSuchElementException, TimeoutException):
            date = ''

            # 정보를 info_list에 추가합니다.
        info_list.append({'link': link, '회사명': company_name, '지역': location, '경력': year, '직무': job,
                          '포지션 상세': about_position, '주요업무': about_work,
                          '자격요건': about_who, '우대사항': about_better, '혜택 및 복지': about_good,
                          '기술스택/툴': tool, '태그': tags, '마감일': date})

        print(f"{job} 정보 수집 완료")

    except Exception as e:
        print(f"Error processing {link}: {str(e)}")

    # WebDriver 종료
    driver.quit()

    df_info = pd.DataFrame(info_list)
    return df_info
#################################################