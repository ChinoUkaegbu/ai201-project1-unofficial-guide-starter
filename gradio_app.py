import gradio as gr

from retriever import retrieve
from generator import generate_answer


def answer_question(query, source_filter):
    # ---- input validation ----
    if not query or query.strip() == "":
        return "Ask me something about NYU math professors or courses :)"
    
    if source_filter == "All":
        source_filter = None
    
    results = retrieve(query, k=5, source_filter=source_filter)

    if len(results["documents"][0]) == 0:
        return "No relevant documents found."

    return generate_answer(query, results)


demo = gr.Interface(
    fn=answer_question,
    inputs=[
        gr.Textbox(label="Ask about NYU Math Professors and Courses"),
        gr.Dropdown(
            choices=["All", "Rate My Professors", "Reddit"],
            value="All",
            label="Filter by Source"
        )
    ],
    outputs=gr.Textbox(label="Answer"),
    title="NYU Math Unofficial Guide",
    description="""
Ask questions about NYU math professors,
courses, and student experiences.
"""
)

demo.launch()