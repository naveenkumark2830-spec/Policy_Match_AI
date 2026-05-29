# Policy_Match_AI

## Multilingual AI Financial Inclusion Assistant
### A Conversational AI System for Financial Education & Government Scheme Recommendation

**<<Naveen Kumar K>> · <<Dharnesh>> · <<Prithvish Wiliam >>**

---

## Abstract

A multilingual AI-powered assistant has been developed to address the financial exclusion experienced by a significant segment of India's population. The system combines large language models with Retrieval-Augmented Generation (RAG), multilingual speech processing, and an interactive avatar interface to deliver personalised financial guidance in English, Hindi, Tamil, and Kannada. Three interaction modalities are supported: manual text-based chat, real-time voice conversation, and an AI avatar video assistant with lip-sync animation. A hybrid recommendation engine — combining gradient-boosted machine learning with LLM-driven natural language explanation — identifies eligible government schemes, insurance products, and pension plans based on user-supplied demographic and financial profiles. End-to-end response latency is maintained within one to three seconds through streaming audio processing and asynchronous LLM inference. The architecture is deployed on AWS with JWT-authenticated APIs, vector-based semantic retrieval, and PCI-DSS-compliant data handling. The system is intended to democratise access to financial knowledge for over 500 million Indians currently underserved by conventional banking and advisory services.

**Keywords:** Financial Inclusion, Retrieval-Augmented Generation, Multilingual NLP, AI Avatar, Voice Interaction, Government Scheme Recommendation, Explainable AI, Conversational AI, IndicTrans2, Flutter.

---

## 1. Introduction

Financial inclusion remains one of the most pressing development challenges in contemporary India. Despite the rapid expansion of digital banking infrastructure and government-led initiatives such as Jan Dhan Yojana, a large fraction of the adult population continues to lack meaningful access to financial products, advisory services, and awareness of entitled government schemes. The barriers are not merely infrastructural; they are linguistic, cognitive, and psychological. A semi-literate farmer in rural Tamil Nadu and an urban informal-sector worker in Bengaluru face fundamentally different but equally formidable obstacles when attempting to navigate a banking system designed around English-language documentation and formal financial literacy.

Recent advances in large language model (LLM) technology, multilingual neural machine translation, and real-time speech processing have created an opportunity to bridge this gap through conversational AI. Systems capable of conducting naturalistic dialogue in regional languages, interpreting intent from imprecise or colloquial utterances, and translating complex financial terminology into accessible explanations hold the potential to function as a financial guide for populations historically excluded from such services.

In this paper, we present a complete architecture for a Multilingual AI Financial Inclusion Assistant — a system that accepts voice or text input in four Indian languages, retrieves relevant financial scheme information through a RAG pipeline, and delivers personalised recommendations via text, voice, or an animated human avatar. The design addresses language barriers, technical jargon, variable literacy levels, and the trust deficit that many users associate with formal financial institutions.

The remainder of this paper is organised as follows: Section 2 reviews related work; Section 3 states the problem formally; Section 4 articulates the system objectives; Section 5 describes the methodology and architecture; Section 6 details implementation; Section 7 analyses system performance; Section 8 discusses implications; Section 9 concludes; and Section 10 identifies directions for future work.

---

## 2. Literature Review

Research in conversational AI for financial services and multilingual NLP for low-resource languages constitutes the primary intellectual context for this work.

The application of LLMs to financial question-answering has been explored through domain-specific fine-tuning and RAG-based approaches. RAG, first formalised by Lewis et al. (2020), augments a frozen LLM with a retrieval mechanism that fetches relevant documents from an external knowledge base at inference time, reducing hallucinations and enabling up-to-date domain knowledge without retraining. Subsequent work demonstrated the effectiveness of RAG for enterprise knowledge management and FAQ systems, establishing its suitability for the scheme-recommendation task addressed here.

Multilingual speech processing for Indian languages has advanced considerably with the introduction of models such as Whisper (Radford et al., 2022), which achieves strong speech recognition across 99 languages including Hindi and Tamil, and IndicTrans2, a dedicated neural machine translation model for 22 scheduled Indian languages developed by AI4Bharat. These models collectively enable the voice pipeline described in Section 5.

AI avatar technology for user-facing conversational agents has been commercially explored by platforms such as D-ID and HeyGen, which provide APIs for generating lip-synced talking-head video from text-to-speech audio. The use of such avatars in rural financial literacy contexts has been proposed as a mechanism for increasing trust and accessibility among users with limited text literacy, a design principle adopted in this work.

Prior work on financial inclusion and technology in the Indian context has examined mobile banking adoption barriers, digital financial literacy interventions, and chatbot deployment in rural banking correspondents. This system synthesises and extends these threads by combining multilingual voice, avatar interaction, RAG-based recommendation, and explainable AI transparency into a single end-to-end platform.

---

## 3. Problem Statement

Despite policy-level efforts to promote financial inclusion in India, three persistent and interrelated challenges continue to limit effective access to financial services for a large segment of the population:

**i. Language and Literacy Barriers.** The majority of government scheme documentation, banking interfaces, and financial advisory materials are available only in English or, at best, in a limited subset of regional languages. Citizens who are not English-literate — or who are semi-literate in any language — are effectively excluded from self-directed financial navigation.

**ii. Technical Jargon and Cognitive Complexity.** Financial products and government scheme eligibility criteria are described in terminology that is opaque even to educated users. The absence of a trusted, accessible intermediary that can translate these concepts into plain, contextually appropriate language represents a significant barrier to informed decision-making.

**iii. Information Fragmentation and Scheme Unawareness.** Government financial schemes are administered across multiple ministries, updated frequently, and disseminated through channels that do not reach rural or semi-urban populations effectively. Eligible citizens routinely fail to enroll in schemes to which they are entitled due to simple lack of awareness.

This work addresses all three challenges through a unified conversational AI platform that is multilingual, voice-first, jargon-free, and continuously updated with scheme data.

---

## 4. Objectives

The specific objectives of this research are:

1. To design and implement a multilingual conversational AI system capable of accepting user input in English, Hindi, Tamil, and Kannada via text and voice modalities.
2. To construct a RAG pipeline over a curated database of government financial schemes, insurance products, loans, and pension plans, enabling accurate and up-to-date scheme recommendation.
3. To integrate an AI avatar interface with real-time lip-sync animation to support voice-first interaction for users with limited text literacy.
4. To develop a hybrid recommendation engine combining gradient-boosted ML ranking with LLM-generated natural language explanations, providing both precision and interpretability.
5. To deploy the system on a cloud infrastructure that satisfies financial data security and privacy requirements, including PCI-DSS compliance and end-to-end encryption.
6. To evaluate system performance in terms of response latency, recommendation accuracy, and user accessibility across the target demographic.

---

## 5. Methodology

### 5.1. System Architecture Overview

The system is organised as eight loosely coupled modules communicating over RESTful APIs and an asynchronous message queue. The frontend mobile application (Flutter, Android and iOS) presents three interaction screens — manual chat, voice conversation, and avatar video — and communicates with a FastAPI backend server. The backend orchestrates authentication, voice processing, LLM inference, recommendation, multilingual translation, avatar generation, and database operations.

### 5.2. Retrieval-Augmented Generation Pipeline

Rather than relying on the parametric knowledge of a base LLM, the system adopts a Retrieval-Augmented Generation approach. A curated corpus of government scheme descriptions, eligibility criteria, application procedures, and financial product specifications is ingested into a vector database (Pinecone). At inference time, the user query — after translation into English if necessary — is embedded and used to retrieve the top-k most semantically relevant scheme documents. These retrieved documents are prepended to the LLM prompt as grounding context, enabling the model to generate accurate, source-attributed recommendations without hallucinating scheme details. The RAG architecture supports incremental corpus updates, so newly announced schemes can be indexed without retraining the underlying model.

### 5.3. Multilingual Speech Pipeline

Voice input is streamed from the mobile client as audio chunks. The Whisper speech recognition model transcribes the audio to text in the detected source language. If the source language is not English, the IndicTrans2 translation model converts the transcript to English for LLM processing. The LLM response is generated in English, translated back to the user's selected language via IndicTrans2, and synthesised to speech using the ElevenLabs text-to-speech API. The full pipeline — speech recognition, translation, LLM inference, back-translation, and TTS — is executed asynchronously to achieve end-to-end latency of one to three seconds.

### 5.4. AI Avatar Interface

For users who benefit from visual, face-to-face interaction, the system integrates an AI avatar rendered using the D-ID or HeyGen API. The TTS audio generated in Step 5.3 is passed to the avatar API, which returns a short video clip of a human-like face with synchronized lip movement and facial expressions. This video is streamed to the mobile client and displayed alongside interactive scheme information cards. The avatar modality is designed specifically for rural users who may be intimidated by text-based interfaces but respond positively to personified agents.

### 5.5. Hybrid Recommendation Engine

Scheme recommendation combines two complementary approaches. An XGBoost classifier, trained on historical scheme eligibility data, ranks candidate schemes by predicted relevance given the user's demographic and financial profile (age, income, occupation, savings goal, location). The top-ranked schemes are then passed to the LLM, which generates a natural language explanation of why each scheme is suitable for the specific user, expressed in simple, jargon-free language. This hybrid design ensures both ranking precision and communicative clarity.

### 5.6. Data Collection and Maintenance

The scheme knowledge base is populated through a combination of web scraping (Scrapy) of official government portals — including MyScheme.gov.in, Jan Dhan Darshak, and individual ministry websites — and manual curation. Scraped scheme data is parsed, normalised, and stored in a PostgreSQL relational database. Embedding vectors are computed for each scheme document using a sentence-transformer model and indexed in Pinecone. A scheduled data refresh pipeline runs weekly to incorporate newly announced schemes and updated eligibility criteria.

---

## 6. Implementation

### 6.1. Technology Stack

The complete technology stack is summarised in Table I.

**Table I: System Technology Stack**

| Component | Technology | Purpose |
|---|---|---|
| Frontend | Flutter | Cross-platform mobile app (Android & iOS) |
| Backend | FastAPI (Python) | API server, LLM orchestration, auth |
| Relational DB | PostgreSQL | User profiles, session logs |
| Vector DB | Pinecone | Semantic search over scheme corpus |
| Cache | Redis | Session state, response caching |
| LLM Engine | GPT / Llama 3 + RAG | Intent understanding, explanation |
| Speech-to-Text | Whisper | Multilingual voice transcription |
| Translation | IndicTrans2 | Indian language translation |
| Text-to-Speech | ElevenLabs | Natural voice synthesis |
| Avatar | D-ID / HeyGen | Lip-sync talking avatar video |
| ML Recommender | XGBoost | Scheme ranking by user profile |
| Data Collection | Scrapy | Government scheme web scraping |
| Cloud | AWS (EC2, RDS, S3, Lambda, ECS) | Scalable cloud deployment |

### 6.2. Interaction Modes

Three interaction modes are implemented and selectable by the user on application launch:

- **Manual Chat:** The user enters demographic and financial details (age, income, occupation, savings goal, insurance needs, pension requirements) via a structured form. The backend constructs a profile vector, queries the recommendation engine, retrieves relevant scheme documents via RAG, and generates a personalised recommendation summary.
- **Voice Conversation:** The user speaks naturally in their chosen language (e.g., "I am a farmer and I need government support for crop insurance"). The voice pipeline transcribes, translates, processes, and responds in the same language with synthesised speech output.
- **AI Avatar Video Assistant:** A human-like avatar appears on screen and speaks the system's response with lip-sync animation. Interactive scheme cards are displayed below the video, each showing the scheme name, eligibility summary, benefit amount, and an application deep-link.

### 6.3. Security Implementation

All API endpoints are protected with JWT-based authentication. Sensitive user data — income figures, Aadhaar-linked identifiers, and banking details — are encrypted at rest using AES-256 and in transit via TLS 1.3. The system is designed for PCI-DSS compliance, with API keys managed through AWS Secrets Manager and regular automated security audits. User consent is obtained at onboarding, and data retention policies comply with applicable Indian data protection regulations.

### 6.4. Real-Time Response Pipeline

The end-to-end real-time pipeline for avatar response proceeds as follows: (1) the frontend streams voice audio chunks to the backend; (2) Whisper transcribes the audio stream in real time; (3) IndicTrans2 translates to English if required; (4) the LLM processes intent and generates a recommendation; (5) the recommendation is translated back to the user's language; (6) ElevenLabs synthesises speech; (7) the D-ID/HeyGen API renders a lip-synced avatar video clip; and (8) the video and scheme cards are streamed to the client. Total response latency is maintained between one and three seconds under normal load conditions.

---

## 7. Results & Analysis

### 7.1. Recommendation Accuracy

The hybrid recommendation engine was evaluated against a curated test set of 200 user profiles with known eligible schemes verified by domain experts. The XGBoost ranking model achieved a top-3 scheme recall of 91.4%, meaning that in over nine of ten cases, the correct eligible scheme appeared within the top three recommendations returned to the user. LLM-generated explanations were rated as "clear and jargon-free" by 87% of evaluators from the target demographic.

### 7.2. Multilingual Performance

Speech recognition accuracy (word error rate) was evaluated across all four supported languages on a held-out set of 500 utterances per language. Whisper achieved word error rates of 4.2% for English, 6.8% for Hindi, 9.1% for Tamil, and 10.3% for Kannada, consistent with published benchmarks for the model. IndicTrans2 translation quality, measured by BLEU score on a financial domain test set, reached 38.4 for Hindi-English and 33.1 for Tamil-English, which is considered adequate for intent-extraction purposes.

### 7.3. Latency

End-to-end response latency was measured across 1,000 simulated interactions under typical AWS deployment load. Mean latency was 1.7 seconds (standard deviation 0.4 seconds), with 95th percentile latency at 2.8 seconds, satisfying the target of 1–3 seconds. Avatar video generation introduced an additional 0.8–1.2 seconds of rendering latency, handled asynchronously and streamed progressively to avoid perceptible delay.

### 7.4. Comparative Feature Analysis

**Table II: Comparison with Existing Financial Assistance Systems**

| Feature | Existing Systems | This System |
|---|---|---|
| Language Support | English only | English, Hindi, Tamil, Kannada |
| Explanation Quality | Scheme names only | Human-language plain explanations |
| Interaction Mode | Text-based only | Text, Voice, and AI Avatar Video |
| Accessibility | Requires reading | Fully voice-enabled for low-literacy users |
| AI Transparency | Opaque (black-box) | Explainable with cited sources |
| User Experience | Transactional | Conversational and empathetic |
| Cultural Fit | Generic | India-specific financial knowledge base |

---

## 8. Discussion

The results confirm that a RAG-based multilingual conversational AI system can deliver accurate, accessible, and timely financial guidance to populations currently underserved by conventional banking and advisory services. The combination of voice input, regional language support, and avatar-mediated interaction addresses the three key exclusion barriers identified in Section 3 — language, jargon, and information fragmentation — within a single platform.

The choice of RAG over fine-tuning is particularly well-suited to this domain. Government schemes change frequently; a fine-tuned model's parametric knowledge becomes stale between training cycles, whereas the RAG corpus can be updated incrementally without retraining. The explainability afforded by surfacing retrieved source documents also aligns with the trust requirements of a financial advisory context, where users benefit from knowing the basis of a recommendation.

The avatar modality warrants particular attention. Qualitative evaluation sessions with rural users — conducted in collaboration with a rural banking correspondent network — indicated markedly higher engagement and trust when financial information was delivered by a human-like avatar speaking in the user's language, compared to text-only or disembodied voice interfaces. This finding is consistent with prior research on anthropomorphic agents in human-computer interaction and suggests that avatar-mediated delivery may be essential, rather than merely supplementary, for the target demographic.

One important operational consideration is the cost of avatar video rendering via third-party APIs (D-ID/HeyGen), which introduces a per-interaction cost that must be managed at scale. Future deployment at the scale of millions of users will require either bulk API agreements, self-hosted open-source avatar models, or a tiered interaction model that reserves avatar delivery for high-value interaction moments.

---

## 9. Conclusion

A complete architecture for a Multilingual AI Financial Inclusion Assistant has been designed, implemented, and evaluated. The system combines retrieval-augmented generation over a curated financial scheme corpus, multilingual voice processing for four Indian languages, a hybrid ML-plus-LLM recommendation engine, and an AI avatar interface with lip-sync animation. End-to-end response latency is maintained within three seconds; scheme recommendation recall exceeds 91% at top-3; and multilingual speech recognition achieves word error rates consistent with state-of-the-art benchmarks across all supported languages.

The system directly addresses the language, literacy, and information-access barriers that exclude over 500 million Indians from meaningful financial participation. By transforming complex financial knowledge into accessible, voice-first, empathetic conversation in regional languages, the platform holds significant potential for social impact across the agricultural, informal-sector, and rural demographic segments most in need of financial guidance.

The architecture is designed to be extensible: new languages, additional scheme domains (e.g., healthcare, education subsidies), and improved LLM or avatar backends can be integrated without structural re-engineering of the platform.

---

## 10. Future Scope

Building on the results of this work, several directions for future investigation are identified:

- **Language Expansion:** Extension of the multilingual pipeline to additional scheduled Indian languages — including Bengali, Marathi, Telugu, Malayalam, and Odia — would substantially broaden the system's demographic reach. IndicTrans2's 22-language coverage provides a direct pathway to this expansion.
- **Offline and Low-Bandwidth Operation:** Deployment in rural India is constrained by intermittent network connectivity. Quantised on-device LLM inference (e.g., using Llama.cpp on mobile) and cached scheme embeddings could enable partial offline functionality for the most common query types.
- **Proactive Scheme Alerts:** Rather than responding only to user queries, the system could proactively notify users of newly announced schemes for which their stored profile indicates eligibility, transforming the assistant from a reactive to a proactive financial inclusion tool.
- **Fine-Tuned Domain LLM:** Training or fine-tuning a smaller LLM specifically on Indian financial domain text — scheme documentation, RBI circulars, SEBI guidelines, insurance policy documents — could improve both accuracy and response quality while reducing inference costs relative to large general-purpose models.
- **User Behaviour Analytics:** An analytics dashboard aggregating anonymised interaction patterns, most-queried schemes, and language distribution would enable government agencies and financial institutions to identify underserved populations and under-communicated schemes, informing policy interventions.
- **Academic Research Publications:** The system's contributions to multilingual NLP for low-resource languages, explainable AI in financial services, and voice-based HCI for semi-literate populations represent publishable findings that could influence fintech development across South Asia and other emerging markets.

---
