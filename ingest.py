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
            "Faisal Abbas is an AI Automation Engineer and Full-Stack Developer currently pursuing his BS in Computer Science. "
            "His engineering philosophy centers on the intersection of structured code and machine intelligence—bridging fluid, "
            "intuitive UI/UX with heavy-duty backend architecture to eliminate structural inefficiencies and scale business workflows."
        ),
        metadata={"category": "about_me", "topic": "summary"}
    ),
    Document(
        page_content=(
            "Faisal Abbas believes building great software is exactly like crafting a good narrative—it requires absolute precision, "
            "flawless pacing, and clean structure. He focuses on full-stack engineering, automation architecture, and innovative AI applications."
        ),
        metadata={"category": "about_me", "topic": "philosophy"}
    ),

    Document(
        page_content=(
            "Faisal Abbas works as a Software Engineer and AI Automation Intern at Tricasol in Lahore, Punjab, Pakistan (Joined June 2026). "
            "In this role, he designs and deploys production-grade automated frameworks and data-driven web platforms, "
            "focusing heavily on bridging fluid user experiences with complex backend logic and managing containerization lifecycles."
        ),
        metadata={"category": "experience", "company": "Tricasol", "role": "AI Automation Intern"}
    ),

    Document(
        page_content=(
            "Faisal Abbas's core technical toolkit and skills include: "
            "Frontend Frameworks: Next.js, React.js, TypeScript, Tailwind CSS, HTML, CSS, JavaScript. "
            "Backend & Automation: Python, FastAPI, Node.js, Express.js, n8n, LangChain, Retrieval-Augmented Generation (RAG). "
            "Infrastructure & Databases: Docker, Docker Compose, Linux, PostgreSQL, Redis, MongoDB, Prisma ORM, Git, GitHub."
        ),
        metadata={"category": "skills", "topic": "tech_stack"}
    ),

    Document(
        page_content=(
            "Project Highlight - WhatsApp AI Automation Agent: Engineered by Faisal Abbas for Tricasol, this production-grade "
            "system streamlines business operations and communications. The backend utilizes n8n for agentic workflow orchestration, "
            "Retrieval-Augmented Generation (RAG) frameworks for data extraction, PostgreSQL for vector storage, Redis for fast caching, "
            "and the Evolution API to handle real-time WhatsApp streams. The entire environment is fully containerized using Docker and Docker Compose."
        ),
        metadata={"category": "projects", "name": "whatsapp_ai_agent"}
    ),

    Document(
        page_content=(
            "Project Highlight - GoRoom.pk: Faisal Abbas is the lead full-stack architect and developer behind GoRoom.pk. "
            "This is an ongoing, real-world platform built for an onsite corporate client to manage end-to-end hospitality operations "
            "across a complete network of 8 hotels. The application features highly scalable web architecture constructed from scratch."
        ),
        metadata={"category": "projects", "name": "goroom_pk"}
    ),

    Document(
        page_content=(
            "Project Highlight - Corporate Frontend Deployments: Faisal Abbas has implemented highly responsive frontend systems "
            "for onsite corporate clients. This includes production-ready, highly optimized responsive web builds for 'Go Guest House Lahore' "
            "and 'Hotel Haven Lahore', alongside analytical e-commerce dashboards built to track complex transactional data."
        ),
        metadata={"category": "projects", "name": "corporate_frontends"}
    ),

    Document(
        page_content=(
            "Education: Faisal Abbas is pursuing a Bachelor of Science (BS) in Computer Science at Khwaja Fareed University of Engineering "
            "and Information Technology (KFUEIT) — Sub Campus, Rajanpur. He is currently in his third semester, maintaining a focus on "
            "software architecture and artificial intelligence systems."
        ),
        metadata={"category": "education", "institution": "KFUEIT"}
    ),

    Document(
        page_content=(
            "The Pixel Cat assistant (Meow-bot) is an interactive product element created by Faisal Abbas for his portfolio site. "
            "It merges professional engineering with playful personality, serving as a direct live demonstration of custom RAG-trained AI assistants. "
            "It answers questions with sharp technical accuracy regarding Faisal's skills, while preserving a fun, feline persona "
            "using text formatting quirks like '*purrs*', '*adjusts pixel glasses*', and 'Meow!'."
        ),
        metadata={"category": "bot_lore", "topic": "personality"}
    )
]

print(f"🚀 Vectorizing {len(portfolio_docs)} portfolio chunks and uploading to Neon Postgres...")
vector_store.add_documents(portfolio_docs)
print("✨ Database ingestion complete! Your portfolio is officially live inside pgvector.")