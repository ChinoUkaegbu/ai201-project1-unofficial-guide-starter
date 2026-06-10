from ingest import load_and_chunk_documents
from retriever import embed_and_store, retrieve, print_results

# used to test retrieval

if __name__ == "__main__":

    print("Loading chunks...")
    chunks = load_and_chunk_documents()

    print(f"Total chunks: {len(chunks)}")

    print("\nEmbedding + storing in ChromaDB...")
    embed_and_store(chunks)

    print("\nReady for queries!\n")

    while True:
        query = input("Ask a question (or type 'exit'): ")

        if query.lower() == "exit":
            break

        results = retrieve(query, k=5)

        print_results(results)