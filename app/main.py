from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# 🔐 .env에서 OPENAI 키 로드
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# ✅ 벡터 DB 로드
embedding_model = OpenAIEmbeddings()
db = FAISS.load_local(
    "../data/Vector_DB",
    embedding_model,
    allow_dangerous_deserialization=True
)

# ✅ 프롬프트 템플릿
prompt_template = """
너는 요기요 리뷰 데이터를 기반으로 음식점을 추천해주는 AI야.
아래에 제공된 리뷰들을 분석하고, 사용자의 질문에 가장 적합한 음식점 **한 곳만** 추천해줘.
추천 이유도 함께 간결하고 친근하게 설명해줘.
음식점 이름은 반드시 명확히 적어줘.

질문:
{question}

리뷰들:
{context}

추천:
""".strip()

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template
)

# ✅ GPT + RAG 체인 구성
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
    retriever=db.as_retriever(search_kwargs={"k": 10}),
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True
)

# ✅ FastAPI 설정
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 요청 모델 정의
class Question(BaseModel):
    user_id: str
    question: str

# ✅ API 엔드포인트
@app.post("/recommend")
def recommend(q: Question):
    print(f"\n💬 질문 수신 from {q.user_id}: {q.question}")

    try:
        result = qa_chain.invoke({"query": q.question})  # ✅ 최신 방식
        answer = result["result"]  # ✅ 텍스트만 추출

        print(f"✅ 응답 생성 완료:\n{answer}\n")
        return {"recommendation": answer}
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        return {"recommendation": "추천을 처리하는 중 오류가 발생했습니다."}
