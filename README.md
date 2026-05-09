# 🦉 SocrAItes: 소크라테스식 학습 코치 Agent

> "정답을 알려주지 않는 AI, 스스로 답을 찾게 하는 AI"

SocrAItes(소크라테스)는 단순한 정답 제공을 넘어, 소크라테스식 문답법을 통해 학습자 스스로 개념을 깨우치도록 돕는 RAG 기반 AI Agent입니다. 

![SocrAItes 실행 화면](docs/images/screenshot.png)

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

SocrAItes 서비스를 로컬 환경에서 실행하려면 아래 단계를 따르세요.

### 1. 환경 설정 (Setup)
Python 3.9 이상의 환경이 필요합니다. 가상환경을 생성하고 필요한 패키지를 설치합니다.

```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화 (Windows)
.venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정 (Configuration)
`.env.example` 파일을 복사하여 `.env` 파일을 생성하고, 필요한 API 키를 입력합니다.

```bash
cp .env.example .env
```

`.env` 파일을 열어 아래 항목을 채웁니다:
- `OPENAI_API_KEY`: OpenAI API 키 (필수)
- `ANTHROPIC_API_KEY`: Anthropic API 키 (선택)

### 3. 데이터베이스 초기화 (Database Initialization)
SQLite 데이터베이스를 초기화하고 샘플 데이터를 삽입합니다.

```bash
# DB 초기화 및 샘플 데이터 삽입
python scripts/init_db.py --seed
```

### 4. 강의 자료 인덱싱 (RAG Ingestion)
강의 PDF를 `data/pdfs/` 폴더에 복사한 후 인덱싱을 실행합니다.

```bash
# PDF를 data/pdfs/에 복사한 후
python scripts/ingest_pdf.py

# 특정 파일만 인덱싱
python scripts/ingest_pdf.py --file data/pdfs/Week5.pdf

# 검색 테스트
python scripts/ingest_pdf.py --query "CAP 정리란 무엇인가"
```

> **참고:** `PyMuPDF` 패키지가 설치되어야 실제 PDF 파싱이 가능합니다.
> API 키 없이도 기본 임베딩(sentence-transformers)으로 인덱싱할 수 있습니다.

### 5. 서비스 실행 (Run)
FastAPI 서버를 실행합니다.

```bash
# 서버 실행 (모듈 모드)
python -m src.api
```

서버가 구동되면 브라우저에서 **[http://localhost:8000](http://localhost:8000)**에 접속하여 서비스를 이용할 수 있습니다.

### 5. 테스트 실행 (Optional)
에이전트가 정상적으로 동작하는지 터미널에서 간단히 테스트할 수 있습니다.

```bash
python scripts/test_agent.py
```
