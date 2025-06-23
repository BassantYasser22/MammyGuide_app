 MammyGuide - Machine Learning Component

This repository contains the Machine Learning part of our graduation project: MummyGuide App , a smart parenting assistant for mothers.

Overview
MammyGuide aims to support mothers by helping them interact with their children in a positive, psychologically safe way.

The ML module plays a key role in:
- Understanding user input through natural language (NLP)
- Retrieving the most relevant parenting videos using semantic search
- Powering the AI chatbot that provides expert-based responses

📌 Key Technologies
- Python  
- HuggingFace Transformers  
- Sentence Transformers (`multilingual-e5-base`)  
- Sklearn for similarity  
- JSON & REST API integration

📁 Main Features
- Semantic Search: Converts user queries into vector embeddings and finds the most suitable video.
- It is connected to an external AI service through an API, allowing it to understand natural language and provide helpful, reliable responses based on trusted educational content.
- Multilingual Support:The model supports English and Arabic queries.

 📂 Structure
- `model/` – Pretrained transformer model used for embedding
- `scripts/` – Core logic for search, matching, and chatbot logic
- `data/` – JSON files containing curated parenting questions and expert advice
- `app.py` – Backend logic that connects ML functions with the frontend
