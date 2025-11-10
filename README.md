# 🧠 Multi-Agent Research Assistant

A research chatbot built using **LangGraph**, **ChatGroq (Llama-3-70B)**, and **Tavily API**.  
Multiple AI agents collaborate to gather, summarize, and analyze research information automatically.

## 🚀 Features
- Multi-agent pipeline (Search → Summarize → Analyze)
- Uses ChatGroq for fast inference
- Real-time web results via Tavily API
- Conversation memory — automatically saves each interaction
- Simple Streamlit interface for interaction

## 🛠️ Tech Stack
- LangGraph
- ChatGroq (Llama-3-70B)
- Tavily API
- Streamlit

## 🧩 Agents
| Agent | Role |
|--------|------|
| 🔍 SearcherAgent | Retrieves top web articles using the Tavily API |
| 📝 SummarizerAgent | Summarizes articles into key points |
| 📊 AnalystAgent | Combines all summaries into a structured final research report |
export GROQ_API_KEY="your_groq_api_key"
streamlit run app.py
