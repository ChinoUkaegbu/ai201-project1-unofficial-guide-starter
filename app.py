from retriever import retrieve
from generator import generate_answer


def answer_question(query):

    results = retrieve(query, k=5)

    if len(results["documents"][0]) == 0:
        return "No relevant documents found."

    return generate_answer(query, results)

if __name__ == "__main__":

    while True:

        query = input("Question: ")

        if query.lower() == "exit":
            break

        print()
        print(answer_question(query))
        print()