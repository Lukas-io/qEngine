from fastapi import FastAPI, UploadFile, File, HTTPException
from app.text_extractor import extract_text
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "qEngine API is running!"}

@app.post("/extract-text/")
async def extract_text_api(file: UploadFile = File(...)):
    try:
        file_path = f"{UPLOAD_DIR}/{file.filename}"
        
        # Save file temporarily
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text
        extracted_text = extract_text(file_path)
        
        # Cleanup
        os.remove(file_path)

        return {"filename": file.filename, "extracted_text": extracted_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))