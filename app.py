
import streamlit as st
from datetime import datetime

from database import (
    init_db,
    create_conversation,
    get_conversations,
    get_messages,
    update_conversation_title,
    delete_conversation,
)
from chatbot import get_ai_response


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Orbia AI | Personal Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>
    .stApp {
        background-color: #f7f8fc;
    }

    [data-testid="stSidebar"] {
        background-color: #eef1f8;
        border-right: 1px solid #e0e5ef;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    .brand {
        font-size: 1.65rem;
        font-weight: 750;
        color: #4f46e5;
        letter-spacing: -0.7px;
        margin-bottom: 0;
    }

    .subtitle {
        color: #778099;
        font-size: 0.9rem;
        margin-top: 4px;
        margin-bottom: 1.3rem;
    }

    .hero {
        padding: 1.3rem 1.5rem;
        background: linear-gradient(120deg, #eef2ff, #f5f3ff);
        border: 1px solid #e0e7ff;
        border-radius: 18px;
        margin-bottom: 1.4rem;
    }

    .hero-title {
        color: #27275f;
        font-size: 1.65rem;
        font-weight: 750;
        margin: 0;
    }

    .hero-subtitle {
        color: #626b85;
        font-size: 0.94rem;
        margin-top: 6px;
    }

    .section-label {
        color: #737d95;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 1rem;
        margin-bottom: 0.6rem;
    }

    [data-testid="stChatMessage"] {
        background: #ffffff;
        border: 1px solid #e9ecf4;
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 8px rgba(35, 45, 85, 0.035);
    }

    [data-testid="stChatInput"] {
        border-color: #d9deed;
    }

    div.stButton > button {
        border-radius: 10px;
        transition: all 0.15s ease;
    }

    div.stButton > button:hover {
        border-color: #818cf8;
        color: #4338ca;
    }

    .timestamp {
        color: #8a93a8;
        font-size: 0.72rem;
        margin-top: 0.45rem;
    }

    .footer-note {
        color: #8991a4;
        font-size: 0.78rem;
        text-align: center;
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def format_timestamp(value):
    """Format an ISO timestamp using the computer's local timezone."""
    if not value:
        return ""

    try:
        timestamp = datetime.fromisoformat(value)

        if timestamp.tzinfo is not None:
            timestamp = timestamp.astimezone()

        return timestamp.strftime("%d %b %Y, %I:%M %p")

    except (ValueError, TypeError):
        return str(value)


def start_new_conversation():
    """Create a conversation and select it."""
    new_id = create_conversation()

    st.session_state.active_conversation_id = new_id
    st.session_state.pending_delete_id = None


# =====================================================
# SESSION STATE
# =====================================================

if "active_conversation_id" not in st.session_state:
    st.session_state.active_conversation_id = None

if "pending_delete_id" not in st.session_state:
    st.session_state.pending_delete_id = None


# Restore the most recent conversation if needed.
existing_conversations = get_conversations()

if (
    st.session_state.active_conversation_id is None
    or not any(
        c["id"] == st.session_state.active_conversation_id
        for c in existing_conversations
    )
):
    if existing_conversations:
        st.session_state.active_conversation_id = (
            existing_conversations[0]["id"]
        )
    else:
        start_new_conversation()


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">✦ Orbia AI</div>'
        '<div class="subtitle">Your personal AI workspace</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "＋  Start a new chat",
        key="new_chat",
        use_container_width=True,
        type="primary",
    ):
        start_new_conversation()
        st.rerun()

    st.markdown(
        '<div class="section-label">Your conversations</div>',
        unsafe_allow_html=True,
    )

    conversations = get_conversations()

    if not conversations:
        st.caption("No conversations yet.")

    for conversation in conversations:

        chat_id = conversation["id"]
        title = conversation["title"] or "New Chat"

        is_active = (
            chat_id == st.session_state.active_conversation_id
        )

        display_title = " ".join(title.split())

        if len(display_title) > 27:
            display_title = display_title[:24] + "..."

        chat_col, delete_col = st.columns([5, 1])

        # Conversation selector
        with chat_col:

            prefix = "● " if is_active else "○ "

            if st.button(
                prefix + display_title,
                key=f"chat_{chat_id}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
                help=title,
            ):
                st.session_state.active_conversation_id = chat_id
                st.session_state.pending_delete_id = None
                st.rerun()

        # Delete button
        with delete_col:

            if st.button(
                "🗑",
                key=f"delete_{chat_id}",
                help="Delete this conversation",
                use_container_width=True,
            ):
                st.session_state.pending_delete_id = chat_id
                st.rerun()

        st.caption(
            f"{conversation['message_count']} messages"
        )

    # Deletion confirmation
    pending_id = st.session_state.pending_delete_id

    if pending_id is not None:

        pending_chat = next(
            (
                c for c in conversations
                if c["id"] == pending_id
            ),
            None,
        )

        if pending_chat is not None:

            st.warning(
                f"Delete '{pending_chat['title']}'? "
                "Its saved messages will also be deleted."
            )

            confirm_col, cancel_col = st.columns(2)

            with confirm_col:

                if st.button(
                    "Delete",
                    key="confirm_delete",
                    type="primary",
                    use_container_width=True,
                ):
                    # Delete the selected conversation
                    delete_conversation(pending_id)

                    # Refresh the remaining conversations
                    remaining = get_conversations()

                    # Select another chat or create a fresh one
                    if (
                        st.session_state.active_conversation_id
                        == pending_id
                    ):
                        if remaining:
                            st.session_state.active_conversation_id = (
                                remaining[0]["id"]
                            )
                        else:
                            start_new_conversation()

                    st.session_state.pending_delete_id = None
                    st.rerun()

            with cancel_col:

                if st.button(
                    "Cancel",
                    key="cancel_delete",
                    use_container_width=True,
                ):
                    st.session_state.pending_delete_id = None
                    st.rerun()

        else:
            st.session_state.pending_delete_id = None

    st.divider()

    st.caption("🟢 Local model · Ollama")
    st.caption("🔒 Conversations stored in SQLite")


# =====================================================
# MAIN HEADER
# =====================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">Your AI Assistant</div>
    <div class="hero-subtitle">
        Ask questions, explore ideas, and continue your conversations.
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# LOAD ACTIVE CONVERSATION
# =====================================================

active_id = st.session_state.active_conversation_id

conversations = get_conversations()

active_conversation = next(
    (c for c in conversations if c["id"] == active_id),
    None,
)

if active_conversation:
    st.caption(f"Chat: {active_conversation['title']}")

st.divider()

messages = get_messages(active_id)


# =====================================================
# DISPLAY EMPTY STATE
# =====================================================

if not messages:

    st.markdown("### 👋 What can I help you with?")

    st.write(
        "Ask a question below to start a conversation. "
        "Your messages will be saved automatically."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("💡 **Learn**\n\nExplain a new concept.")

    with col2:
        st.info("🧑‍💻 **Code**\n\nGet help with Python.")

    with col3:
        st.info("✍️ **Create**\n\nDraft or improve your writing.")


# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================

for message in messages:

    role = message["role"]

    avatar = "🧑" if role == "user" else "🤖"

    with st.chat_message(role, avatar=avatar):

        st.markdown(message["content"])

        timestamp = format_timestamp(
            message.get("created_at")
        )

        if timestamp:
            st.markdown(
                f'<div class="timestamp">{timestamp}</div>',
                unsafe_allow_html=True,
            )


# =====================================================
# CHAT INPUT AND AI RESPONSE
# =====================================================

user_input = st.chat_input("Message Orbia AI...")

if user_input and user_input.strip():

    user_input = user_input.strip()

    # Set the conversation title from the first user message
    has_user_message = any(
        message["role"] == "user"
        for message in messages
    )

    if not has_user_message:

        title = " ".join(user_input.split())[:60]

        update_conversation_title(
            active_id,
            title,
        )

    # Display the new user message
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    # Generate the AI response
    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("Orbia AI is thinking..."):

            try:
                answer = get_ai_response(
                    active_id,
                    user_input,
                )

                st.markdown(answer)

            except Exception as error:

                st.error(
                    "I couldn't generate a response. "
                    "Check that Ollama is running and the model "
                    "is available, then try again."
                )

                # Show technical details in an expandable section
                with st.expander("Technical details"):
                    st.code(str(error))

    # Refresh history and timestamps from SQLite
    st.rerun()


# =====================================================
# FOOTER
# =====================================================

st.markdown(
    '<div class="footer-note">'
    'Orbia AI · Powered by Llama 3.2 · Running locally'
    '</div>',
    unsafe_allow_html=True,
)
