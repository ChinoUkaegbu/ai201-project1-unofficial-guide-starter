import gradio as gr

from retriever import retrieve
from generator import generate_answer


def answer_question(query):
    # ---- input validation ----
    if not query or query.strip() == "":
        return "Ask me something about NYU math professors or courses :)"
    
    results = retrieve(query, k=5)

    if len(results["documents"][0]) == 0:
        return "No relevant documents found."

    return generate_answer(query, results)


demo = gr.Interface(
    fn=answer_question,
    inputs=gr.Textbox(
        label="Ask about NYU Math Professors and Courses"
    ),
    outputs=gr.Textbox(
        label="Answer"
    ),
    title="NYU Math Unofficial Guide",
    description="""
Ask questions about NYU math professors,
courses, and student experiences.
"""
)

demo.launch()