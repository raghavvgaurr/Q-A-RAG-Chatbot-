import streamlit as st
def initialize_memory():
    """Initialize conversation history."""

    if "messages" not in st.session_state:
        st.session_state.messages = []


def get_history():
    """Return conversation history as readable text."""

    messages = st.session_state.get("messages", [])

    return "\n".join(
        f"{'User' if msg['role'] == 'user' else 'Assistant'}: "
        f"{msg['content']}"
        for msg in messages[-12:]
    )


def add_message(role, content, sources=None):
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "sources": sources or [],
    })



def clear_memory():
    """Clear the current conversation."""
    st.session_state.messages = []
