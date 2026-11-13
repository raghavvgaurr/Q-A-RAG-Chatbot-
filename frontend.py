import streamlit as st
import uuid
from backeend import workflowtbot,retrive_allthreads
from langchain_core.messages import HumanMessage, AIMessage
# ==========================================
# 1. UTILITY FUNCTIONS
# ==========================================

def generate_thread_id():
    return str(uuid.uuid4())

def get_config():
    return {
        "configurable": {
            "thread_id": st.session_state["thread_id"]
        }
    }

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_thread"]:
        st.session_state["chat_thread"].append(thread_id)

def reset_message():
    # Generate a new thread ID
    thread_id = generate_thread_id()
    # Update current thread
    st.session_state["thread_id"] = thread_id
    # Add new thread to conversation list
    add_thread(thread_id)
    # Clear current UI messages
    st.session_state["message_history"] = []
    st.rerun()


def load_conversation(thread_id):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    state = workflowtbot.get_state(config)
    return state.values.get("messages", [])


# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


if "chat_thread" not in st.session_state:
    st.session_state["chat_thread"] = retrive_allthreads()


if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()
# Add current thread to thread list
add_thread(st.session_state["thread_id"])

# ==========================================
# 3. SIDEBAR
# ==========================================

st.sidebar.title("LANGGRAPH CHATBOT")
# New Chat Button
if st.sidebar.button("➕ New Chat", use_container_width=True):
    reset_message()
st.sidebar.header("Conversations")
# Display all conversation threads
for thread_id in st.session_state["chat_thread"][::-1]:
    if st.sidebar.button(
        str(thread_id),
        key=f"thread_{thread_id}",
        use_container_width=True
    ):
        # Switch current thread
        st.session_state["thread_id"] = thread_id
        # Load messages from LangGraph checkpointer
        messages = load_conversation(thread_id)
        temp_message = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = "user"
            elif isinstance(msg, AIMessage):
                role = "assistant"
            else:
                continue
            temp_message.append({
                "role": role,
                "content": msg.content
            })
        # Update UI history
        st.session_state["message_history"] = temp_message
        st.rerun()


# ==========================================
# 4. MAIN UI
# ==========================================

st.title("LangGraph Chatbot")
st.caption(
    f"Current Thread: {st.session_state['thread_id']}"
)
# Display conversation history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])
# ==========================================
# 5. USER INPUT
# ==========================================
user_input = st.chat_input("Type your message here...")
if user_input:
    # Add user message to UI history
    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.write(user_input)
    # ======================================
    # 6. AI RESPONSE
    # ======================================

    with st.chat_message("assistant"):
        # Always get the latest thread configuration
        config = get_config()
        ai_answer = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in workflowtbot.stream(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },
                config=config,
                stream_mode="messages"
            )
            if isinstance(message_chunk.content, str)
            and message_chunk.content
        )
    # Save assistant response to UI history
    st.session_state["message_history"].append({
        "role": "assistant",
        "content": ai_answer
    })
