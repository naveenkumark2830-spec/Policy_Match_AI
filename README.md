<div align="center">

<img src="https://www.sju.edu.in/assets/img/st-joseph-university-logo.png" height="80" style="background:white; padding:8px; margin:0 16px;" />
<img src="https://www.erafoundationindia.org/images/logo.svg" height="80" style="background:white; padding:8px; margin:0 16px;" />
<img src="https://comedkares.org/wp-content/uploads/2023/04/Comedkares-Logo-EPS.png" height="80" style="background:white; padding:8px; margin:0 16px;" />

</div>

---

# Policy_Match_AI

## Multilingual AI-Powered Government Scheme Discovery Platform

### Conversational Government Scheme Advisor using RAG, Semantic Search and Large Language Models

**Naveen Kumar K, MSc BDA, 252BDA25· Dharnesh, MSc BDA, 252BDA27· Prithvish William, MSc BDA, 252BDA18**

# Abstract

Policy_Match_AI is an AI-powered conversational platform designed to simplify access to government welfare schemes for Indian citizens.

The system combines:

- Retrieval-Augmented Generation (RAG)
- Sentence Transformers
- FAISS Semantic Search
- Groq LLM
- Conversational Memory
- FastAPI Backend

to help citizens discover government schemes relevant to their personal circumstances.

Unlike traditional government portals that require users to manually search through thousands of schemes, GovSchemeAI allows citizens to interact naturally through conversational text, voice, and AI avatars.

Example:

> "I am a farmer from Karnataka with an annual income of ₹2 lakh."

The system dynamically retrieves and explains relevant schemes from a curated government scheme knowledge base.

Future versions will include multilingual voice interaction, AI avatars, and mobile deployment through Flutter.

---

# Features

## Current Features

- Government Scheme Dataset (3368+ Schemes)
- Semantic Search using FAISS
- Sentence Transformer Embeddings
- Retrieval-Augmented Generation (RAG)
- Groq LLM Integration
- Profile Extraction
- Dynamic User Profiling
- Multi-Turn Conversations
- Session Memory
- Context-Aware Responses
- FastAPI Backend

---

## Upcoming Features

- Flutter Mobile Application
- Email / Phone Authentication
- PostgreSQL Database
- Voice Chat
- AI Avatar
- Multilingual Support
- Conversation History
- User Analytics

---

# Problem Statement

Government welfare schemes are often difficult to discover and understand due to:

- Lack of awareness
- Language barriers
- Complex eligibility criteria
- Fragmented information sources
- Poor accessibility of government portals

GovSchemeAI addresses these challenges through a conversational AI platform capable of understanding user needs, retrieving relevant schemes, and explaining them in simple natural language.

---

# Objectives

- Build a conversational AI assistant for government schemes.
- Enable semantic retrieval using Sentence Transformers and FAISS.
- Support dynamic user profile extraction.
- Maintain multi-turn conversational memory.
- Deliver personalized scheme recommendations.
- Prevent hallucinations through RAG grounding.
- Support multilingual communication.
- Enable voice and avatar-based interactions.
- Improve accessibility of government welfare information.

---

# System Architecture

```text
User
  │
  ▼
Flutter Mobile App
  │
  ▼
FastAPI Backend
  │
  ▼
Profile Extraction
  │
  ▼
Session Memory
  │
  ▼
Sentence Transformer Embeddings
  │
  ▼
FAISS Semantic Search
  │
  ▼
Top Relevant Schemes
  │
  ▼
Groq LLM
  │
  ▼
Context-Aware Response
  │
  ▼
User
```

---

# Methodology

## Step 1: User Query

Example:

```text
I am a farmer from Karnataka with annual income of ₹2 lakh.
```

---

## Step 2: Profile Extraction

The system extracts:

- Occupation
- Age
- Income
- State
- Gender
- Category

The profile is continuously updated throughout the conversation.

---

## Step 3: Embedding Generation

The query is converted into vector embeddings using:

```text
SentenceTransformer
all-MiniLM-L6-v2
```

---

## Step 4: Semantic Retrieval

FAISS retrieves the most relevant government schemes based on semantic similarity.

Example:

- PM-KISAN
- Agriculture Infrastructure Fund
- Crop Insurance Scheme
- Kisan Credit Card

---

## Step 5: Response Generation

Retrieved schemes are passed to the Groq LLM.

The LLM:

- Explains schemes
- Answers follow-up questions
- Maintains context
- Generates human-like responses

---

## Step 6: Conversational Memory

The system remembers:

- User profile
- Recommended schemes
- Selected scheme
- Previous questions
- Previous responses

This enables natural follow-up conversations.

---

# Technology Stack

| Component | Technology |
|------------|------------|
| Frontend | Flutter (Upcoming) |
| Backend | FastAPI |
| LLM | Groq (Llama 3) |
| Semantic Search | FAISS |
| Embeddings | Sentence Transformers |
| Dataset Storage | CSV |
| Database | PostgreSQL (Upcoming) |
| Session Memory | Custom Session Manager |
| Voice Processing | Whisper (Planned) |
| Translation | IndicTrans2 (Planned) |
| Avatar System | D-ID / HeyGen (Planned) |

---

# Project Structure

```text
GovSchemeAI/
│
├── data/
│   ├── cleaned_schemes.csv
│
├── models/
│   ├── scheme_index.faiss
│
├── src/
│   ├── app.py
│   ├── api.py
│   ├── rag_engine.py
│   ├── response_generator.py
│   ├── profile_extractor.py
│   ├── session_manager.py
│   ├── conversation_manager.py
│   └── utils.py
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/GovSchemeAI.git
cd GovSchemeAI
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Application

## CLI Version

```bash
python run.py
```

---

## FastAPI Backend

```bash
uvicorn src.api:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

# Example Conversation

### User

```text
I am a farmer from Karnataka.
```

### Assistant

```text
Based on your profile, these schemes may help:

1. PM-KISAN
2. Agriculture Infrastructure Fund
3. Crop Insurance Scheme
4. Kisan Credit Card
5. Krishi Bhagya

Would you like details about any of these?
```

### User

```text
Tell me more about the second one.
```

### Assistant

Explains Agriculture Infrastructure Fund.

### User

```text
Am I eligible?
```

Assistant uses conversation context and user profile to answer.

---

# Dataset

Current Dataset:

```text
3368 Government Schemes
```

Contains:

- Scheme Name
- Benefits
- Eligibility
- Financial Assistance
- Application Information
- State Information
- Detailed Description

The dataset is transformed into a unified text representation for semantic search.

---

# Future Scope

## Voice AI

Support for:

- English
- Hindi
- Tamil
- Kannada

---

## AI Avatar

Features:

- Human-like digital assistant
- Lip-sync speech
- Natural gestures
- Multilingual communication

---

## Mobile Application

Flutter application with:

- Login
- Chat
- Voice
- Avatar
- History
- Profile

---

## Additional Languages

Future support for:

- Telugu
- Malayalam
- Bengali
- Marathi
- Odia

---

## Real-Time Scheme Updates

Automated ingestion of newly announced government schemes.

---

# Project Status

## Completed

- [x] Dataset Collection
- [x] Data Cleaning
- [x] Scheme Text Generation
- [x] Embedding Generation
- [x] FAISS Index Creation
- [x] Semantic Retrieval
- [x] Groq Integration
- [x] Session Memory
- [x] Profile Extraction
- [x] Multi-Turn Conversations
- [x] FastAPI Backend

---

## In Progress

- [ ] Flutter Frontend
- [ ] PostgreSQL Integration
- [ ] Voice Chat
- [ ] AI Avatar
- [ ] Multilingual Translation
- [ ] User Authentication

---

# Conclusion

GovSchemeAI demonstrates how Retrieval-Augmented Generation (RAG), semantic search, and large language models can be combined to make government welfare information more accessible.

By transforming complex scheme information into conversational interactions, the platform enables citizens to discover, understand, and access government benefits more effectively.

The architecture is designed to be scalable, multilingual, and extensible, making it suitable for deployment as a large-scale citizen assistance platform.


