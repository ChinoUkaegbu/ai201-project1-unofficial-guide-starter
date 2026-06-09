from ingest import load_and_chunk_documents
from retriever import embed_and_store


print("Loading chunks...")
chunks = load_and_chunk_documents()

print(f"Total chunks: {len(chunks)}")

print("\nEmbedding + storing in ChromaDB...")
embed_and_store(chunks)

print("\nReady for queries!\n")