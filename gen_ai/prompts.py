from langchain.prompts import PromptTemplate

# Define a custom prompt template
CUSTOM_PROMPT_TEMPLATE = """
You are a helpful assistant. Use the following context to answer the question.
If you can't find the answer in the context, be honest and say you don't know.
If user ask about the Post related information look carefully for the context and previous chat history before providing any answer, You shouldn't be making mistakes in any such questions.

Context:
{context}

Chat History:
{chat_history}

Question:
{question}

Provide a helpful and accurate response based on the context.
"""

# Custom prompt with required keys for question generation
question_generator_prompt = PromptTemplate(
    input_variables=["chat_history", "question"], 
    template="Condense the following chat history and question into a new question:\n\nChat History:\n{chat_history}\n\nQuestion:\n{question}\n"
)

# Custom prompt for generating the final answer
custom_prompt = PromptTemplate(
    input_variables=["context", "chat_history", "question"],
    template=CUSTOM_PROMPT_TEMPLATE
)