import json
from pathlib import Path

CHUNK_SIZE = 300
OVERLAP = 50


def clean_text(text: str) -> str:
    """
    Basic text cleaning.
    """
    return " ".join(text.split())


def sliding_window_chunk(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Split long text into overlapping chunks.
    """
    words = text.split()

    if len(words) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end >= len(words):
            break

        start += chunk_size - overlap

    return chunks


def build_rmp_chunks(document, source_file):
    chunks = []

    professor = document["title"]

    for idx, review in enumerate(document["entries"]):
        review = clean_text(review)

        # STEP 1: chunk raw review text
        raw_chunks = sliding_window_chunk(review)

        # STEP 2: attach metadata after chunking
        for chunk_num, raw_chunk in enumerate(raw_chunks):

            contextualized_text = f"""
Source: Rate My Professors
Title: {professor}

Review:
{raw_chunk}
""".strip()
            chunks.append(
                {
                    "chunk_id": f"{source_file}_{idx}_{chunk_num}",
                    "source_type": "rmp",
                    "title": professor,
                    "text": contextualized_text,
                    "raw_text": raw_chunk
                }
            )

    return chunks


def build_reddit_chunks(document, source_file):
    chunks = []

    title = document["title"]
    original_post = clean_text(document["original_post"])

    # Original post becomes its own chunk
    op_text = f"""
Source: Reddit
Title: {title}

Content:
{original_post}
""".strip()

   
    chunks.append(
        {
            "chunk_id": f"{source_file}_op",
            "source_type": "reddit",
            "title": title,
            "text": op_text,
            "raw_text": original_post
        }
    )

    # Comments become separate chunks (split if needed)
    for idx, comment in enumerate(document["comments"]):
        comment = clean_text(comment)

        # Only comments may be split (OP's text is not split)
        raw_chunks = sliding_window_chunk(comment)

        for chunk_num, raw_chunk in enumerate(raw_chunks):

            contextualized_comment = f"""
Source: Reddit
Title: {title}

Original Post:
{original_post}

Comment:
{raw_chunk}
""".strip()

    
            chunks.append(
                {
                    "chunk_id": f"{source_file}_{idx}_{chunk_num}",
                    "source_type": "reddit",
                    "title": title,
                    "text": contextualized_comment,
                    "raw_text": raw_chunk
                }
            )

    return chunks


def load_and_chunk_documents(data_dir="documents"):
    all_chunks = []

    for file_path in Path(data_dir).glob("*.json"):

        with open(file_path, "r", encoding="utf-8") as f:
            document = json.load(f)

        source_file = file_path.stem

        if document["source_type"] == "Rate My Professors":
            all_chunks.extend(
                build_rmp_chunks(document, source_file)
            )

        elif document["source_type"] == "Reddit":
            all_chunks.extend(
                build_reddit_chunks(document, source_file)
            )

    return all_chunks


if __name__ == "__main__":

    chunks = load_and_chunk_documents()

    print(f"Created {len(chunks)} chunks")

    if len(chunks) > 5:
        
        print("\nSample Chunks:\n")
        for i in range(5):
            print(f"Chunk {i+1}:")
            print(chunks[i]["text"])
            print("\n")