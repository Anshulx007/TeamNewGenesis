<<<<<<< HEAD

=======
# SahajAI – System Design Document

## Team Information
- Team Name: NewGenesis  
- Team Leader: Anshul Tyagi  
- Team Members:  
  - Saksham Agnihotri  
  - Shubh Aggarwal  
  - Neel Gupta
- Hackathon Theme: AI for Bharat (AWS)

---

## Table of Contents

- Architecture Overview  
- System Layers  
- Component Responsibilities  
- Technology Stack  
- Data Model & Relationships  
- Multilingual & Voice Design  
- Security & Privacy  
- Scalability & Future Enhancements  
- Design Decisions  
- Implementation Checklist  

---

## Architecture Overview

SahajAI is a modular, AI-powered citizen services platform designed around:

- Retrieval Augmented Generation (RAG) for verified policy answers  
- Graph-based Document Dependency Intelligence for mapping document pathways  
- Voice-first and multilingual interaction for accessibility  
- Location-based service discovery for nearest office guidance  

The system supports both:
- A low-cost hackathon MVP implementation  
- A scalable, production-grade AWS architecture  

---

## System Layers

### User Interface Layer
- Web Application (React)  
- Chat Interface (Web / Telegram)  
- Voice Interface (Microphone + Speaker)  
- Language Selector (Hindi, English, Regional)  

Responsibilities:
- Capture text and voice queries  
- Capture preferred language  
- Display AI responses and checklists  
- Play spoken guidance  

---

### API & Backend Layer
- API Gateway  
- Backend Service (FastAPI / Node.js)  

Responsibilities:
- Route and validate requests  
- Maintain user session context  
- Pass language preferences  
- Orchestrate calls to AI, dependency engine, and location service  

---

### AI & RAG Layer (Multilingual)
Components:
- Multilingual Large Language Model (LLM)  
- Vector Database for embeddings  
- Policy & Scheme Knowledge Base  

Responsibilities:
- Retrieve verified scheme data  
- Perform semantic search  
- Ground AI responses  
- Generate localized explanations  

---

### Document Dependency Intelligence Engine (Core USP)
Graph-based reasoning engine that models:

- Scheme → required documents  
- Document → prerequisite documents  

Responsibilities:
- Traverse document dependency graph  
- Generate complete document pathways  
- Ensure no dead ends in documentation  
- Output human-readable step sequences  

---

### Location & Office Discovery Service
Responsibilities:
- Map pincode to district  
- Identify nearest:
  - CSC centers  
  - Tehsil offices  
  - Aadhaar centers  
  - Other issuing authorities  
- Return office details in selected language  

---

### Form Assistance Module
Responsibilities:
- Define form schemas  
- Guide users field-by-field  
- Validate user input  
- Generate pre-filled form previews (PDF or structured output)  

---

### Voice Services Layer (Multilingual)
Components:
- Speech-to-Text (STT)  
- Text-to-Speech (TTS)  

Responsibilities:
- Convert spoken input to text  
- Convert AI output to speech  
- Support multiple Indian languages  
- Enable voice-first experience  

---

## Component Responsibilities

| Component                  | Responsibility                                      |
|---------------------------|------------------------------------------------------|
| Web / Chat UI             | User interaction, language selection, display         |
| Voice Interface           | Multilingual voice capture and playback               |
| Backend API               | Request orchestration + session context               |
| RAG Engine                | Multilingual retrieval of policy content              |
| LLM                        | Multilingual simplified responses                     |
| Vector Database            | Semantic search on policy documents                   |
| Document Dependency Engine | Traverse document dependency graph                   |
| Graph Database             | Store document relationships                          |
| Location Service           | Find nearest CSC / office                             |
| Form Assistance Module     | Multilingual form guidance and validation              |

---

## Technology Stack

### Hackathon MVP (Low-Cost / Free)
- LLM: Ollama / Groq API (multilingual)  
- Vector DB: ChromaDB / FAISS  
- Graph: Neo4j Community / NetworkX  
- Backend: FastAPI / Node.js  
- UI: React Web  
- Voice STT: Whisper  
- Voice TTS: gTTS / Coqui TTS  
- Storage: Local FS / S3 Free Tier  

### Production (Final AWS Architecture)
- LLM: Amazon Bedrock  
- Vector DB: Amazon OpenSearch  
- Graph DB: Neo4j Aura / EC2-hosted Neo4j  
- Backend: AWS Lambda + API Gateway  
- Voice STT: AWS Transcribe  
- Voice TTS: AWS Polly  
- Storage: Amazon S3 + DynamoDB  

---

## Data Model & Relationships

| From Entity | Relationship | To Entity |
|--------------|--------------|-----------|
| Scheme       | requires     | Document  |
| Document     | requires     | Document  |
| Document     | issued_by    | Office    |
| Office       | located_in   | Location  |
| User         | located_in   | Location  |

---

## Multilingual & Voice Design

- All user interactions support language selection  
- Language context passed through backend to AI services  
- Multilingual embeddings used for vector search  
- Voice STT and TTS operate in selected language  
- Fallback to text if voice fails  

---

## Security & Privacy

- No storage of official identity documents  
- Minimal temporary handling of form data  
- No access to private government systems  
- Session-based data only  
- Compliance with basic data minimization principles  

---

## Scalability & Future Enhancements

- Integration with official government APIs  
- WhatsApp Business integration  
- OCR for scanned document uploads  
- User profiles for proactive scheme suggestions  
- Real-time policy update alerts  
- Expanded regional language coverage  

---

## Design Decisions

- RAG chosen to ensure grounded, verified responses  
- Graph-based model enables true document pathway reasoning  
- Voice-first design improves accessibility for Bharat users  
- Modular architecture allows independent scaling of services  

---

## Implementation Checklist

- [x] Define system architecture  
- [x] Design RAG pipeline  
- [x] Design document dependency graph model  
- [x] Design multilingual and voice pipeline  
- [x] Design nearest office lookup logic  
- [x] Define form assistance workflow  
- [ ] Implement backend APIs  
- [ ] Integrate LLM and vector DB  
- [ ] Implement graph traversal logic  
- [ ] Implement UI and voice interface  
- [ ] End-to-end testing and demo setup  
>>>>>>> 03f8bc4 (comit1)
