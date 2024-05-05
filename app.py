import streamlit as st
from data_collection import extract_content_as_json
from embedding import create_faiss_indexes, merge_vector_stores
from gen_ai import query_chain
from template import css, bot_template, user_template


def handle_userinput(user_question):
    # Query the conversation chain with the user's question
    response = st.session_state.conversation({"question": user_question})
    # Update the chat history in the session state
    st.session_state.chat_history = response["chat_history"]

    # Display the chat history in the UI
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    # Set the Streamlit page configuration
    st.set_page_config(page_title="Query Your WordPress Site", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    # Sidebar for entering WordPress domain
    st.sidebar.header("WordPress Content Extraction")
    wordpress_domain = st.sidebar.text_input("Enter WordPress domain (e.g., example.com)")

    # Proceed only if a valid domain is entered
    if wordpress_domain:
        if st.sidebar.button("Extract Content"):
            with st.spinner("Extracting content from WordPress..."):
                # Extract content from the specified WordPress domain
                wordpress_json = extract_content_as_json(wordpress_domain)
                
                # Create FAISS indexes from the extracted content
                create_faiss_indexes(wordpress_json)
                # merege faiss indexes
                vector_store = merge_vector_stores()
                
                # Create the conversation chain for querying the extracted content
                chain, memory = query_chain(vector_store=vector_store)
                st.session_state.conversation = chain

    # If a conversation has been created, allow the user to ask questions
    if "conversation" in st.session_state:
        st.subheader("Ask a question about your WordPress content:")
        user_question = st.text_input("Ask a question about the WordPress content:")
        
        # Handle the user input
        if user_question:
            handle_userinput(user_question)

    # Clear session state if needed
    if st.sidebar.button("Clear"):
        st.session_state.clear()


if __name__ == "__main__":
    main()
