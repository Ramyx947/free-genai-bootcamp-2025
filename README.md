# free-genai-bootcamp-2025

This project is part of a GenAI bootcamp. The primary goal is to **design, prototype, and deploy AI-powered tools** for a Romanian Language Learning School, helping them **expand language offerings** and **enrich** students’ learning experiences outside of instructor-led classes.

---

## 1. Project Overview

- **Objective:**  
  Build a **self-hosted, privacy-focused** AI infrastructure to serve up to **300 active learners** in a Romanian language program.

- **Scope:**  
  - Provide **grammar and morphology explanations** (Romanian cases, diacritics, conjugations).  
  - Offer **contextual responses** for formal/informal communication practice.  
  - Possibly integrate **speech-to-text** for pronunciation and oral comprehension exercises.

### Why Romanian?
Romanian has **fewer open-source datasets** compared to major languages like English or Japanese, plus notable **morphological complexity** and **varying formality**. This highlights the importance of **tailored data curation** and specialized LLM capabilities. Additionally, as a **native Romanian speaker who speaks English daily**, I’m seeking a structured way to **practice and reconnect** with my mother tongue.

---

## 2. Self-Hosted Infrastructure

### Motivations
1. **Data Privacy**: The school wants direct ownership of student data and course materials.  
2. **Cost Stability**: Avoid escalating cloud fees by investing **\$10k–\$15k** in on-premise hardware (a GPU-accelerated AI PC).

### Planned Setup
- A single **AI server** in the school’s office with sufficient GPU power to handle real-time inference for ~300 students.
- **Local Database** storing *licensed or purchased* educational content to avoid copyright issues.

---

## 3. High-Level Architecture

1. **Frontend (React)**
   - A **React**-based web application that provides:
     - Chat-like interface for students to engage in Romanian dialogues.
     - Grammar corrections, morphological hints, or step-by-step feedback.
     - Optional **role-playing** modules for everyday language practice.

2. **Backend (Python + Flask)**
   - **Flask** server handles all API requests and manages:
     - **RAG** (Retrieval-Augmented Generation) logic to pull relevant materials from a vector database.
     - **LLM Inference** for generating natural-language responses, running locally on the AI PC.
   - Containerized with **Docker** for easy deployment and environment consistency.

3. **Data Storage & Knowledge Base**
   - **Vector Database** (FAISS, Pinecone, Weaviate, or ChromaDB) containing grammar notes, reading passages, and past Q&A.
   - **Relational or NoSQL DB** for user profiles, progress tracking, and subscription/authorization details.

4. **Security & Guardrails**
   - **Docker** to isolate and run all components in containers.
   - **Access control** (token-based auth) for users and staff.
   - **SSL/TLS** for data-in-transit encryption.

---

## 4. Key AI Techniques

### 4.1 Retrieval-Augmented Generation (RAG)
- Minimizes hallucinations by pulling from **verified Romanian educational content** (textbooks, grammar guides, licensed reading passages).

### 4.2 Romanian LLM (Fine-Tuned)
- Could be **OpenLLM-Ro** or **IBM Granite** or a **Llama-2** derivative, specialized in Romanian usage (diacritics, morphological structures).
- **Traceable Training Data** helps maintain compliance with local regulations and avoid undisclosed/unclear data sources.

### 4.3 Guardrails
- **Pre-/Post-processing** steps remove sensitive input, enforce grammar rules, and provide corrective feedback on morphological issues.
- Additional checks ensure **formal/informal usage** is followed depending on the conversation context (e.g., “tu” vs. “dumneavoastră”).

---

## 5. Functional Requirements

1. **Self-Hosted Environment**  
   - Deploy on an on-premise AI PC (\$10k–\$15k budget) to serve ~300 students in Nagasaki.
2. **Secure Handling of Licensed Materials**  
   - Store course materials in an **internal database**; integrate with RAG for lesson retrieval.  
   - While developing the MVP, no authentication is required.
3. **Accurate Romanian Linguistic Support**  
   - Respect **Romanian diacritics**, conjugations, and morphological nuances.  
   - Provide grammar breakdowns and morphological annotation.
4. **Scalability & Maintainability**  
   - Use **Docker** for containerized deployments.  
   - Logging and monitoring (Prometheus, Grafana, ELK) for performance insights.

---

## 6. Potential Learning Apps & Extensions

1. **Daily Life Visual Novel**  
   - Simulate real-life interactions in Romanian cities (Bucharest, Iasi, etc.)
   - Track multiple NPCs with distinct speech styles (formal, casual, regional idioms).
2. **Romanian Text Adventure**  
   - Introduce new vocabulary and grammar in an interactive storyline.  
   - Provide instant feedback on the user’s typed actions.
3. **Romanian Sentence Constructor**  
   - Show English sentences, guide learners to build the Romanian equivalent step by step.  
   - Reinforce morphological transformations (e.g., verb endings, diacritics).
4. **Subtitles to Vocabulary**  
   - Tag each with part of speech and morphological details.
5. **Speech to Learn**  
   - Present words or short phrases for pronunciation practice.

---

## 7. Additional Security & Orchestration Best Practices

- **Containerization with Docker**:  
  - Wrap both the Flask backend and the React frontend in Docker containers for consistent deployment.
- **Role-Based Access Control (RBAC)**:
  - Ensure each user (student, teacher, admin) has the appropriate permissions to interact with AI services.
- **Network Segmentation**:
  - Host the AI inference server in a protected subnet, exposing minimal endpoints.
- **Data Encryption**:
  - Use HTTPS/TLS for front-to-back communications.
  - Encrypt local databases at rest if hosting sensitive learner records.
- **Monitoring & Alerting**:  
  - Tools like Prometheus and Grafana for real-time resource usage (CPU, GPU, memory) and request latencies.
- **Regular Backups**:  
  - Maintain offline snapshots of the vector DB and user data to quickly restore in case of system failure.

---

## 8. Summary

By integrating **React** on the frontend, a **Flask** (Python) backend, and **Docker** for containerization, this solution:

- **Retains Full Ownership** of user data by running everything on a locally managed AI server.
- **Controls Costs** through a one-time hardware investment (\$10k–\$15k), avoiding monthly cloud fees.
- **Delivers Rich Romanian-Learning Features**, leveraging specialized LLM models and carefully curated content for grammar, diacritics, and formality practice.
- **Maintains Security & Compliance** with container orchestration, guarded endpoints, and encrypted data flows.

This approach empowers the Romanian Language Learning School to offer **dynamic, AI-driven** lessons while preserving data privacy and cost predictability.
