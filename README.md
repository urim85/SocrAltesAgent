# 🦉 SocrAItes: 소크라테스식 학습 코치 Agent

> "정답을 알려주지 않는 AI, 스스로 답을 찾게 하는 AI"

SocrAItes(소크라테스)는 단순한 정답 제공을 넘어, 소크라테스식 문답법을 통해 학습자 스스로 개념을 깨우치도록 돕는 RAG 기반 AI Agent입니다. 

## 🚀 프로젝트 개요
- **목적:** 대학원생들이 강의 자료를 깊이 있게 이해하고 비판적 사고를 기를 수 있도록 돕는 메타인지 학습 도우미
- **주요 특징:** 
  - **정답 지연 & 반문:** 즉각적인 답 대신 반문, 예시 요구, 전제 검토를 통해 사고를 자극합니다.
  - **강의 자료 기반 (RAG):** 환각(Hallucination)을 최소화하고 교수님이 제공한 PDF 자료를 기반으로 답변합니다.
  - **적응형 깊이 조절 (Adaptive Socratic Depth):** 학습자의 좌절 신호를 감지하여 힌트를 제공하거나 난이도를 조절합니다.

## ✨ 주요 기능
- **강의자료 RAG:** PDF 업로드 및 지식 기반 질의응답
- **소크라테스식 대화 엔진:** 반문 및 사고 유도 대화
- **학습 도우미 (Function Calling):** 퀴즈 생성, 일정 등록, 약점 저장
- **약점 진단 & 리포트:** 대화 이력을 기반으로 한 주간 학습 리포트 제공

## 🛠️ 기술 스택
- **LLM:** GPT-4o-mini / Claude Haiku
- **RAG & Vector DB:** LangChain, OpenAI text-embedding-3-small, ChromaDB
- **Orchestration:** LangGraph (Agentic Workflow)
- **Frontend:** Streamlit
- **기타:** Python, SQLite

## 📂 문서
상세 기획 및 설계 문서는 `docs/` 디렉토리를 참고하세요.
- [소프트웨어 요구사항 명세서 (SRS)](docs/SRS.md)
- [시스템 아키텍처 및 설계 문서](docs/System_Design.md)

## 🏃 시작하기 (Getting Started)
(추후 작성 예정)
