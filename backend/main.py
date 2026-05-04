from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse
from embedding_service import embedding_service
from vector_store import vector_store
from reranker_service import reranker_service
#from ollama_service import ollama_service
from groq_services import generate
from database import save_chat_history
import config
import uuid
from typing import List

app = FastAPI(title="BP2TL Jakarta Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("Loading FAISS index...")
    loaded = vector_store.load("./faiss_index/bp2tl")
    if loaded:
        print(f"FAISS index loaded successfully with {vector_store.index.ntotal} documents")
    else:
        print("No existing FAISS index found. Please run load_data.py first.")

@app.get("/")
def read_root():
    return {
        "message": "BP2TL Jakarta Chatbot API",
        "status": "running",
        "endpoints": {
            "chat": "/chat",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "faiss_documents": vector_store.index.ntotal,
        "ollama_url": config.OLLAMA_BASE_URL
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        user_message = request.message.strip()
        session_id = request.session_id or str(uuid.uuid4())

        if not user_message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        print(f"\n{'='*60}")
        print(f"Query: {user_message}")
        print(f"{'='*60}")

        query_embedding = embedding_service.encode_query(user_message)
        print("Query embedding generated")

        retrieved_docs = vector_store.search(query_embedding, top_k=config.TOP_K_RETRIEVAL)
        print(f"Retrieved {len(retrieved_docs)} documents from FAISS")

        if not retrieved_docs:
            fallback_response = f"Mohon maaf kak 😊, untuk informasi tersebut belum tersedia. Silakan cek: https://linktr.ee/bpptljkt"
            save_chat_history(session_id, user_message, fallback_response)
            return ChatResponse(response=fallback_response, session_id=session_id)

        documents_for_reranking = [doc[0] for doc in retrieved_docs]

        print(f"Reranking top {config.TOP_K_RETRIEVAL} documents...")
        reranked_indices = reranker_service.rerank(user_message, documents_for_reranking)

        top_reranked = reranked_indices[:config.TOP_K_RERANK]
        print(f"Selected top {len(top_reranked)} documents after reranking")

        contexts = []
        for idx, score in top_reranked:
            doc_text = retrieved_docs[idx][0]
            contexts.append(doc_text)
            print(f"  - Rank {len(contexts)}: Score {score:.4f}")

        print(f"Generating response with ({config.LLM_MODEL})...")
        #bot_response = ollama_service.generate(user_message, contexts)
        print("\n========== FINAL CONTEXT ==========")
        for i, ctx in enumerate(contexts):
            print(f"\n--- CONTEXT {i+1} ---")
            print(ctx[:1000])
        bot_response = generate(user_message, contexts)
        print(f"Response generated: {bot_response[:100]}...")

        save_chat_history(session_id, user_message, bot_response)

        return ChatResponse(response=bot_response, session_id=session_id)

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        error_response = f"Mohon maaf kak 😊, terjadi kesalahan sistem. Silakan coba lagi atau cek: https://linktr.ee/bpptljkt"
        return ChatResponse(response=error_response, session_id=session_id or str(uuid.uuid4()))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
