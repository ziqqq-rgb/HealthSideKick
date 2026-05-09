# HealthSideKick

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Overview

**HealthSideKick** is an AI-powered, full-stack application designed to help users and healthcare professionals instantly query and extract vital information from medical documents. By leveraging Retrieval-Augmented Generation (RAG), the system allows users to securely upload medical PDFs, parse the content, and ask natural language questions to get precise, context-aware answers directly from their own documents.

### Problem Statement
Medical guidelines, patient records, and research papers are often dense, lengthy, and difficult to navigate quickly. When healthcare practitioners or patients need to find a specific dosage, contraindication, or procedural step, manually searching through pages of PDF documents is time-consuming and prone to human error. HealthSideKick solves this by turning static medical documents into interactive, queryable knowledge bases.

## Features

* **Secure User Authentication:** Full user signup and login flow protected by JWT access tokens and bcrypt password hashing.
* **Intelligent Document Processing:** Upload medical PDFs which are then parsed and ingested into a Pinecone vector database.
* **Conversational AI Interface:** A clean, intuitive Streamlit chat interface to ask questions about your documents.
* **Advanced RAG Engine:** Powered by LangChain, Google GenAI, and Groq to deliver highly accurate, document-grounded answers.
* **Robust Backend API:** Built on FastAPI with SQLAlchemy and PostgreSQL for scalable database management and secure file handling.

## Tech Stack

* **Frontend:** Streamlit, Requests
* **Backend:** FastAPI, Uvicorn, Python-Multipart
* **Database & Auth:** PostgreSQL, SQLAlchemy, PyJWT, Bcrypt
* **AI & RAG:** LangChain, Llama-Parse, Pinecone, Google GenAI, Groq

## Installation

### Prerequisites
* Python 3.10+
* PostgreSQL running locally or via a cloud provider
* Pinecone API Key
* LLM API Keys (Google GenAI / Groq)

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/healthsidekick.git](https://github.com/yourusername/healthsidekick.git)
cd healthsidekick
```
### 2. Setup the Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
### 3. Setup the Frontend
```bash
cd frontend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
## Configuration
Create a .env file in the backend directory and add the following environmental variables:
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/healthsidekick

# JWT Security
SECRET_KEY=your_super_secret_jwt_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Vector Database & AI
PINECONE_API_KEY=your_pinecone_api_key
GOOGLE_API_KEY=your_google_genai_api_key
GROQ_API_KEY=your_groq_api_key
```
## Usage
### Start the FastAPI Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```
The backend API will be available at http://localhost:8000. You can view the interactive Swagger documentation at http://localhost:8000/docs.

### Start the Streamlit Frontend
In a separate terminal:
```bash
cd frontend
source venv/bin/activate
streamlit run app.py
```
The frontend UI will automatically open in your browser at http://localhost:8501. Create an account, upload a medical PDF, and start asking questions!

## Contributing
Contributions are welcome! If you'd like to improve HealthSideKick:

1. Fork the repository.

2. Create a feature branch (git checkout -b feature/AmazingFeature).

3. Commit your changes (git commit -m 'Add some AmazingFeature').

4. Push to the branch (git push origin feature/AmazingFeature).

5. Open a Pull Request.

Please ensure your code follows the existing style and includes appropriate documentation.
