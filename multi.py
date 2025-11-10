from langgraph.graph import StateGraph, END, START
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from tavily import TavilyClient
from dotenv import load_dotenv
from typing import TypedDict, List, Optional
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv(dotenv_path="C:\\Users\\HP\\Desktop\\Playground\\LangGraph\\LLM Bot\\Multi_agent chatbot\\groq_multi.env")

llm = ChatGroq(model="llama-3.3-70b-versatile")
tavily = TavilyClient()

class AgentState(TypedDict):
    query : str
    sources : Optional[List[str]]
    summaries : Optional[List[str]]
    final_report : Optional[str]


def searcher_agent(state : AgentState) -> AgentState :
    query = state["query"]
    results = tavily.search(query, max_results=3)
    articles = [r["content"] for r in results["results"]]
    return{"sources":articles}

def summarizer_agent(State : AgentState) :
    summaries = []
    for src in State["sources"] :
        prompt = ChatPromptTemplate.from_template("Summarize this article clearly:\n{text}")
        summary = llm.invoke(prompt.format_messages(text=src))
        summaries.append(summary.content)
    return{"summaries" : summaries}
    
def analyst_agent(state : AgentState) :
    summaries_text = "\n\n".join(state["summaries"])
    prompt = ChatPromptTemplate.from_template(
        "Combine the following summaries into a structured research report:\n{summaries}")
    report = llm.invoke(prompt.format_messages(summaries = summaries_text))
    return{"final_report":report.content}


graph = StateGraph(AgentState)


graph.add_node("searcher_agent" , searcher_agent)
graph.add_node("summarizer_agent" , summarizer_agent)
graph.add_node("analyst_agent" , analyst_agent)


graph.set_entry_point("searcher_agent")
graph.add_edge("searcher_agent","summarizer_agent")
graph.add_edge("summarizer_agent","analyst_agent")
graph.add_edge("analyst_agent", END)

research_assistant = graph.compile()

conversation_history = []


if __name__ == "__main__":
    query = "Latest research on AI in financial risk modeling"
    conversation_history.append(HumanMessage(content=query))
    result = research_assistant.invoke({"query": query})
    final_report = result["final_report"]
    conversation_history.append(AIMessage(content=final_report))
    print("\n🧠 Final Research Report:\n")
    print(result["final_report"])

    with open("conversation.txt", "a", encoding="utf-8") as file:
        file.write("\n--- New Conversation ---\n\n")
        for message in conversation_history:
            if isinstance(message, HumanMessage):
                file.write(f"User:\n{message.content}\n\n")
            elif isinstance(message, AIMessage):
                file.write(f"Multi-Agent:\n{message.content}\n\n")
        file.write("✅ Conversation saved!\n")