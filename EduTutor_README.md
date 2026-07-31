# EduTutor — LLM-Powered Multi-Agent Tutoring System

An end-to-end AI tutoring system for **SPM Additional Mathematics**, built as a Final Year Project for the Bachelor of Information System (Hons.), Intelligent Systems Engineering (Big Data Track) at Universiti Teknologi MARA (UiTM).

EduTutor combines a **multi-agent architecture** (Router → Tutor → Hint), **Retrieval-Augmented Generation (RAG)** over curriculum-aligned materials, and a self-hosted local AI stack to deliver personalized, step-by-step math tutoring without relying on a single monolithic chatbot.

## How it works

- **Router Agent** — classifies the student's query and decides which specialist agent should respond.
- **Tutor Agent** — retrieves relevant curriculum content via RAG (Qdrant) and generates full worked explanations.
- **Hint Agent** — guides the student toward the answer step-by-step, without giving away the full solution, using the math reasoning API below.
- **Math Reasoning API** (`main.py`) — a FastAPI backend implementing the KSSM Solution of Triangles syllabus: Sine Rule, Cosine Rule, Area of Triangle, Heron's Formula, and the Ambiguous Case, each returning worked steps rather than just a final number.
- **Conversational Memory** — PostgreSQL-backed, so the tutor remembers context across a session.
- **Frontend** (`spm_tutor_chat.html`) — a lightweight chat interface for students.

## Stack

| Layer | Tool |
|---|---|
| Workflow orchestration | n8n |
| Local LLM inference | Ollama |
| Vector store (RAG) | Qdrant |
| Conversational memory | PostgreSQL |
| Math reasoning backend | FastAPI (Python) |
| External access tunneling | Ngrok |
| Containerization | Docker Compose |

## Running locally

```bash
git clone https://github.com/khausar17/EduTutor-LLM-Agentic-AI.git
cd EduTutor-LLM-Agentic-AI
cp .env.example .env   # fill in your own local secrets before running
docker compose --profile cpu up   # or gpu-nvidia / gpu-amd depending on your hardware
```

Once the stack is up, n8n is available at `http://localhost:5678`, Qdrant at `http://localhost:6333`, and the math reasoning API at `http://localhost:8000` (run via `uvicorn main:app --reload`).

## Acknowledgements

The local AI infrastructure (n8n + Ollama + Qdrant + PostgreSQL via Docker Compose) is adapted from n8n's open-source [Self-hosted AI Starter Kit](https://github.com/n8n-io/self-hosted-ai-starter-kit) (Apache License 2.0). All agent logic, the math reasoning API, RAG configuration, and the tutoring frontend are original work built on top of that infrastructure for this project.

## Author

**Nurul Khausar Faqihah binti Mohd Suhaimi**
Final Year Student, Intelligent Systems Engineering (Big Data Track), UiTM
📧 khausarn@gmail.com · 🌐 [khausar17.github.io](https://khausar17.github.io)

## License

Apache License 2.0 — see [LICENSE](LICENSE).
