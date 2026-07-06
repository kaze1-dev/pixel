---
title: Pixel
emoji: 🐈
colorFrom: purple
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# Pixel: AI Portfolio Companion

Pixel is an interactive, pixel-art AI chatbot built for my personal portfolio. Modeled as a violet pixel cat, Pixel serves as an automated assistant to help potential clients and recruiters learn about my skills, background, and projects through natural conversation.

As a Retrieval-Augmented Generation (RAG) pipeline, Pixel pulls accurate, real-time facts directly from my verified portfolio data and resume.

## Key Features

- Context-Aware RAG: Powered by LangChain to fetch relevant professional context before answering queries.
- Ultra-Fast Responses: Utilizes the Groq API for sub-second LLM inference.
- Chat Memory: Uses langchain_postgres to maintain conversation history for seamless multi-turn interactions.
- Modern Stack: Structured with FastAPI, packaged with uv, and containerized via Docker for Hugging Face Spaces.

## Tech Stack

- Backend: FastAPI
- Orchestration: LangChain
- LLM Gateway: Groq Cloud API
- Embeddings: LangChain HuggingFace
- Vector Store & History: PostgreSQL (via Neon and langchain_postgres)
- Package Manager: uv
- Deployment: Docker and Hugging Face Spaces

## Repository Structure

.
├── README.md               
├── Dockerfile              
├── main.py                
├── ingest.py              
├── pyproject.toml          
└── uv.lock                 

## Local Setup

Make sure you have uv installed on your machine before starting.

1. Clone the repository and install dependencies:
git clone <your-repo-url>
cd pixel
uv sync

2. Create a .env file in the root directory:
GROQ_API_KEY="your_groq_api_key"
DATABASE_URL="postgresql://user:password@your-neon-host/dbname?sslmode=require"

3. Run the ingestion script to seed your database:
uv run ingest.py

4. Start the local development server:
uv run uvicorn main:app --reload --port 7860

## Continuous Deployment

This repository automatically syncs to Hugging Face Spaces on every push to the main branch via GitHub Actions. Ensure your HF_TOKEN is added to your GitHub repository secrets to allow the automation to run smoothly.