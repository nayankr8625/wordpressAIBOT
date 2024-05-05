from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.retrievers.merger_retriever import MergerRetriever
from typing import Tuple

GROQ_API_KEY = "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"

def query_chain(vector_store: MergerRetriever)-> Tuple[ConversationalRetrievalChain, ConversationBufferMemory]:
    chat = ChatGroq(temperature=0, model_name="llama3-8b-8192", api_key=GROQ_API_KEY)
    memory = ConversationBufferMemory(
    memory_key='chat_history', return_messages=True, output_key='answer')
    conversation_chain = (ConversationalRetrievalChain.from_llm
                        (llm=chat,
                        retriever=vector_store,
                        # condense_question_prompt=CONDENSE_QUESTION_PROMPT,
                        memory=memory,
                        return_source_documents=True,verbose=False))
    print("Conversational Chain created for the LLM using the vector store")
    return conversation_chain,memory