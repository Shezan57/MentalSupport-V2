# Step1: Setup Streamlit
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("🧠 MenatalSupport – AI Mental Health Therapist")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Step2: User is able to ask question
# Chat input
user_input = st.chat_input("What's on your mind today?")
if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # AI Agent exists here
    try:
        response = requests.post(BACKEND_URL, json={"message": user_input}, timeout=120)
        
        if response.status_code == 200:
            response_data = response.json()
            assistant_message = f'{response_data["response"]}'
            if response_data.get("tool_called") and response_data["tool_called"] != "None":
                assistant_message += f' [Tool: {response_data["tool_called"]}]'
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_message})
        else:
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": f"Sorry, I encountered an error (Status {response.status_code}). Please try again."
            })
    except requests.exceptions.JSONDecodeError:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Sorry, I received an invalid response from the server. Please make sure the backend is running properly."
        })
    except requests.exceptions.ConnectionError:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Sorry, I couldn't connect to the backend server. Please make sure it's running on http://localhost:8000"
        })
    except Exception as e:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"Sorry, an unexpected error occurred: {str(e)}"
        })


# Step3: Show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])