import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from multi import research_assistant  # Import your multi-agent system

# Streamlit configuration
st.set_page_config(page_title="Multi-Agent Research Chatbot", page_icon="🧠", layout="wide")

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Page title and description
st.title("🧠 Multi-Agent Research Chatbot")
st.markdown("Ask a research question and let multiple AI agents gather, summarize, and analyze information for you.")

# Input
query = st.text_input("Enter your research question:")

# Run Research
if st.button("Run Research") and query.strip():
    st.session_state.conversation_history.append(HumanMessage(content=query))
    with st.spinner("Researching... please wait ⏳"):
        result = research_assistant.invoke({"query": query})
        final_report = result["final_report"]
        st.session_state.conversation_history.append(AIMessage(content=final_report))
    
    st.success("✅ Research completed!")
    st.write("### 🧾 Final Research Report")
    st.write(final_report)

    # Save to file
    with open("conversation.txt", "a", encoding="utf-8") as file:
        file.write("\n--- New Conversation ---\n\n")
        for msg in st.session_state.conversation_history[-2:]:
            if isinstance(msg, HumanMessage):
                file.write(f"User:\n{msg.content}\n\n")
            elif isinstance(msg, AIMessage):
                file.write(f"AI:\n{msg.content}\n\n")
        file.write("✅ Conversation saved!\n")

# Show conversation history
st.write("---")
st.write("### 💬 Conversation History")
for msg in st.session_state.conversation_history:
    if isinstance(msg, HumanMessage):
        st.markdown(f"**🧍User:** {msg.content}")
    elif isinstance(msg, AIMessage):
        st.markdown(f"**🤖 AI:** {msg.content}")
