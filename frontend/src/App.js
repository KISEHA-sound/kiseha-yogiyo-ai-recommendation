import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState("");
  const [count, setCount] = useState(0);
  const LIMIT = 10;

  const ask = async () => {
    if (count >= LIMIT) return;
    const res = await axios.post("http://localhost:8000/recommend", {
      user_id: "neo",
      question
    });
    setResult(res.data.recommendation);
    setCount(prev => prev + 1);
  };

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#fff0f5',
      fontFamily: 'sans-serif',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      padding: 20
    }}>
      <div style={{
        backgroundColor: '#ff3366',
        padding: '30px 40px',
        borderRadius: '20px',
        boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
        width: '100%',
        maxWidth: 500,
        color: 'white'
      }}>
        <h1 style={{ textAlign: 'center', marginBottom: 20 }}>🍱 메뉴 추천 시스템</h1>

        <p style={{ textAlign: 'center', fontSize: 14, marginBottom: 30 }}>
          <strong>무료 이용 기회: {Math.max(0, LIMIT - count)}회 남음</strong><br />
          {count >= LIMIT && "⚠️ 무료 이용이 종료되었습니다. 유료 플랜을 확인해주세요."}
        </p>

        <div style={{ display: 'flex', gap: 10 }}>
          <input
            value={question}
            onChange={e => setQuestion(e.target.value)}
            placeholder="오늘 뭐 먹을까?"
            disabled={count >= LIMIT}
            style={{
              flex: 1,
              padding: '10px 15px',
              fontSize: 16,
              borderRadius: 8,
              border: 'none',
              outline: 'none',
              backgroundColor: count >= LIMIT ? '#ddd' : 'white',
              color: '#333'
            }}
          />
          <button
            onClick={ask}
            disabled={count >= LIMIT}
            style={{
              padding: '10px 16px',
              backgroundColor: count >= LIMIT ? '#aaa' : 'white',
              color: count >= LIMIT ? '#eee' : '#ff3366',
              border: 'none',
              borderRadius: 8,
              cursor: count >= LIMIT ? 'not-allowed' : 'pointer',
              fontWeight: 'bold'
            }}
          >
            추천받기
          </button>
        </div>

        {result && (
          <div style={{
            marginTop: 30,
            backgroundColor: 'white',
            padding: 20,
            borderRadius: 12,
            color: '#ff3366',
            whiteSpace: 'pre-wrap',
            lineHeight: 1.6
          }}>
            {result}
          </div>
        )}

        {/* 👇 요금제/회원가입 버튼 위치 */}
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          gap: 12,
          marginTop: 30
        }}>
          <button
            style={{
              padding: '10px 20px',
              backgroundColor: 'white',
              color: '#ff3366',
              border: '2px solid white',
              borderRadius: 10,
              fontWeight: 'bold',
              cursor: 'pointer'
            }}
            onClick={() => alert("요금제 모달 열기")}
          >
            💳 요금제 보기
          </button>

          <button
            style={{
              padding: '10px 20px',
              backgroundColor: 'white',
              color: '#ff3366',
              border: '2px solid white',
              borderRadius: 10,
              fontWeight: 'bold',
              cursor: 'pointer'
            }}
            onClick={() => alert("회원가입 모달 열기")}
          >
            📝 회원가입
          </button>
        </div>

      </div>
    </div>
  );
}

export default App;
