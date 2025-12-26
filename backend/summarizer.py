from transformers import pipeline
import textwrap

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

MAX_CHARS = 1000  # safe chunk size

LENGTH_MAP = {
    "short": {"min": 20, "max": 60},
    "medium": {"min": 40, "max": 120},
    "long": {"min": 80, "max": 200},
}

def summarize_text(text: str, length="medium", bullet=False) -> str:
    if not text or len(text.strip()) < 100:
        return "Text is too short to summarize."

    min_len = LENGTH_MAP.get(length, {"min": 40})["min"]
    max_len = LENGTH_MAP.get(length, {"max": 120})["max"]

    chunks = textwrap.wrap(text, MAX_CHARS)
    summaries = []

    for chunk in chunks[:20]:
        # If bullet points requested, prepend instruction
        input_text = f"Summarize in bullet points: {chunk}" if bullet else chunk

        summary = summarizer(
            input_text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )
        summaries.append(summary[0]["summary_text"])

    # Post-process: make each sentence a bullet if bullet=True
    if bullet:
        bullet_summary = ""
        for s in summaries:
            for line in s.split(". "):
                if line.strip():
                    bullet_summary += f"• {line.strip()}\n"
        return bullet_summary

    return " ".join(summaries)
