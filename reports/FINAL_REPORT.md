\# ZentroMart Voice AI Support Agent

\## VoiceOps 2026 Capstone — Final Report



\*\*Program:\*\* From Tokens to Transformers  

\*\*Organizers:\*\* IIT Guwahati × Gnani.ai  

\*\*Project:\*\* ZentroMart Voice AI Support Agent  

\*\*Date:\*\* 25 October 2026



\## 1. Problem Statement



Customer-support teams handle repetitive questions about business policies, order status, returns, and issue resolution. A voice-based assistant can make these interactions more accessible by converting customer speech into text, retrieving relevant knowledge, and responding with generated speech.



\## 2. Project Objective



Build a prototype voice-support agent that combines speech recognition, knowledge-base retrieval, conversational handling, mock business tools, and speech synthesis in one workflow.



\## 3. System Architecture



1\. \*\*Audio input:\*\* Accept a supported customer audio file.

2\. \*\*Speech recognition:\*\* Use Gnani.ai Speech-to-Text (STT) to transcribe the customer's request.

3\. \*\*Knowledge retrieval:\*\* Use Sentence Transformers embeddings and FAISS to retrieve relevant knowledge-base passages.

4\. \*\*Conversation handling:\*\* Process policy questions and order-related requests.

5\. \*\*Business tools:\*\* Use mock order lookup and ticket creation tools where appropriate.

6\. \*\*Speech generation:\*\* Use Gnani.ai Text-to-Speech (TTS) to generate an audio response.

7\. \*\*Output artifacts:\*\* Save the transcript, text response, audio response, retrieved sources, and pipeline metadata.



\## 4. Technology Stack



\- Python

\- Gnani.ai STT and TTS

\- Sentence Transformers

\- FAISS

\- Pandas and NumPy

\- Google GenAI SDK

\- Python dotenv



\## 5. Safety and Business Rules



\- Order information must not be disclosed before successful identity verification.

\- Verification must follow the supplied tool's rules, including its retry limit.

\- Ticket creation must be confirmed by the mock tool's returned status.

\- Customer-facing policy answers should be grounded in the current knowledge base.

\- Superseded policy documents must not override current policy.

\- API credentials must remain outside the public repository.



\## 6. Implementation and Artifacts



The project includes baseline and RAG-related modules, a conversation agent, a voice pipeline, and a command-line entry point.



The sample voice run produced the following artifacts:



\- `sample\_outputs/customer\_question\_transcript.txt`

\- `sample\_outputs/customer\_question\_reply.txt`

\- `sample\_outputs/customer\_question\_reply.wav`

\- `sample\_outputs/customer\_question\_sources.json`

\- `sample\_outputs/voice\_pipeline\_results.json`



The sample request concerns the electronics return policy. These files provide evidence of the transcription, response generation, source capture, and audio-output stages.



\## 7. Testing Notes



Python syntax compilation completed successfully for the project entry point and principal pipeline modules. The sample voice pipeline completed successfully in the local environment, and a mock ticket-creation test returned a successful result.



The baseline evaluation output is saved at `outputs/baseline\_results.csv`. No numerical performance score is claimed in this report; metrics should be quoted only after confirming them from the evaluation results.



\## 8. Limitations



This is a prototype that depends on the supplied dataset, configured API credentials, external speech services, and mock business tools. It has not been established as a production-ready customer-support system. Further work should include broader test coverage, robust error handling, latency measurements, and validation of responses against business rules.



\## 9. Conclusion



ZentroMart demonstrates an integrated voice-support workflow combining speech recognition, retrieval-grounded information access, conversational processing, business-tool integration, and speech synthesis. The saved sample artifacts and source code provide evidence for reviewing the implemented workflow.



\## 10. Reproducibility



Refer to the repository `README.md` for setup instructions, dependency installation, environment configuration, and execution steps. Keep secrets in a local `.env` file and never publish them.



