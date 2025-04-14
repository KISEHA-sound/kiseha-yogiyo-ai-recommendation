# test_vectorstore.py

import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# 🔑 환경 변수 로드
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# ✅ 저장된 벡터 DB 불러오기
db = FAISS.load_local(
    "../data/Vector_DB",
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True
)

# 🔍 검색 테스트
query = "최애 치킨 추천해줘"
results = db.similarity_search(query, k=20)  # 원본은 10이지만, 중복 제거할 거니까 더 가져와도 됨

# ✅ 방법 1: 리뷰 텍스트 중복 제거
seen_reviews = set()
unique_results = []
for doc in results:
    if doc.page_content not in seen_reviews:
        seen_reviews.add(doc.page_content)
        unique_results.append(doc)

# 🖨️ 출력
print(f"🔍 유사한 리뷰 Top {len(unique_results)} - 질문: {query}")
for i, doc in enumerate(unique_results, 1):
    print(f"\n[{i}] 매장: {doc.metadata['store']}")
    print(f"리뷰: {doc.page_content}")
