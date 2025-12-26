# #main.py
# from fastapi import FastAPI, UploadFile, File, Form
# from summarizer import summarize_text
# from extractor import extract_text_from_file

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "AI Document Summarizer is running"}

# @app.post("/summarize")
# async def summarize(
#     text: str = Form(None),
#     file: UploadFile = File(None)
# ):
#     if file:
#         extracted_text = extract_text_from_file(file)
#         summary = summarize_text(extracted_text)
#         return {"summary": summary}

#     if text:
#         summary = summarize_text(text)
#         return {"summary": summary}

#     return {"error": "Please provide text or upload a file"}
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
    file: UploadFile = File(None)
):
    if not text and not file:
        raise HTTPException(400, "Please provide text or upload a file")

    if file:
        if file.content_type not in [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ]:
            raise HTTPException(400, "Only PDF and DOCX files are allowed")

        extracted_text = extract_text_from_file(file)
        summary = summarize_text(extracted_text)

        return {
            "summary": summary,
            "source": "file"
        }

    summary = summarize_text(text)
    return {
        "summary": summary,
        "source": "text"
    }
