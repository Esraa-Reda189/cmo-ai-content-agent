# Pinecone RAG layer
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_cohere import CohereEmbeddings
from langchain_core.documents import Document

load_dotenv()

# ── Free Cohere embeddings (no pytorch, no payment needed) ──
embeddings = CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key=os.getenv("COHERE_API_KEY")
)

INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "cmo-content-kb")

def get_pinecone_index():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    existing_indexes = [i.name for i in pc.list_indexes()]
    if INDEX_NAME not in existing_indexes:
        print(f"Creating Pinecone index: {INDEX_NAME}...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=1024,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print("Index created successfully!")
    return pc.Index(INDEX_NAME)

def get_vector_store():
    get_pinecone_index()
    return PineconeVectorStore(
        index_name=INDEX_NAME,
        embedding=embeddings
    )

def store_brand_knowledge(brand_name: str, documents: list[dict]):
    """Store brand-specific knowledge in Pinecone."""
    vs = get_vector_store()
    docs = [
        Document(
            page_content=d["text"],
            metadata={
                "brand": brand_name,
                "type":  d.get("type", "general")
            }
        )
        for d in documents
    ]
    vs.add_documents(docs)
    print(f"✅ Stored {len(docs)} documents for brand: {brand_name}")

def retrieve_brand_knowledge(brand_name: str, query: str, k: int = 3) -> str:
    """Retrieve relevant brand knowledge to inject into prompts."""
    try:
        vs = get_vector_store()
        results = vs.similarity_search(
            query=query,
            k=k,
            filter={"brand": brand_name}
        )
        if not results:
            return "No specific brand knowledge available."

        knowledge = "\n".join([
            f"- [{doc.metadata.get('type', 'info')}]: {doc.page_content}"
            for doc in results
        ])
        return knowledge

    except Exception as e:
        print(f"RAG warning: {e}")
        return "No specific brand knowledge available."
