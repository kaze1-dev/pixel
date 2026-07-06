import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_postgres import PGEngine, PGVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

if not os.getenv("DATABASE_URL") or not os.getenv("GROQ_API_KEY"):
    raise ValueError("DATABASE_URL or GROQ_API_KEY not found in environment variables. Please set them in your .env file.")

app = FastAPI(
    title= "Pixel AI",
    description="Production RAG backend."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
engine = PGEngine.from_connection_string(url=os.getenv("DATABASE_URL"))
vector_store = PGVectorStore.create_sync(
    engine=engine,
    table_name="pixel_cat_knowledge",
    embedding_service=embeddings,
)

llm = ChatGroq(
    temperature=0.6,
    model_name="openai/gpt-oss-20b",
    max_tokens=120,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_with_pixel(request: ChatRequest):
    try:
        docs = vector_store.similarity_search(request.message, k=3)
        context_block = "\n\n".join([doc.page_content for doc in docs])
        
        system_prompt = (
    "You are 'Pixel', a sharp, professional AI cat assistant on Faisal Abbas's portfolio site.\n\n"
    "CRITICAL DIRECTIVES:\n"
    "- Length: Respond in 1-3 sentences MAXIMUM, unless the user explicitly asks for a detailed explanation "
    "or walkthrough. Default to the shortest answer that fully addresses the question. Never ask more than "
    "one follow-up question at a time.\n"
    "- Persona: Maintain a brilliant tech-engineered mindset. Speak professionally about Faisal's skills, "
    "but insert ONE organic, sparse cat quirk per response MAX (e.g. *adjusts pixel glasses*). Never stack "
    "multiple action beats in one reply.\n"
    "- Grounding: Use ONLY the context below. If an answer isn't present, use your feline persona to briefly "
    "redirect the user to Faisal's LinkedIn or direct contact — do this in one sentence, not a paragraph.\n\n"
    f"--- START CONTEXT ---\n{context_block}\n--- END CONTEXT ---"
)
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{user_message}")
        ])
        
        rag_chain = prompt_template | llm
        ai_response = rag_chain.invoke({"user_message": request.message})
        return {"response": ai_response.content}
    except Exception as e:
        print(f"Error during chat processing: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "bot": "Pixel AI is running smoothly"}