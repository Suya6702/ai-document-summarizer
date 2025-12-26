
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from summarizer import summarize_text
from extractor import extract_text_from_file

app = FastAPI(title="AI Document Summarizer")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Document Summarizer is running"}

@app.post("/summarize")
async def summarize(
    text: str = Form(None),
    file: UploadFile = File(None),
    length: str = Form("medium"),
    bullet: bool = Form(False)  # new
):
    if not text and not file:
        raise HTTPException(400, "Please provide text or upload a file")

    if file:
        if file.content_type not in [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ]:
            raise HTTPException(400, "Only PDF and DOCX files are allowed")
        text_content = extract_text_from_file(file)
    else:
        text_content = text

    summary = summarize_text(text_content, length=length, bullet=bullet)

    return {
        "summary": summary,
        "source": "file" if file else "text",
        "length": length,
        "bullet": bullet
    }
