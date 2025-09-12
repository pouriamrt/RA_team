import streamlit as st
from agents.create_team import initialize_team
import time
from dotenv import load_dotenv
import os
from agno.models.openai import OpenAIChat

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
model = OpenAIChat(id=MODEL_NAME, api_key=OPENAI_API_KEY)
model_name = model.id

if "team" not in st.session_state:
    if "team_session_id" not in st.session_state:
        st.session_state.team_session_id = f"streamlit-team-session-{int(time.time())}"
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    st.session_state.team = initialize_team(model)

st.title("Research Assistant Team")
st.markdown("""
This AI team can help with:
- Web searches  
- Website content extraction  
- YouTube video analysis  
- Email drafting & sending  
- GitHub repo exploration  
- Hacker News trend tracking  
- General Q&A and synthesis  
""")

# Display past messages (if any) from the session state
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box for the user's query
user_query = st.chat_input("Ask the research team anything...")

if user_query:
    # Log user message in history
    st.session_state.messages.append({"role": "user", "content": user_query})
    # Display user message immediately in chat
    with st.chat_message("user"):
        st.markdown(user_query)
    # Prepare to display team's answer
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # placeholder for streaming text
        full_response = ""
        # Run the team on the user query with streaming enabled
        try:
            # Check if tool logs should be captured
            capture_tool_logs = st.session_state.get("show_tool_logs", False)
            tool_logs = []
            
            response_stream = st.session_state.team.run(user_query, stream=True)
            for chunk in response_stream:
                if chunk.content and isinstance(chunk.content, str):
                    # Filter out tool execution messages from the main response
                    if "delegate_task_to_member" in chunk.content:
                        break
                    
                    if not (chunk.content.startswith(("duckduckgo_", "web_crawler", "youtube_", "resend_", "github_", "hackernews_")) or 
                            ") completed in " in chunk.content):
                        full_response += chunk.content
                        # Display the current accumulated response with a cursor
                        message_placeholder.markdown(full_response + "▌")
                    elif capture_tool_logs:
                        # Capture tool logs for debugging
                        tool_logs.append(chunk.content)
            
            # Store tool logs if captured
            if capture_tool_logs and tool_logs:
                st.session_state.tool_logs = "\n".join(tool_logs)
            
            # When done, display the final response (remove the blinking cursor)
            message_placeholder.markdown(full_response)
            # Add the final response to the messages history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            memories = []
            for memory in st.session_state.team.db.get_user_memories():
                memories.append(memory.memory)
            st.session_state.memory_dump = memories
            
        except Exception as e:
            # Error handling: show an error in the app and log to history
            st.error(f"An error occurred: {e}\nPlease check your API keys and try again.")
            st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})
            st.exception(e)  # for debug, print full traceback in the app
            
            
            
with st.sidebar:
    st.title("Team Settings")

    # Toggle to display team memory for debugging
    if st.checkbox("Show Team Memory Contents", value=False):
        st.subheader("Team Memory (Debug)")
        if "memory_dump" in st.session_state:
            # Pretty-print the memory message list
            from pprint import pformat
            memory_str = pformat(st.session_state.memory_dump, indent=2, width=80)
            st.code(memory_str, language="python")
        else:
            st.info("Interact with the team to see memory contents here.")
    
    # Toggle to show tool execution logs for debugging
    show_tool_logs = st.checkbox("Show Tool Execution Logs", value=False)
    st.session_state.show_tool_logs = show_tool_logs
    
    if show_tool_logs:
        st.subheader("Tool Execution Logs (Debug)")
        if "tool_logs" in st.session_state:
            st.code(st.session_state.tool_logs, language="text")
        else:
            st.info("Tool execution logs will appear here when enabled.")
    # Display current session info
    st.markdown(f"**Session ID**: `{st.session_state.team_session_id}`")
    st.markdown(f"**Model**: {model_name}")
    st.subheader("Memory & Session")
    st.markdown("This team remembers the conversation in this session. Use the reset button to clear memory.")
    # Button to clear chat history and reinitialize the team
    if st.button("Clear Chat & Reset Team"):
        st.session_state.messages = []
        st.session_state.team_session_id = f"streamlit-team-session-{int(time.time())}"
        st.session_state.team = initialize_team(model)  # start a fresh team instance
        if "memory_dump" in st.session_state:
            del st.session_state.memory_dump
        if "tool_logs" in st.session_state:
            del st.session_state.tool_logs
        st.rerun()  # reload the app
    st.title("About")
    st.markdown("""
    **How this works**:  
    - The *coordinator* agent analyzes your query and delegates tasks to the specialist agents.  
    - Each specialist does its part (searching, crawling, analyzing, etc.) and returns results to the coordinator.  
    - The coordinator then synthesizes everything into a final answer which you see here.  
    - The team has memory within a session, so you can ask follow-up questions that reference earlier answers.  
    **Example queries**:  
    - "What are the latest AI breakthroughs?" (uses Web Search)  
    - "Crawl http://example.com and summarize the homepage." (uses Web Crawler)  
    - "Summarize the YouTube video at https://youtu.be/dQw4w9WgXcQ" (uses YouTube Analyst)  
    - "Draft an email to [email protected] about our project." (uses Email Assistant)  
    - "Find trending Python repositories on GitHub this week." (uses GitHub Researcher)  
    - "What's trending on Hacker News today?" (uses HackerNews Monitor)  
    - "What was my first question to you?" (tests the team's memory)  
    """)