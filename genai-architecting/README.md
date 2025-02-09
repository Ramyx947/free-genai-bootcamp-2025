# Designing a Romanian-Learning LLM Architecture

## Table of Contents
1. [Rationale for On-Premise Infrastructure](#1-rationale-for-on-premise-infrastructure)
2. [Romanian-Specific Constraints](#2-romanian-specific-constraints)
3. [High-Level Architecture](#3-high-level-architecture)
4. [Infrastructure & Hardware Investment](#4-infrastructure--hardware-investment)
5. [Functional Requirements](#5-functional-requirements)
6. [Orchestration & Security Best Practices](#6-orchestration--security-best-practices)
7. [End-to-End Workflow](#7-end-to-end-workflow-romanian-example)
8. [Adaptations for Learning Apps](#8-adaptations-for-learning-apps)
9. [Implementation Tips for Romanian](#9-implementation-tips-for-romanian)
10. [Summary](#10-summary)

This proposal outlines an end-to-end solution for a **self-hosted, AI-driven Romanian language tutor**. It consolidates **technical**, **functional**, and **infrastructure** requirements to ensure privacy, predictable costs, and robust linguistic coverage for up to 300 learners.

---

# 1. Rationale for On-Premise Infrastructure

### Privacy & Data Control
- The organization plans to **own and manage** its AI hardware to **fully control** learner data and conversation logs.  
- This approach addresses **privacy concerns** and reduces potential legal or regulatory complications tied to third-party cloud services.

### Cost Predictability
- **Cloud-based GenAI services** may become increasingly expensive.  
- By purchasing a dedicated **AI PC** (budget \$10k–\$15k), the team ensures **long-term cost stability** without external provider fluctuations.

### Performance Expectations
- The single on-premise server is projected to serve around **300 active students** in Nagasaki with adequate **internet bandwidth** to handle real-time interactions.

[Back to Table of Contents](#table-of-contents)

# 2. Romanian-Specific Constraints

### Fewer Publicly Available Datasets
Romanian lacks the extensive open-source dataset ecosystem available for English or Japanese. This highlights the need for **curated educational resources** (grammar lessons, dialogues, reading passages).

### Morphological Complexity
Romanian involves **cases** (nominative, accusative, dative, genitive), **rich verb conjugations**, and **diacritics** (ă, â, î, ș, ț). Any LLM must be trained (or fine-tuned) on **linguistically annotated** data to master these nuances.

### Cultural Context and Formality
- Switching between **informal (“tu”)** and **formal (“dumneavoastră”)** usage is crucial.  
- Designing **role-play scenarios** or toggles for different registers ensures the app caters to real-world language dynamics.

### Speech-to-Text Gaps
- **Romanian ASR** offerings are limited.  
- **Open-source frameworks** (e.g., Whisper, XLS-R) may require extra fine-tuning for accurate recognition and real-time feedback.

For more details on Romanian language characteristics, see the document: [Romanian-language-characteristics.md](../docs/Romanian-language-characteristics.md).

[Back to Table of Contents](#table-of-contents)

# 3. High-Level Architecture

### Frontend (User Interface)
- A **web or mobile** application enabling two-way communication in Romanian.  
- Potential role-playing modules for **daily-life dialogues** and **multiple character interactions**.

### Backend (LLM API & Orchestration Layer)
- **API server** (FastAPI, Flask, or Express.js) that:
  1. Leverages **RAG** to retrieve relevant grammar or vocabulary  
  2. Invokes a **fine-tuned LLM** for natural-language generation  

### AI & NLP Layer

#### RAG (Retrieval-Augmented Generation)
- Uses a **vector database** (FAISS, Weaviate, Pinecone, or ChromaDB) with curated Romanian resources.  
- Reduces hallucination by anchoring answers in authorized educational materials (paid/licensed).

#### Romanian LLM (Fine-Tuned for Education)
- Candidates include **OpenLLM-Ro**, a **Llama-2** Romanian derivative, or a **multilingual Mistral** model.  
- Must respect **diacritics**, handle **formal/informal** registers, and integrate seamlessly with RAG outputs.

For a more detailed analysis of using RAG and fine-tuning for language learning, see the document: [RAG-LLM-fine-tuning.md](../docs/RAG-LLM-fine-tuning.md).

#### Speech-to-Text (Optional)
- **Whisper** (fine-tuned for Romanian) or **XLS-R** to support pronunciation and spoken exercises.

#### Guardrails & Pre-/Post-Processing
- Filters out disallowed queries and enforces grammatical correctness.  
- Incorporates clarifications, such as “sunt” vs. “ești,” or diacritic prompts.

For extra details on the LLM architecture, see the document: [romanian-llm-architecture.md](../docs/romanian-llm-architecture.md).

[Back to Table of Contents](#table-of-contents)

# 4. Infrastructure & Hardware Investment

### Self-Hosted AI PC
- Budget of **\$10k–\$15k** to purchase a GPU-accelerated server for local inference:
  - Ensures direct data oversight and cost predictability.
  - Targets **300 concurrent learners** for real-time responses.

### Data Protection and Compliance
- All **grammar lessons**, dialogues, and reading passages are stored **on-prem** in a secure database.  
- Only authenticated users can access these materials, preventing unauthorized distribution or copyright violations.

[Back to Table of Contents](#table-of-contents)

# 5. Functional Requirements

1. **Licensed & Purchased Materials**  
   - To avoid copyright issues, the platform will incorporate legitimate, purchased educational resources.  
   - The RAG pipeline references locally stored data for grammar rules, vocabulary, and reading passages.

2. **Model Selection & Deployment**  
   - Evaluating **IBM Granite** (or similar open-source solutions) with **traceable training data** to ensure compliance.  
   - The primary requirement is the ability to **run on-prem** under the hardware and budget constraints, with feasible inference speeds.

3. **Open-Source Flexibility**  
   - Additional LLMs may be tested, provided they meet transparency standards regarding training data.  
   - This ensures the system avoids hidden compliance pitfalls and potential licensing risks.

[Back to Table of Contents](#table-of-contents)

# 6. Orchestration & Security Best Practices

### Containerization & Deployment
- **Docker** or **Kubernetes** can be used to package and deploy the LLM, RAG services, and vector databases.  
- This enables **consistent builds**, simpler upgrades, and smooth scaling if future user numbers grow.

### Access Control & Authentication
- Integrate **Role-Based Access Control (RBAC)** for administrative dashboards.  
- Enforce user authentication (e.g., **OAuth** or **JWT tokens**) so only enrolled students and authorized personnel can access AI services.

### Encryption & Data Handling
- **Encrypt in transit** (HTTPS/TLS) and **at rest** (disk-level encryption) to protect educational materials and user data.  
- Implement **key management** procedures for secure handling of credentials and encryption keys.

### Network Segmentation
- Keep the **AI server** and **vector database** on a protected subnet.  
- Only expose essential API endpoints to the internet, reducing the attack surface.

### Logging & Auditing
- Log **LLM queries**, retrieval steps, and system events in a **centralized log repository**.  
- Audit logs regularly for anomalies or unauthorized access attempts.

### Monitoring & Alerting
- Use tools like **Prometheus**, **Grafana**, or **ELK Stack** to monitor system health, GPU utilization, and latency.  
- Set up alerts for resource spikes or repeated request failures to maintain availability.

### Disaster Recovery
- Maintain **offline backups** of the vector database and user data.  
- Test restoration procedures to ensure quick recovery from hardware failures or data corruption.

[Back to Table of Contents](#table-of-contents)

# 7. End-to-End Workflow (Romanian Example)

1. **Learner Query**  
   - A user asks: “Cum conjug verbul ‘a merge’ la prezent?”  
2. **API Preprocessing**  
   - Basic transformations (lowercasing, diacritic checks).  
3. **RAG Retrieval**  
   - Embeds the query; searches the vector DB for “a merge” conjugation rules.  
   - Returns matching grammar references (e.g., “Eu merg, tu mergi, etc.”).  
4. **LLM Generation**  
   - Integrates user query + retrieved references; outputs a concise explanation.  
5. **Guardrails & Formatting**  
   - Validates correctness; adds clarifications where needed.  
6. **Response**  
   - The user sees the final, diacritically correct breakdown of the verb.

[Back to Table of Contents](#table-of-contents)

# 8. Adaptations for Learning Apps

### Daily Life Visual Novel
- Realistic dialogues in **Romanian cities** (e.g., Bucharest, Cluj).  
- Emphasize polite vs. casual speech and multiple character interactions.

### Romanian Text Adventure
- Dynamic narrative introducing **vocabulary** and **grammatical structures**.  
- Corrects player inputs in real time.

### Romanian Sentence Constructor
- Guides learners in **building** Romanian sentences from English prompts.  
- Reinforces morphological and diacritic usage.

### Subtitles to Vocabulary
- Takes **Romanian subtitles** as input, extracting key terms and morphological tags.

### Speech to Learn
- Offers single words or phrases for **pronunciation** checks.  
- Uses local ASR (Whisper or XLS-R) for feedback.

[Back to Table of Contents](#table-of-contents)

# 9. Implementation Tips for Romanian

### Curate High-Quality Datasets
Given the limited public resources, preparing **custom educational content** is essential. Thorough **morphological annotation** significantly improves accuracy.

### Fine-Tune vs. Multilingual
Assess whether a **multilingual** model suffices or if deeper **fine-tuning** on Romanian data is required—especially for advanced grammar corrections or formal/informal toggling.

### Formal/Informal Toggle
Allow switching between **"tu"** and **"dumneavoastră"** modes to accommodate different social registers.

### Diacritic Enforcement
Prompt learners (and the model) to include Romanian diacritics. Offer **user-friendly corrections** if missing.

### Guardrails & QA
Leverage **Romanian language experts** for final validation. Ensure the system doesn't inadvertently revert to outdated forms (e.g., "sînt").

### RAG for Content Depth
With all licensed materials hosted locally, RAG ensures direct referencing of **official texts**—minimizing misinformation.

[Back to Table of Contents](#table-of-contents)

# 10. Summary

By combining **on-premise AI hardware** (to reduce ongoing operational costs and enhance data privacy) with **open-source Romanian LLM solutions**, this architecture addresses:
- **Privacy & Compliance**: The organization fully controls data and content usage.  
- **Cost Stability**: A one-time investment in hardware (\$10k–\$15k) replaces monthly cloud fees.  
- **Language Nuances**: Through curated datasets, morphological annotations, and diacritic enforcement, the system can provide advanced Romanian-language tutoring.  

**IBM Granite** and other open-source models with **traceable training data** are strong candidates under these constraints. Deploying the infrastructure with **containerization** and robust **security measures** further ensures a scalable, maintainable solution that meets privacy and performance standards.
