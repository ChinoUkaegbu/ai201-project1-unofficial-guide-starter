import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "nyu_math_reviews"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ----------------------------
# Global initialization
# ----------------------------
model = SentenceTransformer(EMBEDDING_MODEL)

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)


def embed_and_store(chunks):
    texts = [c["text"] for c in chunks]

    embeddings = model.encode(texts).tolist()

    collection.add(
        embeddings=embeddings,
        documents=texts,
        metadatas=[
            {
                "source_type": c["source_type"],
                "title": c["title"],
                "chunk_id": c["chunk_id"]
            }
            for c in chunks
        ],
        ids=[c["chunk_id"] for c in chunks]
    )

    print(f"Stored {collection.count()} chunks.")


def retrieve(query, k=5, source_filter=None):

    # SAFETY CHECK
    if collection.count() == 0:
        raise ValueError(
            "Vector database is empty. Run build_index.py first."
        )
    
    query_embedding = model.encode([query]).tolist()

    # Build filter dict if provided
    where_clause = None
    if source_filter:
        where_clause = {"source_type": source_filter}

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"],
        where=where_clause
    )

    return results

def print_results(results):
    for i in range(len(results["documents"][0])):
        print("=" * 80)
        print("Rank:", i + 1)
        print("Distance:", results["distances"][0][i])
        print("\n", results["documents"][0][i])