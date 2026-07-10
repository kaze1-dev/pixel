import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_postgres import PGEngine, PGVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
load_dotenv()

CONNECTION_STRING = os.getenv("DATABASE_URL")
if not CONNECTION_STRING:
  raise ValueError("DATABASE_URL not found in environment variables. Please set it in your .env file.")

print("Loading local embedding model (all-MiniLM-L6-v2)...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
VECTOR_SIZE = 384

engine = PGEngine.from_connection_string(
    url=CONNECTION_STRING 
)

TABLE_NAME = "pixel_cat_knowledge"
print(f"📦 Initializing database table: {TABLE_NAME}...")
engine.init_vectorstore_table(
    table_name=TABLE_NAME,
    vector_size=VECTOR_SIZE
)

vector_store = PGVectorStore.create_sync(
    engine=engine,
    table_name=TABLE_NAME,
    embedding_service=embeddings
)

portfolio_docs = [
    Document(
        page_content=(
            "Faisal Abbas is a Full-Stack AI Engineer currently pursuing his BS in Computer Science. "
            "His engineering philosophy centers on bridging fluid, high-performance user interfaces with "
            "complex, intelligent backend systems. He specializes in building end-to-end production applications "
            "that integrate machine intelligence seamlessly into the web fabric."
        ),
        metadata={"category": "about_me", "topic": "summary"}
    ),
    Document(
        page_content=(
            "Faisal Abbas believes building great software is exactly like crafting a good narrative—it requires absolute precision, "
            "flawless pacing, and clean structure. He focuses on full-stack web architecture, custom AI agent workflows, "
            "and robust semantic search integrations."
        ),
        metadata={"category": "about_me", "topic": "philosophy"}
    ),

    Document(
        page_content=(
            "Faisal Abbas works as a Software and AI Engineer at Tricasol in Lahore, Punjab, Pakistan. "
            "In this role, he designs, builds, and deploys production-grade full-stack web applications and intelligent agent frameworks, "
            "focusing heavily on connecting modern frontends with robust backend logic and managing containerization lifecycles."
        ),
        metadata={"category": "experience", "company": "Tricasol", "role": "Software and AI Engineer Intern"}
    ),

    Document(
        page_content=(
            "Faisal Abbas's core technical toolkit and skills include: "
            "Frontend Frameworks: Next.js, React.js, TypeScript, Tailwind CSS, HTML, CSS, JavaScript. "
            "Backend & AI Architecture: Python, FastAPI, Next.js API Routes (NextRequest/NextResponse), n8n, LangChain, Retrieval-Augmented Generation (RAG). "
            "Infrastructure & Databases: Docker, Docker Compose, Linux, PostgreSQL, pgvector, Redis, MongoDB, Prisma ORM, Git, GitHub."
        ),
        metadata={"category": "skills", "topic": "tech_stack"}
    ),

    Document(
        page_content=(
            "Project Highlight - Autonomous WhatsApp AI Agent: Engineered by Faisal Abbas for Tricasol, this production-grade "
            "system streamlines business operations and communications. The backend utilizes n8n for agentic workflow orchestration, "
            "Retrieval-Augmented Generation (RAG) frameworks for data extraction, PostgreSQL and pgvector for semantic vector storage, "
            "Redis for fast caching, and the Evolution API to handle real-time WhatsApp streams. The entire environment is fully containerized using Docker."
        ),
        metadata={"category": "projects", "name": "whatsapp_ai_agent"}
    ),

    Document(
        page_content=(
            "Project Highlight - GoRoom.pk: Faisal Abbas is the lead full-stack architect and developer behind GoRoom.pk. "
            "This is an ongoing, real-world multi-hotel booking platform engineered for an onsite corporate client to manage "
            "end-to-end hospitality operations across a complete network of 8 hotels. The application features highly scalable "
            "full-stack web architecture constructed completely from scratch."
        ),
        metadata={"category": "projects", "name": "goroom_pk"}
    ),

    Document(
        page_content=(
            "Project Highlight - Corporate Frontend Deployments & Dashboards: Faisal Abbas has implemented highly responsive, production-ready "
            "frontend systems for onsite corporate clients, including optimized web builds for 'Go Guest House Lahore' "
            "and 'Hotel Haven Lahore'. He also builds high-performance analytical e-commerce dashboards designed to track complex transactional data."
        ),
        metadata={"category": "projects", "name": "corporate_frontends"}
    ),

    Document(
        page_content=(
            "Education: Faisal Abbas is pursuing a Bachelor of Science (BS) in Computer Science at Khwaja Fareed University of Engineering "
            "and Information Technology (KFUEIT) — Sub Campus, Rajanpur. He is currently in his third semester, maintaining a sharp focus on "
            "software architecture and artificial intelligence systems."
        ),
        metadata={"category": "education", "institution": "KFUEIT"}
    ),

    Document(
        page_content=(
            "The Pixel Cat assistant is an interactive, full-stack product element created by Faisal Abbas for his portfolio site. "
            "It merges professional engineering with a playful personality, serving as a live demonstration of custom RAG-trained AI applications. "
            "It answers questions with technical accuracy regarding Faisal's full-stack and AI skills, while preserving a fun, feline persona "
            "using text formatting quirks like '*purrs*', '*adjusts pixel glasses*', and 'Meow!'."
        ),
        metadata={"category": "bot_lore", "topic": "personality"}
    )
]

print(f"🚀 Vectorizing {len(portfolio_docs)} portfolio chunks and uploading to Neon Postgres...")
vector_store.add_documents(portfolio_docs)
print("✨ Database ingestion complete! Your portfolio is officially live inside pgvector.")
