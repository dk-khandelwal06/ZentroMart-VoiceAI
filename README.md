\# ZentroMart — Voice AI Support Agent



\*\*VoiceOps 2026 Capstone | From Tokens to Transformers\*\*  

\*\*IIT Guwahati × Gnani.ai\*\*



\## Overview



ZentroMart Voice AI Support Agent is a voice-based customer support prototype designed to answer customer questions using a retrieval-augmented knowledge base and connect customer requests to mock business tools.



The project combines speech recognition, knowledge retrieval, conversation handling, and speech synthesis in a single pipeline.



\## Key Features



\- \*\*Speech-to-text:\*\* Transcribes customer audio using Gnani.ai STT.

\- \*\*Knowledge retrieval:\*\* Uses sentence embeddings and a FAISS index to retrieve relevant knowledge-base passages.

\- \*\*Customer support conversation:\*\* Handles policy questions and order-related requests.

\- \*\*Order verification:\*\* Requires an approved verification value before disclosing protected order information.

\- \*\*Ticket creation:\*\* Integrates with the supplied mock ticket tool.

\- \*\*Text-to-speech:\*\* Generates a spoken response using Gnani.ai TTS.

\- \*\*Source output:\*\* Saves retrieved source information alongside the response for inspection.



\## Architecture



1\. Customer audio is provided to the voice pipeline.

2\. Gnani.ai STT converts the audio into text.

3\. The conversation agent processes the customer request.

4\. The RAG pipeline retrieves relevant passages from the knowledge base.

5\. The agent responds to the customer and invokes mock business tools when appropriate.

6\. Gnani.ai TTS generates an audio response.

7\. The pipeline saves the transcript, response, audio, sources, and run metadata.



\## Technology Stack



\- Python

\- Gnani.ai STT and TTS

\- Sentence Transformers

\- FAISS

\- Pandas and NumPy

\- Google GenAI SDK

\- Python dotenv



\## Project Structure



```text

ZentroMart-VoiceAI/

├── src/

│   ├── baseline.py

│   ├── conversation\_agent.py

│   ├── evaluate\_baseline.py

│   ├── rag\_chatbot.py

│   ├── rag\_pipeline.py

│   └── voice\_pipeline.py

├── sample\_audio/

├── sample\_outputs/

├── outputs/

│   ├── baseline\_results.csv

│   └── rag\_index/

├── reports/

├── docs/

├── .env.example

├── .gitignore

├── requirements.txt

├── run.py

└── README.md

```



\## Setup



\### 1. Create and activate a virtual environment



```bash

python -m venv .venv

```



Windows CMD:



```cmd

.venv\\Scripts\\activate

```



\### 2. Install dependencies



```bash

python -m pip install -r requirements.txt

```



\### 3. Configure environment variables



Create a local `.env` file based on `.env.example` and provide the API keys required by the integrations.



\*\*Never commit `.env` or expose API keys in source code, screenshots, logs, or a public repository.\*\*



\### 4. Configure the dataset



Extract the supplied VoiceOps capstone dataset and ensure the application can access its knowledge-base documents and mock tools. Update the dataset path in the source configuration if the dataset is located somewhere other than the path used during development.



\### 5. Run the voice pipeline



With a supported sample audio file in `sample\_audio/`, run:



```bash

python run.py

```



The pipeline processes the input audio and writes the generated transcript, response, audio, source information, and run metadata to `sample\_outputs/`.



Check `python run.py --help` if you need to inspect the supported command-line options.



\## Security and Reliability



\- Protected order details should only be disclosed after successful identity verification.

\- Ticket creation should be confirmed using the mock tool's returned status.

\- Customer-facing policy responses should be grounded in the applicable knowledge-base documents.

\- Superseded policy documents should not be treated as current policy.

\- API keys and private customer data must not be committed to version control.



\## Limitations



This is a capstone prototype using a supplied dataset and mock business tools. Its behavior depends on the availability of the configured dataset, API credentials, and external speech services. Responses and tool outcomes should be validated before use in a production customer-support environment.



\## Deliverables



The repository contains the application source code, setup instructions, generated project artifacts, and sample voice-pipeline outputs. Refer to the `reports/` and `docs/` directories for the final submission materials.



