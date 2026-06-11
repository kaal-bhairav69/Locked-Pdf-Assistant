from pypdf import PdfReader
import requests
from sentence_transformers import SentenceTransformer
import numpy as np
import time
from phi.agent import Agent
from phi.model.groq import Groq

#Model (Load Once)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
chat_agent = Agent( model=Groq(id="llama-3.3-70b-versatile"), show_tool_calls=True, markdown=True )

#summarise the pdf
def summarise_pdf(chat_agent, text):
    prompt = f"""
    Summarize this PDF.

    Cover all major topics and subtopics briefly.
    Include important formulas if present.
    Keep the summary structured.

    PDF Text:
    {text}
    """

    response = chat_agent.run(prompt)
    return response.content.strip()

#Pre-Processing
def process_pdf(pdf_path,password):
    reader=PdfReader(pdf_path)
    if reader.is_encrypted:
        result=reader.decrypt(password)
        if(result==0):
            raise Exception("wrong pdf password")
    text= ""   
    for page in reader.pages:
        text += page.extract_text()

    chunk_size = 1500
    overlap = 300
    chunks=[]
    start=0
    while start < len(text):
        end = start+chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)

    chunk_embedding = embed_model.encode(chunks,normalize_embeddings=True)
    pdf_summary = summarise_pdf(chat_agent, text)
    return text,chunks,chunk_embedding,pdf_summary

#retrieve 
def retrieve_chunks(question, chunks, chunk_embeddings, k=3):
    question_embedding = embed_model.encode([question],normalize_embeddings=True)[0]
    scores = np.dot(chunk_embeddings, question_embedding)
    max_score = np.max(scores)

    if max_score < 0.3:
        return None

    top_indices = np.argsort(scores)[-k:]
    return [chunks[i] for i in reversed(top_indices)]


# Chat with PDF Function
def chat_with_pdf(question, chunks, chunk_embeddings, pdf_summary, history):

    history_text = "\n".join(history)
    if any(x in question.lower() for x in ["summarize","summarise","summary","overview of pdf","what is in this pdf"]):
        
        return pdf_summary, history

    relevant_chunks = retrieve_chunks(question,chunks,chunk_embeddings,k=3)

    if relevant_chunks is None:
        context = pdf_summary
    else:
        context = "\n\n".join(relevant_chunks)

    prompt = f"""
    You are a PDF assistant who can explain the concepts in the pdf just like normal chatbots.
    Answer ONLY using the PDF context
    If the context is a summary, answer using the summary.
    If the context is detailed chunks, answer from those chunks.

    PDF Context:
    {context}

    Conversation History:
    {history_text}

    Question:
    {question}

    Answer:
    """
    response = chat_agent.run(prompt)
    answer = response.content.strip()
    history.append(f"User: {question}")
    history.append(f"Assistant: {answer}")
    history = history[-6:]
    
    return answer, history







