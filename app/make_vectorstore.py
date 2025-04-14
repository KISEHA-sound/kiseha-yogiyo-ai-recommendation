# make_vectorstore.py

import os
import json
from glob import glob
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# 🔑 .env에서 API 키 로드
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# 📂 JSON 파일들 전부 불러오기 (정렬: 숫자 기준)
json_files = sorted(
    glob("../data/DB/yogiyo_reviews_result1_*.json"),
    key=lambda x: int(x.split("_")[-1].split(".")[0])
)

print(f"📁 JSON 파일 수: {len(json_files)}")

# 📄 리뷰들 하나의 리스트로 통합
all_reviews = []
for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        all_reviews.extend(data)

print(f"📄 총 리뷰 원본 개수: {len(all_reviews)}")

# 📚 LangChain Document로 변환 (빈 리뷰 제거)
documents = [
    Document(page_content=review["review"].strip(), metadata={"store": review["store"]})
    for review in all_reviews
    if review.get("review") and review["review"].strip()
]

print(f"📝 유효한 리뷰 개수 (빈 값 제거 후): {len(documents)}")

# 📏 텍스트 나누기
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
split_docs = splitter.split_documents(documents)

print(f"📦 벡터화할 텍스트 청크 개수: {len(split_docs)}")

# 🧠 임베딩 & 벡터 DB 생성
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(split_docs, embeddings)

# 💾 저장 경로 생성
save_path = "../data/Vector_DB"
os.makedirs(save_path, exist_ok=True)

# 💾 저장
db.save_local(save_path)
print("✅ 벡터 DB 생성 완료! 저장 위치:", save_path)
