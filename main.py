import streamlit as st

from services import get_query_response

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# if not st.session_state.get("messages"):
#     st.session_state["messages"] = []
    
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Please enter your query...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    
    with st.chat_message("assistant"):
        with st.spinner('Fetching...'):
            response = get_query_response(user_input)
            content = st.write_stream(response)
            # status.update(label="Done!", state="complete")
    print(content)
    st.session_state.messages.append({
        "role": "assistant",
        "content": content
    })