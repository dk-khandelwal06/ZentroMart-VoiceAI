# <div align="center">🛒 ZentroMart — Voice AI Support Agent</div>

<div align="center">

### 🎙️ From Tokens to Transformers | VoiceOps 2026 Capstone

**IIT Guwahati × Gnani.ai**

An intelligent voice-based customer support prototype combining speech recognition, retrieval-augmented generation, and speech synthesis.

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Voice_AI-FFB800?style=for-the-badge&logo=googleassistant&logoColor=black" alt="Voice AI"/>
  <img src="https://img.shields.io/badge/RAG-6C5CE7?style=for-the-badge&logo=databricks&logoColor=white" alt="RAG"/>
  <img src="https://img.shields.io/badge/Gnani.ai-111111?style=for-the-badge&logoColor=white" alt="Gnani.ai"/>
</p>

[🚀 Explore Repository](https://github.com/dk-khandelwal06/ZentroMart-VoiceAI) · [👨‍💻 Developer Profile](https://github.com/dk-khandelwal06) · [💼 LinkedIn](https://www.linkedin.com/in/daksh-khandelwal-b02748391/)

</div>

---

## 🌟 Overview

ZentroMart Voice AI Support Agent is a voice-based customer support prototype designed to answer customer questions using a knowledge base and connect customer requests to mock business tools.

The system brings together speech recognition, knowledge retrieval, conversation handling, order verification, ticket creation, and speech synthesis in one workflow.

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🎤 Speech-to-Text
Converts customer audio into text using Gnani.ai STT.

</td>
<td width="50%">

### 🧠 Knowledge Retrieval
Uses Sentence Transformers and FAISS to retrieve relevant knowledge-base passages.

</td>
</tr>
<tr>
<td width="50%">

### 🔐 Order Verification
Requires successful identity verification before protected order information is disclosed.

</td>
<td width="50%">

### 🎫 Ticket Creation
Connects customer requests to the supplied mock ticket-creation tool.

</td>
</tr>
<tr>
<td width="50%">

### 🔊 Text-to-Speech
Generates spoken customer-support responses using Gnani.ai TTS.

</td>
<td width="50%">

### 📚 Source Tracking
Saves retrieved source information alongside generated responses.

</td>
</tr>
</table>

## ⚙️ How It Works

<div align="center">

**🎙️ Customer Audio**  
↓  
**🗣️ Gnani.ai Speech-to-Text**  
↓  
**💬 Conversation Agent**  
↓  
**🔎 RAG Retrieval — Sentence Transformers + FAISS**  
↓  
**🛠️ Mock Business Tools — Verification & Tickets, When Needed**  
↓  
**🔊 Gnani.ai Text-to-Speech**  
↓  
**✅ Spoken Response + Saved Artifacts**

</div>

## 🧰 Technology Stack

<div align="center">

| Technology | Purpose |
|:---:|---|
| 🐍 Python | Core application |
| 🎙️ Gnani.ai STT | Speech recognition |
| 🔊 Gnani.ai TTS | Speech generation |
| 🧠 Sentence Transformers | Text embeddings |
| 🔎 FAISS | Similarity-based retrieval |
| 📊 Pandas & NumPy | Data processing |
| 🤖 Google GenAI SDK | Generative AI integration |
| 🔑 Python dotenv | Environment configuration |

</div>

## 📂 Project Structure

```text
ZentroMart-VoiceAI/
├── src/
│   ├── baseline.py
│   ├── conversation_agent.py
│   ├── evaluate_baseline.py
│   ├── rag_chatbot.py
│   ├── rag_pipeline.py
│   └── voice_pipeline.py
├── sample_audio/
├── sample_outputs/
├── outputs/
│   ├── baseline_results.csv
│   └── rag_index/
├── reports/
│   └── FINAL_REPORT.md
├── docs/
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/dk-khandelwal06/ZentroMart-VoiceAI.git
cd ZentroMart-VoiceAI
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows CMD:

```cmd
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure API Keys

Create a local `.env` file using `.env.example` as a reference, then add the API credentials required by the integrations.

**🔒 Never commit your `.env` file or publish API keys.**

### 5. Configure the Dataset

Extract the supplied VoiceOps capstone dataset and ensure the application can access its knowledge-base documents and mock tools. Update the dataset path in the source configuration if required.

### 6. Run the Voice Pipeline

Place a supported audio file in `sample_audio/`, then execute:

```bash
python run.py
```

Generated transcripts, text responses, audio responses, source information, and run metadata are saved in `sample_outputs/`.

## 🔐 Safety & Reliability

- Verify customer identity before disclosing protected order information.
- Confirm ticket creation using the mock tool's returned status.
- Ground customer-facing policy responses in the applicable knowledge base.
- Use current policy documents rather than superseded versions.
- Keep credentials and private customer information out of public version control.

## ⚠️ Limitations

This project is a capstone prototype that relies on the supplied dataset, configured API credentials, external speech services, and mock business tools. It is not represented as a production-ready customer-support system.

## 📑 Project Report & Demo Artifacts

- **Final Report:** [`reports/FINAL_REPORT.md`](reports/FINAL_REPORT.md)
- **Sample Transcript:** [`sample_outputs/customer_question_transcript.txt`](sample_outputs/customer_question_transcript.txt)
- **Sample Response:** [`sample_outputs/customer_question_reply.txt`](sample_outputs/customer_question_reply.txt)
- **Generated Voice Response:** [`sample_outputs/customer_question_reply.wav`](sample_outputs/customer_question_reply.wav)
- **Retrieved Sources:** [`sample_outputs/customer_question_sources.json`](sample_outputs/customer_question_sources.json)

---

<div align="center">

## 👨‍💻 About the Developer

<img src="https://img.shields.io/badge/Student-IIT%20Jodhpur-FFB800?style=for-the-badge" alt="IIT Jodhpur"/>
<img src="https://img.shields.io/badge/Field-Applied%20AI%20%26%20Data%20Science-6C5CE7?style=for-the-badge" alt="Applied AI and Data Science"/>

### **Daksh Khandelwal**

**B.S. in Applied Artificial Intelligence & Data Science**  
*Indian Institute of Technology Jodhpur (IIT Jodhpur)*

📧 **Email:** [dk.khandelwaliitj@gmail.com](mailto:dk.khandelwaliitj@gmail.com)

🐙 **GitHub:** [dk-khandelwal06](https://github.com/dk-khandelwal06)

💼 **LinkedIn:** [Connect with me](https://www.linkedin.com/in/daksh-khandelwal-b02748391/)

🌐 **Project Repository:** [ZentroMart-VoiceAI](https://github.com/dk-khandelwal06/ZentroMart-VoiceAI)

---

*Building practical AI solutions, one project at a time. 🚀*

⭐ If you find this project interesting, consider starring the repository!

</div>
