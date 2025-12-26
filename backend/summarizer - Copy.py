#summarizer.py
from transformers import pipeline
import textwrap

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

MAX_CHARS = 1000  # safe chunk size

def summarize_text(text: str) -> str:
    if not text or len(text.strip()) < 100:
        return "Text is too short to summarize."

    # Split large text into chunks
    chunks = textwrap.wrap(text, MAX_CHARS)
    summaries = []

    for chunk in chunks[:20]:  # limit to avoid overload
        summary = summarizer(
            chunk,
            max_length=120,
            min_length=40,
            do_sample=False
        )
        summaries.append(summary[0]["summary_text"])

    return " ".join(summaries)
