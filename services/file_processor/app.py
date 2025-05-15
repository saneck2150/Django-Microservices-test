from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import hashlib, magic

app = FastAPI(title="File Processor Service")

@app.post("/process")
async def process(file: UploadFile):
    content = await file.read()

    # простейшая валидация
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(413, "File too large")

    meta = {
        "filename": file.filename,
        "size": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
        "mime": magic.from_buffer(content, mime=True),
    }
    return JSONResponse(meta)