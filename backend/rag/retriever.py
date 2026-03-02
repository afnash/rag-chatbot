from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from backend.config import settings

def get_retriever():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=settings.GEMINI_API_KEY)
    vector_db = FAISS.load_local(settings.VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    return vector_db.as_retriever(search_kwargs={"k": 3})

def retrieve_context(query: str, chat_history: str = ""):
    """
    Retrieves context and generates a grounded response using Gemini.
    """
    retriever = get_retriever()
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", google_api_key=settings.GEMINI_API_KEY)
    
    # 1. Retrieve Documents
    docs = retriever.invoke(query)
    context_text = "\n\n".join([doc.page_content for doc in docs])
    
    # 2. Prepare Prompt
    prompt_template = """
    You are a professional University Admission Assistant.
    Your goal is to provide accurate information based ONLY on the context provided below.
    
    Rules:
    1. Provide a helpful and relevant response based on the context. If the user's query can be reasonably addressed using the program names or details in the context, do so.
    2. Use the context to suggest programs that match the user's interests or background (e.g., if a student is interested in AI, suggest the Artificial Intelligence program from our list).
    3. If the question is entirely unrelated to admissions, university programs, or the provided context, state that you don't have that information.
    4. Do NOT use external knowledge about other universities or non-existent programs. Do not name the university unless it appears in the context. Use "Our university" instead.
    5. Maintain a friendly and professional tone.
    6. Consider the provided chat history for continuity.
    7. Do NOT include labels like "Answer:" or "Assistant:" in your response. Do NOT use bold markdown (**) for the primary answer label.

    Chat History:
    {history}

    Context:
    {context}

    Current Question: {question}

    Answer:
    """
    
    formatted_prompt = prompt_template.format(
        history=chat_history if chat_history else "No previous history.",
        context=context_text if context_text else "No specific documents found.",
        question=query
    )
    
    # 3. Generate Response
    response = llm.invoke([HumanMessage(content=formatted_prompt)])
    final_response = response.content.replace("**Answer:**", "").replace("**", "").strip()
    
    return final_response, [doc.page_content for doc in docs]
