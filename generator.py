import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def build_context(results):
    """
    Convert retrieved chunks into a prompt context.
    """

    return "\n\n".join(results["documents"][0])


def generate_answer(query, results):

    context = build_context(results)

    prompt = f"""
Answer the user's question using ONLY the information
provided in the context below.

If the context does not contain enough information,
respond exactly:

"I don't have enough information on that."

Do not use outside knowledge.
Do not make assumptions.

CONTEXT:
{context}

QUESTION:
{query}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    # detect refusal
    if "I don't have enough information" in answer:
        return answer

    # otherwise, display sources
    sources = sorted(
        {
            f"{meta['title']} ({meta['source_type']})"
            for meta in results["metadatas"][0]
        }
    )

    answer += "\n\nSources:\n"

    for source in sources:
        answer += f"- {source}\n"

    return answer