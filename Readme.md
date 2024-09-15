# 🌟 Langchain OpenAI QnA Agent 🌟  
🚀 **Powered by FastAPI, Langchain, Langsmith, Langgraph, and OpenAI** 🚀

This web application provides a seamless QnA chatbot experience, combining the power of state-of-the-art language models and a robust API backend.

---

## 🚀 Overview

🤖 **Langchain QnA Agent** is a cutting-edge chatbot web application leveraging FastAPI and various language model frameworks to provide efficient and intelligent multi-document QnA support.

---

## 🌟 Features

1. **Multi-Document QnA**: Easily handle and query across multiple documents simultaneously. 📂💬
2. **Multi-Question Support**: Answer multiple questions in a single interaction. 🎥📝
3. **Slack Integration**: Stay connected with seamless Slack integration for real-time QnA interactions. 💬⚡

---

## 📋 Prerequisites

- **Python 3.10**
- **FastAPI**
- **Langchain**
- **OpenAI API Key**
- **LangGraph**
- **Langsmith**

---

## 🔧 Setup Instructions

### 1. Clone the Repository:

```bash
git clone https://github.com/Nakul74/langgraph-bot.git
```

### 2. Create Conda Environment:

```bash
conda create -p ./envs $(cat runtime.txt) -y
```

### 3. Activate Environment:

```bash
conda activate envs/
```

### 4. Install Dependencies:
```bash
pip install -r requirements.txt
```

### 5. Run FastApi app:
```bash
uvicorn main:app --reload
```

---

## 🐳 Docker Setup

### 1. Build the Docker Image:

```bash
docker build -t langchain-qna-bot .
```

### 2. Run the Docker Container:

```bash
docker run -d -p 8080:8080 langchain-qna-bot
```


---
