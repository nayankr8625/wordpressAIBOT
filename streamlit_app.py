import streamlit as st
from data_collection import extract_content_as_json
from embedding import create_faiss_indexes, merge_vector_stores
from gen_ai import query_chain
from template import css, bot_template, user_template
import tempfile


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():

    st.set_page_config(page_title="Query Your Wordpress Site",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    # Sidebar for uploading documents and processing
    st.sidebar.header("Upload Document")
    uploaded_file = st.sidebar.file_uploader("Upload your Document", type=["pdf", "doc"])

    # Check if document is uploaded
    if uploaded_file:
        file_contents = uploaded_file.read()
        if file_contents is not None:
            if st.sidebar.button("Process"):
                with st.spinner("Processing"):
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        temp_file.write(file_contents)
                        temp_file.seek(0)
                        # Get pdf text
                        vectorStores = indexing(pdf=temp_file.name,pdf_name=uploaded_file.name)
                        chain, memory = query_llm(vector_store=vectorStores)
                        # Create conversation chain
                        st.session_state.conversation = chain

    # Ask user for query if document is uploaded
    if "conversation" in st.session_state:
        st.subheader("Ask a question about your documents:")
        user_question = st.text_input("Ask a question about your documents:")
        if user_question:
            handle_userinput(user_question)

    # Clear session state button
    if st.sidebar.button("Clear"):
        st.session_state.clear()

if __name__ == '__main__':
    main()