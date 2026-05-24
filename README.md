# Sujho AI Teaching Assistant - Core Agent Backend Prototype

A production-ready prototype built to demonstrate the foundational architecture of an AI-native Teaching Assistant platform for Indian K-12 education. This backend integrates a robust FastAPI server with Google's Gemini 2.5 Flash model to deliver real-time, context-aware student metrics directly over WhatsApp via Twilio.

The platform showcases a deterministic **Tool-Calling (Function Calling) lifecycle** that completely eliminates LLM hallucination by binding the agent directly to a shared relational database layer.

---

## 🏗️ Architectural Topology

[ WhatsApp Client ]
                       │ (Inbound User Prompt)
                       ▼
           [ Twilio WhatsApp Gateway ]
                       │ (Encrypted Public Webhook POST)
                       ▼
        [ FastAPI Backend via Public Tunnel ]
                       │ 
  ┌────────────────────┴────────────────────┐
  ▼                                         ▼
  [ Google Gemini 2.5 Flash ]             [ SQLite Data Layer ]
• System Instructions                   • Relational Schema
• Tool Declaration (Schema)             • Contextual Seeding
• Abstract Reasoning Loop               • Case-Insensitive Queries
│                                         ▲
└──────► [ Executable Function Tool ] ────┘
(Automated Parameter Extraction)


---

## 🧠 Core Engineering Principles Implemented

### 1. Clean Abstractions & Architectural Taste
The codebase intentionally isolates concerns to ensure modular scale:
* `database.py`: Fully abstracts the data layer. Handles thread-safe SQLite initialization, table indexing, dummy data seeding, and case-insensitive parameterized lookups.
* `main.py`: Manages network ingestion, handles CORS/tunneling middleware constraints, configures agent behavior, and serializes responses into strict **TwiML (Twilio Markup Language)**.

### 2. AI-Native Workflow (10x Developer Paradigm)
Built natively within an AI-first IDE (**Cursor**). Utilized advanced semantic context indexing (`@` file and symbol tracking) to radically accelerate iteration velocity across environment setup, syntax debugging, and module refactoring.

### 3. Deterministic Function Calling
Instead of allowing the LLM to hallucinate academic records, the model is bound via explicit tool declarations. When a user queries a student's status, the orchestration engine pauses the generation loop, extracts the target parameters, runs an isolated SQL statement against the local state, and passes the grounded context back to the model for semantic synthesis.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.x
* **API Framework:** FastAPI & Uvicorn (Asynchronous server architecture)
* **Orchestration Engine:** Google GenAI SDK (`gemini-2.5-flash`)
* **Database:** SQLite3 (Local relational storage)
* **Ingress & Gateway:** Twilio WhatsApp Sandbox API & Pyngrok Tunneling

---

## 🚀 Getting Started

### 1. Environment & Secrets Configuration
Clone the repository and set up a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt


Create a .env file in the root directory:

GEMINI_API_KEY=your_gemini_api_key
NGROK_AUTH_TOKEN=your_ngrok_auth_token


2. Run the Ingress Tunnel

Initialize the secure public webhook tunnel to port 8000:

python tunnel.py

3. Launch the Application Server

In a parallel terminal, spin up the asynchronous FastAPI engine:

python main.py


4. Hook the Webhook to Twilio

Copy the generated https://...ngrok-free.dev address from your tunnel terminal, append /webhook to it, and map it as an HTTP POST hook in your Twilio Sandbox Console.

URL Destination: [https://your-unique-subdomain.ngrok-free.dev/webhook](https://your-unique-subdomain.ngrok-free.dev/webhook)


---
