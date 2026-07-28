<div align="center">

```
███╗   ██╗███████╗██╗   ██╗██████╗  █████╗ ██╗   ██╗██╗  ████████╗
████╗  ██║██╔════╝██║   ██║██╔══██╗██╔══██╗██║   ██║██║  ╚══██╔══╝
██╔██╗ ██║█████╗  ██║   ██║██████╔╝███████║██║   ██║██║     ██║   
██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██╔══██║╚██╗ ██╔╝██║     ██║   
██║ ╚████║███████╗╚██████╔╝██║  ██║██║  ██║ ╚████╔╝ ███████╗██║   
╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝   
```

### 🔐 Multi-Tenant Enterprise RAG Platform with Secure AI Knowledge Isolation

![Architecture Diagram](diagram.png)

<br/>

[![Frontend](https://img.shields.io/badge/🖥️_Live_App-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://f6fatjpcgdgnmqk8keai5h.streamlit.app/)
[![Backend](https://img.shields.io/badge/🚀_Live_API-Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://neuravault-multi-tenant-enterprise-rag.onrender.com)
[![API Docs](https://img.shields.io/badge/📖_API_Docs-Swagger_UI-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)](https://neuravault-multi-tenant-enterprise-rag.onrender.com/docs)

<br/>

![Python](https://img.shields.io/badge/Python_3.12+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB_Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-000000?style=flat-square&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_LLaMA-F55036?style=flat-square&logoColor=white)
![Beanie](https://img.shields.io/badge/Beanie_ODM-47A248?style=flat-square&logoColor=white)

</div>

---

## 🧠 What is NeuraVault?

**NeuraVault** is a production-grade, **multi-tenant RAG SaaS platform** where every user gets their own completely isolated AI knowledge base. Upload your private documents — PDFs, DOCX, or TXT — and query them with a powerful LLM that answers **only from your documents**, **never from someone else's**.

The platform enforces **namespace-level isolation at the vector store** — each user's Pinecone namespace equals their unique `user_id`. Even if two users upload the same file, their data stays completely separate. No cross-tenant leakage. Ever.

Built with enterprise-grade features: **JWT dual-token auth**, **per-user rate limiting**, **background document ingestion**, **async MongoDB ODM (Beanie)**, **usage telemetry**, and a **custom dark-themed Streamlit UI**.

---

## 🌐 Live Deployment

| | Service | URL |
|---|---|---|
| 🖥️ | **Frontend App** | [f6fatjpcgdgnmqk8keai5h.streamlit.app](https://f6fatjpcgdgnmqk8keai5h.streamlit.app/) |
| 🚀 | **Backend REST API** | [neuravault-multi-tenant-enterprise-rag.onrender.com](https://neuravault-multi-tenant-enterprise-rag.onrender.com) |
| 📖 | **Swagger UI** | [/docs](https://neuravault-multi-tenant-enterprise-rag.onrender.com/docs) |
| 📋 | **ReDoc** | [/redoc](https://neuravault-multi-tenant-enterprise-rag.onrender.com/redoc) |

---

## ✨ Platform Features

<table>
<tr>
<td width="50%">

### 🔐 Security & Auth
- ✅ **JWT Dual-Token System** — short-lived access (60 min) + long-lived refresh (7 days)
- ✅ **bcrypt_sha256 Hashing** — SHA256 first, then bcrypt (handles passwords > 72 bytes)
- ✅ **HTTPBearer Middleware** — every protected route uses `Depends(get_current_user)`
- ✅ **Token Type Validation** — access tokens rejected on refresh endpoint and vice versa

</td>
<td width="50%">

### 🏢 Multi-Tenancy
- ✅ **Pinecone Namespace Isolation** — each user's namespace = their `user_id`
- ✅ **Zero cross-tenant leakage** — queries are always namespace-scoped
- ✅ **Per-user usage tracking** — daily resets for queries & uploads
- ✅ **Plan-based access** — free / premium tier framework built-in

</td>
</tr>
<tr>
<td width="50%">

### ⚡ Performance
- ✅ **Background Ingestion** — upload returns `202 Accepted` immediately; processing happens async
- ✅ **`asyncio.to_thread()`** — non-blocking Pinecone & embedding calls
- ✅ **Batch upsert (100 vectors/batch)** — efficient large-document ingestion
- ✅ **`@lru_cache` on Settings** — singleton config object, loaded once

</td>
<td width="50%">

### 🛡️ Rate Limiting
- ✅ **SlowAPI (global)** — IP-based rate limiting via slowapi
- ✅ **InMemoryRateLimiter** — per-user: 20 queries/min, 50 uploads/day
- ✅ **Daily auto-reset** — usage counters reset at midnight UTC
- ✅ **Upgrade path** — limit messages reference premium plan

</td>
</tr>
</table>

---

## 🏗️ Architecture

```mermaid
flowchart TD
    U(["👤 User"])

    subgraph FE ["🖥️ Streamlit Frontend · Streamlit Cloud"]
        LOGIN["🔐 Login / Register"]
        CHAT["💬 Chat Page"]
        DOCS["🗃️ Documents Page"]
        DASH["📊 Dashboard Page"]
        HIST["📜 History Page"]
        API["🔌 APIClient\napi_client.py"]
    end

    subgraph BE ["⚙️ FastAPI Backend · Render · /api/v1"]
        direction TB
        AUTH["🔑 /auth\nregister · login · refresh · me"]
        DOCRTR["📄 /documents\nupload · list · get · delete"]
        QRTR["❓ /query\nquery · history"]
        STRTR["📊 /stats\nstats · namespace"]
        BG["🔄 BackgroundTask\n_background_ingest"]
        RAG["🤖 RAG Pipeline\nembed → retrieve → generate → log"]
        RL["🛡️ Rate Limiter\n20 q/min · 50 upload/day"]
    end

    subgraph STORE ["☁️ Cloud Storage"]
        PINE[("🌲 Pinecone\nNamespace = user_id\n1536-dim · cosine")]
        MONGO[("🍃 MongoDB Atlas\nBeanie ODM\n4 collections")]
        OAI["🔑 OpenAI\ntext-embedding-3-small"]
        GROQ["⚡ Groq\nllama-3.3-70b-versatile"]
    end

    U --> LOGIN --> AUTH
    U --> CHAT & DOCS & DASH & HIST
    CHAT & DOCS & DASH & HIST --> API
    API -->|"JWT Bearer"| AUTH & DOCRTR & QRTR & STRTR

    DOCRTR --> BG --> RAG
    QRTR --> RL --> RAG
    RAG --> OAI --> PINE
    RAG --> GROQ
    RAG --> MONGO
    AUTH --> MONGO
    STRTR --> PINE & MONGO

    classDef user   fill:#7c3aed,stroke:#5b21b6,color:#fff
    classDef fe     fill:#1d4ed8,stroke:#1e40af,color:#fff
    classDef be     fill:#0f766e,stroke:#059669,color:#fff
    classDef store  fill:#374151,stroke:#1f2937,color:#fff

    class U user
    class LOGIN,CHAT,DOCS,DASH,HIST,API fe
    class AUTH,DOCRTR,QRTR,STRTR,BG,RAG,RL be
    class PINE,MONGO,OAI,GROQ store
```

---

## 🗂️ Project Structure

```
NeuraVault/
│
├── 📂 backend/
│   ├── 🐍 main.py                    # App factory · lifespan · CORS · routers · global error handler
│   ├── ⚙️  config.py                 # Pydantic BaseSettings · @lru_cache singleton · origins_list property
│   │
│   ├── 📂 models/
│   │   └── 🐍 db_models.py           # Beanie Documents + Pydantic schemas (see table below)
│   │
│   ├── 📂 utils/
│   │   └── 🐍 auth.py                # bcrypt_sha256 · JWT create/decode · get_current_user dependency
│   │
│   ├── 📂 middleware/
│   │   └── 🐍 rate_limiter.py        # SlowAPI global limiter · InMemoryRateLimiter per-user
│   │
│   ├── 📂 routers/
│   │   ├── 🐍 auth.py                # /register · /login · /refresh · /me
│   │   ├── 🐍 documents.py           # /upload (202) · / (list) · /{id} (get) · DELETE /{id}
│   │   ├── 🐍 query.py               # POST / (RAG query) · GET /history
│   │   └── 🐍 stats.py               # GET / (usage stats) · GET /namespace (Pinecone stats)
│   │
│   ├── 📂 services/
│   │   ├── 🐍 embeddings.py          # embed_texts · embed_query · embed_documents (batch 100)
│   │   ├── 🐍 vector_store.py        # VectorStore class — all ops scoped to user namespace
│   │   ├── 🐍 document_processor.py  # parse PDF/DOCX/TXT · chunk · embed · upsert · MongoDB record
│   │   └── 🐍 rag_pipeline.py        # run_rag() · system prompt · user prompt builder · query logger
│   │
│   └── 📋 requirements.txt
│
├── 📂 frontend/
│   ├── 🐍 app.py                     # Streamlit UI — 4 pages + custom dark CSS + chat bubbles
│   ├── 🐍 api_client.py              # APIClient class — wraps all backend endpoints with JWT headers
│   ├── 🐍 sample_UI.py               # Alternative UI layout
│   └── 📋 requirements.txt
│
├── 📄 Workflow_of_Project.txt        # Step-by-step build guide
├── 📄 sample_Workflow.txt            # Detailed development roadmap
├── 🐍 main.py                        # Root entry point
└── 📋 pyproject.toml
```

---

## 📊 Data Models — What Each Model Does

| Model | Type | MongoDB Collection | Purpose |
|---|---|---|---|
| `User` | Beanie Document | `users` | Stores email, username, bcrypt_sha256 password, plan, `pinecone_namespace = user_id` |
| `UsageStat` | Beanie Document | `usage_stats` | Tracks `queries_today`, `uploads_today`, `total_queries`, `total_uploads` with daily auto-reset |
| `DocumentRecord` | Beanie Document | `documents` | Tracks file metadata, chunk count, token count, and `status` (processing / ready / error) |
| `QueryLog` | Beanie Document | `query_logs` | Stores every query with answer, sources, `latency_ms`, `tokens_used` for history |
| `UserCreate` | Pydantic Schema | — | Signup request: `email`, `username`, `password` |
| `UserLogin` | Pydantic Schema | — | Login request: `username`, `password` |
| `TokenResponse` | Pydantic Schema | — | Auth response: `access_token`, `refresh_token`, `token_type` |
| `UserOut` | Pydantic Schema | — | Safe user response (no password): `user_id`, `email`, `username`, `plan`, `created_at` |
| `DocumentOut` | Pydantic Schema | — | Document response: `doc_id`, `filename`, `file_type`, `chunk_count`, `status` |
| `StatsOut` | Pydantic Schema | — | Dashboard response: today's + total queries and uploads, document count |
| `QueryRequest` | Pydantic Schema | — | Chat input: `query`, `top_k` (default 5), `temperature` (default 0.3) |
| `QueryResponse` | Pydantic Schema | — | Chat output: `answer`, `sources`, `latency_ms`, `tokens_used` |

---

## 🔑 Authentication System

NeuraVault uses a **dual-token JWT system** — the same pattern used in production-grade apps:

```
Register ──► MongoDB insert ──► UsageStat created ──► namespace = user_id
Login    ──► bcrypt_sha256 verify ──► access_token (60 min) + refresh_token (7 days)
Refresh  ──► validate refresh type ──► issue new token pair
/me      ──► HTTPBearer → decode → User.find_one → UserOut
```

**Why `bcrypt_sha256`?** Standard bcrypt only accepts 72 bytes. Long passwords get silently truncated. The `bcrypt_sha256` scheme runs `SHA256 → bcrypt` to handle passwords of any length safely.

**Why `user_id` only in refresh token?** Usernames can change. User IDs can't. The refresh token uses `sub = user_id` so it stays valid even after a username update.

```python
# Access token: short-lived, contains username for convenience
{"sub": user_id, "username": username, "type": "access", "exp": ...}

# Refresh token: long-lived, only ID — username could change
{"sub": user_id, "type": "refresh", "exp": ...}
```

---

## 🏢 Tenant Isolation — How It Works

This is the most critical feature. Here is the isolation guarantee at every level:

```
User signs up
    └── user.pinecone_namespace = user.user_id   (set at registration, never changes)

User uploads a document
    └── VectorStore(namespace=user.pinecone_namespace)
        └── index.upsert(vectors=..., namespace=namespace)
                                      ↑ scoped to this user only

User asks a question
    └── VectorStore(namespace=user.pinecone_namespace)
        └── index.query(vector=..., namespace=namespace)
                                    ↑ Pinecone only searches THIS namespace
```

> **Zero trust between tenants.** A user querying "What is in my contracts?" will never surface chunks from another user's contracts — even if the documents are identical — because Pinecone namespaces act as hard partition walls.

---

## 📥 Document Ingestion Pipeline

Uploading a document triggers a **non-blocking 5-stage pipeline**:

```
POST /documents/upload
    │
    ├── [Sync] Rate limit check (50 uploads/day)
    ├── [Sync] File type validation (pdf · docx · txt · doc)
    ├── [Sync] File size check (max 20 MB)
    ├── [Sync] Create DocumentRecord in MongoDB → status: "processing"
    ├── [Sync] Increment UsageStat.uploads_today
    ├── [Sync] Return 202 Accepted → DocumentOut immediately
    │
    └── [Background Task] _background_ingest()
            │
            ├── 1. parse_file()     → raw text (PyPDF2 / python-docx / UTF-8 decode)
            ├── 2. SPLITTER         → chunk_size=600, overlap=80
            ├── 3. embed_documents()→ OpenAI text-embedding-3-small (batch 100)
            ├── 4. VectorStore.upsert_chunks() → Pinecone (batch 100, async thread)
            └── 5. DocumentRecord.save() → status: "ready", chunk_count, token_count
```

The user sees `status: processing` immediately and can poll `GET /documents/{doc_id}` to check when it becomes `ready`.

---

## 🤖 RAG Pipeline

```python
async def run_rag(user_id, namespace, query, top_k=5, temperature=0.3):
    # 1. Embed the query
    query_vector = await embed_query(query)          # OpenAI text-embedding-3-small

    # 2. Retrieve from this user's namespace only
    store = VectorStore(namespace=namespace)
    matches = await store.query(vector=query_vector, top_k=top_k)

    # 3. Build structured prompt with source attribution
    user_prompt = _build_user_prompt(query, matches)
    # → "[Source: report.pdf, Chunk: 3]\n<chunk text>\n----\n..."

    # 4. Generate via Groq LLaMA
    completion = await groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[SYSTEM_PROMPT, user_prompt],
        temperature=temperature,
        max_tokens=1024
    )

    # 5. Log to MongoDB (latency, tokens, sources)
    await _log_query(user_id, query, answer, sources, latency_ms, tokens_used)

    return answer, sources, latency_ms, tokens_used
```

**System Prompt rules (strictly enforced):**
1. Answer ONLY from the provided context
2. If context is insufficient → say so explicitly
3. Always cite the source document
4. Be concise and structured — use bullet points
5. Never fabricate information

---

## 🛡️ Rate Limiting — Two Layers

| Layer | Scope | Limit | Implementation |
|---|---|---|---|
| **SlowAPI** | Per IP address | Configurable | `@limiter.limit("X/minute")` decorator |
| **InMemoryRateLimiter** | Per user_id | 20 queries/min · 50 uploads/day | asyncio.Lock sliding window |

```python
# Per-user query rate check (sliding 60-second window)
async def check_query_limit(self, user_id: str) -> bool:
    async with self._lock:
        now = datetime.utcnow()
        window = [ts for ts in self._query_counts[user_id]
                  if (now - ts).total_seconds() < 60]
        if len(window) >= settings.rate_limit_per_minute:
            return False
        self._query_counts[user_id].append(now)
        return True
```

> **Production note:** The `InMemoryRateLimiter` is thread-safe for asyncio single-worker deployments. For multi-worker production, replace with Redis + `redis-py` atomic operations.

---

## 🖥️ Frontend UI — 4 Pages

The Streamlit frontend uses a **custom dark theme** (`#0a0e1a` background, `Space Grotesk` font, `JetBrains Mono` for code) with fully custom CSS components:

| Page | Route Key | What It Shows |
|---|---|---|
| **💬 Chat** | `chat` | Chat bubbles, source chips, latency + token metadata, adjustable `top_k` and `temperature` sliders |
| **🗃️ Documents** | `documents` | Upload panel (PDF/DOCX/TXT), document list with `ready/processing/error` status badges, delete button |
| **📊 Dashboard** | `dashboard` | 4-tile metric grid (documents, queries today, total queries, total uploads) + Pinecone namespace info |
| **📜 History** | `history` | Full query history with expandable cards showing answer, sources, latency, tokens, timestamp |

---

## 🌐 API Reference

Base URL: **`https://neuravault-multi-tenant-enterprise-rag.onrender.com/api/v1`**

> Full interactive docs at [`/docs`](https://neuravault-multi-tenant-enterprise-rag.onrender.com/docs)

### 🔑 Auth

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | ❌ | Create account — returns `UserOut` |
| `POST` | `/auth/login` | ❌ | Login — returns `access_token` + `refresh_token` |
| `POST` | `/auth/refresh` | ❌ | Refresh access token using refresh token |
| `GET` | `/auth/me` | ✅ Bearer | Get current user profile |

### 📄 Documents

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/documents/upload` | ✅ Bearer | Upload PDF/DOCX/TXT → returns `202 Accepted` immediately |
| `GET` | `/documents/` | ✅ Bearer | List all documents for this user |
| `GET` | `/documents/{doc_id}` | ✅ Bearer | Get single document by ID |
| `DELETE` | `/documents/{doc_id}` | ✅ Bearer | Delete from Pinecone + MongoDB |

### ❓ Query

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/query/` | ✅ Bearer | Query your knowledge base — RAG answer with sources |
| `GET` | `/query/history` | ✅ Bearer | Get past query history (default last 20) |

### 📊 Stats

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/stats/` | ✅ Bearer | Usage stats: queries & uploads (today + total) + doc count |
| `GET` | `/stats/namespace` | ✅ Bearer | Pinecone namespace stats + queries remaining this minute |

### Quick Test

```bash
# Register
curl -X POST https://neuravault-multi-tenant-enterprise-rag.onrender.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","username":"yourname","password":"secure123"}'

# Login → copy access_token
curl -X POST https://neuravault-multi-tenant-enterprise-rag.onrender.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"yourname","password":"secure123"}'

# Upload a document
curl -X POST https://neuravault-multi-tenant-enterprise-rag.onrender.com/api/v1/documents/upload \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -F "file=@report.pdf"

# Ask a question
curl -X POST https://neuravault-multi-tenant-enterprise-rag.onrender.com/api/v1/query/ \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"query":"Summarise the key findings","top_k":5,"temperature":0.3}'
```

---

## 📦 Installation & Local Setup

### Prerequisites

- Python 3.12+
- [MongoDB Atlas](https://www.mongodb.com/atlas) (free tier)
- [Pinecone](https://pinecone.io) (free tier)
- [OpenAI API Key](https://platform.openai.com) (for embeddings)
- [Groq API Key](https://console.groq.com) (free — for LLaMA generation)

### 1. Clone

```bash
git clone https://github.com/paras160500/NeuraVault-Multi-Tenant-Enterprise-RAG-Platform-with-Secure-AI-Knowledge-Isolation.git
cd NeuraVault-Multi-Tenant-Enterprise-RAG-Platform-with-Secure-AI-Knowledge-Isolation
```

### 2. Install

```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 3. Backend `.env`

```env
# JWT
JWT_SECRET_KEY=your_super_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# MongoDB
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/
MONGODB_DB_NAME=tenant_rag_saas

# Pinecone
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=tenant-rag-sass-index

# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Groq
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

# Rate Limits
RATE_LIMIT_PER_MINUTE=20
RATE_LIMIT_UPLOAD_PER_DAY=50

# CORS (comma-separated)
ALLOWED_ORIGINS=http://localhost:8501

# App
APP_ENV=development
LOG_LEVEL=INFO
```

### 4. Frontend `.env`

```env
BACKEND_URL=http://localhost:8000/api/v1
# For live backend:
# BACKEND_URL=https://neuravault-multi-tenant-enterprise-rag.onrender.com/api/v1
```

### 5. Run

```bash
# Terminal 1 — Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## ☁️ Deployment

### Backend → Render

| Setting | Value |
|---|---|
| **Root Directory** | `backend` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

Add all `.env` variables in the Render **Environment** tab.

### Frontend → Streamlit Cloud

| Setting | Value |
|---|---|
| **Main file path** | `frontend/app.py` |
| **Secret** | `BACKEND_URL=https://neuravault-multi-tenant-enterprise-rag.onrender.com/api/v1` |

---

## ⚡ Tech Stack

| Layer | Technology | Why |
|---|---|---|
| **Frontend** | Streamlit + Custom CSS | Dark enterprise UI with Space Grotesk + JetBrains Mono fonts |
| **Backend** | FastAPI + Uvicorn | Async, typed, auto-docs via OpenAPI |
| **MongoDB ODM** | Beanie (async) | Native async MongoDB with Pydantic models + lifespan init |
| **Auth** | JWT (python-jose) + passlib bcrypt_sha256 | Dual-token system, long-password safe |
| **Vector Store** | Pinecone Serverless | Namespace isolation, 1536-dim cosine, AWS us-east-1 |
| **Embeddings** | OpenAI text-embedding-3-small | 1536-dim, fast, cost-effective |
| **LLM** | Groq llama-3.3-70b-versatile | Fast inference, generous free tier |
| **Rate Limiting** | SlowAPI + InMemoryRateLimiter | Two-layer: IP global + per-user sliding window |
| **Chunking** | LangChain RecursiveCharacterTextSplitter | 600 token chunks, 80 overlap |
| **Config** | Pydantic BaseSettings + @lru_cache | Type-safe env vars, singleton pattern |
| **Background Tasks** | FastAPI BackgroundTasks | Non-blocking document ingestion |
| **Deployment** | Render (backend) + Streamlit Cloud (frontend) | |

---

## 🧠 Key Engineering Decisions

- **App Factory Pattern** — `create_app()` returns the FastAPI instance rather than defining a global `app`, making the code testable and importable without side effects.

- **Beanie Lifespan** — MongoDB connection is initialized in `@asynccontextmanager lifespan()`, ensuring clean startup/shutdown. All Beanie document models are registered once at boot.

- **`asyncio.to_thread()` for Pinecone** — the Pinecone SDK is synchronous. Wrapping every call in `asyncio.to_thread()` prevents blocking the FastAPI event loop during heavy upsert/query operations.

- **Background ingestion → 202** — uploading large PDFs could take 30+ seconds (parse + embed + upsert). Returning `202 Accepted` immediately and processing in background means the user is never left waiting for an HTTP timeout.

- **Refresh token only stores `user_id`** — usernames can change after account creation. The long-lived refresh token only stores the immutable `user_id` in `sub`, keeping it valid through profile updates.

- **`bcrypt_sha256` instead of plain `bcrypt`** — bcrypt silently truncates passwords longer than 72 bytes. The `bcrypt_sha256` scheme runs SHA256 first, producing a fixed-size hash that bcrypt can safely handle — no truncation, no silent security holes.

- **LRU-cached Settings** — `@lru_cache` on `get_settings()` ensures Pydantic only reads and validates `.env` once per process, not on every import.

---

## 🔮 Future Improvements

- [ ] **Redis-backed rate limiter** — replace InMemoryRateLimiter for true multi-worker horizontal scaling
- [ ] **Token refresh rotation** — invalidate old refresh tokens on use (prevent replay attacks)
- [ ] **Webhook on ingest complete** — notify frontend when background processing finishes
- [ ] **Document versioning** — re-upload a file to update embeddings without a full delete-and-reupload
- [ ] **Streaming LLM responses** — token-by-token answer streaming via FastAPI `StreamingResponse`
- [ ] **Admin panel** — super-admin view across all tenants with usage analytics
- [ ] **Email verification** — flip `is_verified` with a tokenized verification link

---

<div align="center">

**Built with 🧠 + ⚡ + 🔐**

*Multi-Tenant Enterprise RAG · FastAPI · Streamlit · MongoDB · Pinecone · Groq · Render*

**[paras160500](https://github.com/paras160500)**

</div>