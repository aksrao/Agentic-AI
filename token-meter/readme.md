# Token Meter 🚦

**Monitor and Track LLM Token Usage Across Providers**

Token Meter is a lightweight API service built with **FastAPI** that tracks token consumption across multiple Large Language Model providers such as **Google Gemini** and **Hugging Face**.
It records token usage, model information, timestamps, and business units (SBU) into a structured JSON log and enables easy visualization through dashboards.

This project helps teams **monitor usage, analyze token consumption, and control LLM costs**.

---

# 🚀 Features

* 🔍 Track **input, output, and total tokens**
* 🤖 Support multiple providers

  * Google Gemini
  * Hugging Face models
* 📊 Store token metrics in a **JSON log**
* 📈 Easily build dashboards from logs
* ⚡ FastAPI-based REST API
* 🔐 Environment-based API key management
* 🧠 Supports both **simple prompts and chat messages**

---

# 🏗️ Architecture

<p align="center">
  <img src="images/architecture.png" width="700">
</p>

Flow:

Client Request → FastAPI → LLM Provider → Token Extraction → JSON Log → Dashboard

---

# 📂 Project Structure

```
token-meter/
│
├── main.py
├── token_usage.json
├── dashboard.py
├── requirements.txt
├── .env
│
├── images/
│   ├── architecture.png
│   └── dashboard.png
```

---

# ⚙️ Installation

### 1. Clone the repository

```
git clone https://github.com/your-username/token-meter.git
cd token-meter
```

### 2. Create a virtual environment

```
python -m venv .tokMeter
source .tokMeter/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```
GEMINI_API_KEY=your_google_api_key
hugging_face_api=your_huggingface_api_token
```

---

# ▶️ Running the API

Start the FastAPI server:

```
uvicorn main:app --reload
```

or using FastAPI CLI:

```
python -m fastapi dev main.py
```

Open the API documentation:

```
http://127.0.0.1:8000/docs
```

---

# 🧪 API Endpoints

## Gemini Endpoint

```
POST /gemini
```

Example request:

```
{
  "model": "gemini-1.5-flash",
  "SBU": "finance",
  "payload": "Explain Kubernetes",
  "temperature": 0.7
}
```

---

## Hugging Face Endpoint

```
POST /hugging-face
```

Example request:

```
{
  "repo_id": "google/gemma-2-2b-it",
  "task": "text-generation",
  "SBU": "analytics",
  "payload": "Explain Kubernetes",
  "temperature": 0.7
}
```

---

# 🧾 Token Logging

Every request generates a record in `token_usage.json`.

Example:

```
{
  "id": 1,
  "sbu": "finance",
  "model": "gemini-1.5-flash",
  "date": "2026-03-18",
  "time": "10:15:20",
  "Input Tokens Used": 20,
  "Output Tokens Used": 50,
  "Total Tokens Used": 70
}
```

---

# 📊 Dashboard Example

Token usage logs can be visualized using **Plotly or Streamlit**.

<p align="center">
  <img src="images/bar-chart.png" width="700">
</p>

Example metrics:

* Tokens per model
* Tokens per SBU
* Daily token usage
* Provider usage distribution

# 🧠 Supported Payload Formats

### Simple Prompt

```
{
  "payload": "Explain Kubernetes"
}
```

### Chat Format

```
{
  "payload": [
    ["system", "You are a sentiment analysis agent"],
    ["human", "I like ice cream"]
  ]
}
```

---

# 🔮 Future Improvements

* LLM cost estimation
* Prometheus metrics integration
* Grafana dashboards
* Multi-provider routing
* Redis caching
* Streaming responses
* Token cost alerts

---

# 🛠️ Tech Stack

* FastAPI
* LangChain
* Google Gemini
* Hugging Face
* Transformers
* Plotly
* Python

---

# 📜 License

MIT License

---

# 🙌 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

# ⭐ Acknowledgements

Inspired by the need to **track LLM usage and manage AI infrastructure costs** in production systems.

---

**Token Meter**
